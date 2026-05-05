import base64
import json
import sys
from datetime import datetime, timedelta, UTC
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import scrape_readmes
from scrape_readmes import (
    fetch_readme,
    process_repos,
    safe_filename,
    should_skip,
    write_readme,
)


def make_response(status_code, *, json_body=None, headers=None):
    resp = MagicMock()
    resp.status_code = status_code
    resp.headers = headers or {}
    if json_body is not None:
        resp.json.return_value = json_body
    if status_code >= 400:
        resp.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=resp
        )
    else:
        resp.raise_for_status.return_value = None
    return resp


def b64(s: bytes) -> str:
    return base64.b64encode(s).decode("ascii")


def test_safe_filename_basic():
    assert safe_filename("microsoft/vscode", "README.md") == "microsoft+vscode+README.md"


def test_safe_filename_rejects_plus():
    with pytest.raises(ValueError):
        safe_filename("foo/bar", "READ+ME.md")


def test_should_skip_recent_missing():
    recent = (datetime.now(UTC) - timedelta(days=5)).isoformat()
    assert should_skip({"status": "missing", "fetched_at": recent}) is True


def test_should_skip_old_missing():
    old = (datetime.now(UTC) - timedelta(days=60)).isoformat()
    assert should_skip({"status": "missing", "fetched_at": old}) is False


def test_should_skip_ok_never_skips():
    recent = datetime.now(UTC).isoformat()
    assert should_skip({"status": "ok", "fetched_at": recent}) is False


def test_fetch_readme_ok():
    body = {
        "name": "README.md",
        "sha": "abc123",
        "size": 11,
        "encoding": "base64",
        "content": b64(b"hello world"),
    }
    resp = make_response(
        200,
        json_body=body,
        headers={
            "ETag": '"etag-1"',
            "X-RateLimit-Remaining": "5000",
            "X-RateLimit-Reset": "9999999999",
        },
    )
    with patch.object(scrape_readmes.requests, "get", return_value=resp):
        result = fetch_readme("foo/bar", "tok")
    assert result["status"] == "ok"
    assert result["name"] == "README.md"
    assert result["content"] == b"hello world"
    assert result["etag"] == '"etag-1"'


def test_fetch_readme_not_modified():
    resp = make_response(304)
    with patch.object(scrape_readmes.requests, "get", return_value=resp):
        result = fetch_readme("foo/bar", "tok", etag='"etag-1"')
    assert result == {"status": "not_modified"}


def test_fetch_readme_missing():
    resp = make_response(404)
    with patch.object(scrape_readmes.requests, "get", return_value=resp):
        result = fetch_readme("foo/bar", "tok")
    assert result == {"status": "missing"}


def test_fetch_readme_429_then_ok():
    body = {
        "name": "README.md",
        "sha": "s",
        "size": 1,
        "encoding": "base64",
        "content": b64(b"x"),
    }
    rate_limited = make_response(429)
    success = make_response(
        200,
        json_body=body,
        headers={"ETag": '"e"', "X-RateLimit-Remaining": "5000", "X-RateLimit-Reset": "0"},
    )
    with patch.object(scrape_readmes.requests, "get", side_effect=[rate_limited, success]), \
         patch.object(scrape_readmes.time, "sleep") as mock_sleep:
        result = fetch_readme("foo/bar", "tok")
    assert result["status"] == "ok"
    mock_sleep.assert_called()


def test_fetch_readme_binary():
    body = {
        "name": "README",
        "sha": "s",
        "size": 4,
        "encoding": "base64",
        "content": b64(b"\xff\xfe\x00\x01"),
    }
    resp = make_response(
        200,
        json_body=body,
        headers={"ETag": '"e"', "X-RateLimit-Remaining": "5000", "X-RateLimit-Reset": "0"},
    )
    with patch.object(scrape_readmes.requests, "get", return_value=resp):
        result = fetch_readme("foo/bar", "tok")
    assert result["status"] == "binary"
    assert "content" not in result


def test_write_readme_creates_file_and_dir(tmp_path):
    out = write_readme("foo/bar", "README.md", b"hello", readme_dir=tmp_path)
    written = Path(out)
    assert written.read_bytes() == b"hello"
    assert written.name == "foo+bar+README.md"


def test_write_readme_collision_aborts(tmp_path):
    known = {}
    write_readme("foo/bar", "README.md", b"a", readme_dir=tmp_path, known_paths=known)
    with pytest.raises(RuntimeError):
        write_readme("foo/bar", "README.md", b"b", readme_dir=tmp_path, known_paths=known.copy() | {str(tmp_path / "foo+bar+README.md"): "other/repo"})


def test_process_repos_writes_and_updates_metadata(tmp_path, monkeypatch):
    stars_file = tmp_path / "github_stars.json"
    monkeypatch.setattr(scrape_readmes, "STARS_FILE", str(stars_file))
    readme_dir = tmp_path / "readmes"

    data = {
        "repositories": {
            "foo/bar": {"metadata": {"full_name": "foo/bar"}},
            "baz/qux": {"metadata": {"full_name": "baz/qux"}},
        },
    }

    body = {
        "name": "README.md",
        "sha": "sha-1",
        "size": 5,
        "encoding": "base64",
        "content": b64(b"hello"),
    }
    ok_resp = make_response(
        200,
        json_body=body,
        headers={"ETag": '"e1"', "X-RateLimit-Remaining": "5000", "X-RateLimit-Reset": "0"},
    )
    missing_resp = make_response(404)

    with patch.object(scrape_readmes.requests, "get", side_effect=[missing_resp, ok_resp]):
        process_repos(data, "tok", readme_dir=readme_dir)

    assert data["repositories"]["baz/qux"]["readme"]["status"] == "missing"
    assert data["repositories"]["foo/bar"]["readme"]["status"] == "ok"
    assert data["repositories"]["foo/bar"]["readme"]["etag"] == '"e1"'

    written = readme_dir / "foo+bar+README.md"
    assert written.read_bytes() == b"hello"

    saved = json.loads(stars_file.read_text())
    assert saved["repositories"]["foo/bar"]["readme"]["sha"] == "sha-1"


if __name__ == "__main__":
    pytest.main()
