Container Tools
=============

.. image:: https://raw.githubusercontent.com/avkcode/container-tools/refs/heads/main/favicon.svg
   :alt: Container Tools Logo
   :width: 80px
   :align: right

Build minimal, fast, and secure Debian- and RPM-based images from scratch. Container Tools uses ``debootstrap`` for Debian families and ``dnf --installroot`` for Fedora/CentOS-style families, with reproducible rootfs packaging, CI-friendly workflows, and easy validation via container-structure-test.

Version: ``1.0.0``

``1.0.0`` is the first normal release baseline. Major product, spec, CI, supply-chain, or compatibility changes should include an explicit SemVer bump from that point forward.

Why Container Tools?
--------------------

- Eliminate Dockerfile layer bloat and rebuild pain
- Include only the packages you need
- Use one workflow across Debian, Fedora, and CentOS Stream roots
- Build from declarative JSON image specs
- Export rootfs tarballs as OCI image archives
- Generate SBOM and SLSA-style provenance artifacts
- Verify rebuild-to-identical output
- First-class CI support (GitHub Actions)
- Built-in security scan and test automation

Quick Start
-----------

.. code-block:: bash

   git clone https://github.com/avkcode/container-tools.git
   cd container-tools
   make help
   make validate-specs
   make debian11-java-slim  # Example build target
   make fedora44            # RPM-based example target
   make build-spec SPEC=specs/fedora44.json

Use the image:

.. code-block:: bash

   cat debian/dist/debian11-java-slim/debian11-java-slim.tar | docker import - debian11-java-slim
   docker run -it debian11-java-slim /bin/bash

Highlights
----------

GitHub Actions pipeline
~~~~~~~~~~~~~~~~~~~~~~~

- CI runs static checks, spec dry-runs, OCI exporter smoke tests, and selected Debian/RPM builds
- Artifacts include rootfs tarballs, OCI archives, SBOMs, provenance, checksums, and logs
- No signing in CI unless signing secrets are explicitly provided; sign locally after download
- Tools detect GitHub Actions and automatically skip signing

Import artifacts or push to a registry:

.. code-block:: bash

   skopeo copy --insecure-policy docker-archive:/path/to/image.tar docker://yourrepo/yourimage:tag

Validate with container-structure-test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Test image contents, metadata, and commands
- Configs live under ``test/<name>.yaml``
- The test helper imports tarballs automatically when the image tag is missing

.. code-block:: bash

   ./scripts/test.py --image debian11-nodejs-23.11.0 --config test/debian11-nodejs-23.11.0.yaml

Declarative specs
~~~~~~~~~~~~~~~~~

Image specs live in ``specs/*.json`` and compile to the Debian or RPM builders:

.. code-block:: bash

   make validate-specs
   make build-spec SPEC=specs/debian11.json
   make build-spec SPEC=specs/fedora44.json
   make build-spec SPEC=specs/centos-stream10.json

Each spec defines the image name, distro family, release, package list, recipes, repository policy, and output behavior.

Specs are validated against ``specs/schema/image-spec-v1.json`` before CI dry-runs or builds. The validator reports JSON paths for schema failures and missing referenced recipe, script, keyring, or repository files.

Repository pinning is part of the spec contract. Debian specs can set ``debian.repoUrl`` and ``debian.securityRepoUrl`` to snapshot repositories. RPM specs can set ``rpm.repoFile`` to a checked-in or generated ``.repo`` file with pinned base URLs and GPG policy.

OCI, SBOM, and provenance
~~~~~~~~~~~~~~~~~~~~~~~~~

Spec builds can emit OCI archives and attestations:

.. code-block:: bash

   make oci ARTIFACT=rpm/dist/fedora44/fedora44.tar IMAGE_REF=example/fedora44:1.0.0
   make attest ARTIFACT=rpm/dist/fedora44/fedora44.oci.tar SPEC=specs/fedora44.json

``scripts/attest.py`` uses Syft when available and falls back to a deterministic SPDX document. Set ``GPG_KEY_ID`` to produce detached signatures for SBOM and provenance files.

Release evidence bundle
~~~~~~~~~~~~~~~~~~~~~~~

Release-like GitHub Actions runs generate one evidence bundle per baseline image. The bundle contains an OCI archive, SBOM, provenance, release gate result, strict reproducibility result, benchmark table, checksums, and optional detached GPG signatures:

.. code-block:: bash

   make release-evidence \
     TARGET=fedora44 \
     SPEC=specs/fedora44.json \
     ARTIFACT=rpm/dist/fedora44/fedora44.tar \
     METRICS=rpm/dist/fedora44/build_metrics.json \
     SECURITY_REPORT=rpm/dist/fedora44/security_scan.json

Signing is automatic when ``GPG_KEY_ID`` is configured. GitHub Actions skip signing unless signing material is explicitly enabled.

Reproducibility and benchmarks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   make repro-check SPEC=specs/fedora44.json
   make benchmark BENCHMARK_ARTIFACTS="rpm/dist/fedora44/fedora44.tar debian/dist/debian11/debian11.tar"

Benchmarks report artifact size and vulnerability counts from existing Trivy scan reports. Remote image comparisons are available through ``scripts/benchmark.py --image <ref>`` when Trivy is installed.

``make repro-check`` compares the rootfs tarball plus post-processing outputs: OCI archive, SBOM, provenance, and their checksums. Detached GPG signatures are intentionally excluded because OpenPGP signatures can include signer metadata and signature creation time; Syft-generated SBOM scanner metadata may also need explicit reproducibility configuration.

Continuous improvement spec
~~~~~~~~~~~~~~~~~~~~~~~~~~~

``PRODUCT_SPEC.md`` defines the product contract and ``specs/product-quality-gates.json`` makes the contract machine-checkable. Run:

.. code-block:: bash

   make improve-spec

The script writes ``reports/continuous-improvement.md`` and ``reports/continuous-improvement.json`` with a quality score, failed gates, and the next improvement plan. GitHub Actions runs the same audit on pushes, pull requests, schedules, and manual dispatches.

Release gates are configured in ``specs/product-quality-gates.json`` under ``releaseGates``. CI enforces those budgets after each baseline image build: compressed artifact size, build duration, installed package count, critical CVE count, and high CVE count. To check a built artifact locally, run:

.. code-block:: bash

   make release-gate \
     TARGET=fedora44 \
     ARTIFACT=rpm/dist/fedora44/fedora44.tar \
     METRICS=rpm/dist/fedora44/build_metrics.json \
     SECURITY_REPORT=rpm/dist/fedora44/security_scan.json

Tagged releases, manual runs, and scheduled runs also execute reproducibility checks with ``scripts/repro_check.py``.

Security scanning (Trivy)
~~~~~~~~~~~~~~~~~~~~~~~~~

- Available during builds via ``scripts/security-scan.sh``
- Control via ``CT_DISABLE_SECURITY_SCAN`` (omit/enable script) and ``CT_SKIP_SECURITY_SCAN`` (skip execution)
- ``CT_SECURITY_SCAN_SEVERITY`` controls report severities; ``CT_SECURITY_SCAN_EXIT_SEVERITY`` controls which severities fail the scan before release gates run.

Popular Targets
---------------

- ``debian11`` (base)
- ``debian11-java`` and ``debian11-java-slim``
- ``debian11-graal`` and ``debian11-graal-slim``
- ``debian11-nodejs-23.11.0``
- ``debian11-cuda-runtime`` (GPU-ready via NVIDIA Container Toolkit)
- ``fedora44`` (RPM base)
- ``fedora44-nodejs`` and ``fedora44-python``
- ``centos-stream10`` (RPM enterprise stream base)

CUDA quick start:

.. code-block:: bash

   make debian11-cuda-runtime
   docker run --rm -it --gpus all debian11-cuda-runtime nvidia-smi

Configuration (env vars)
------------------------

- ``VARIANT``: container | fakechroot | minbase (default: container)
- ``RELEASE``: Debian codename (default: bullseye)
- ``DIST_DIR``: output directory (default: debian/dist)
- Versions: ``JAVA_VERSION``, ``GRAALVM_VERSION``, ``CORRETTO_VERSION``, ``MAVEN_VERSION``, ``GRADLE_VERSION``, ``NODE_VERSION``, ``PYTHON_VERSION``
- RPM builds: ``RPM_DISTRO``, ``RPM_RELEASE``, ``RPM_DIST_DIR``, ``RPM_REPO_FILE``, ``RPM_GPGCHECK``, ``RPM_INSTALL_WEAK_DEPS``, ``RPM_PACKAGES``
- Spec builds: ``SPEC``, ``ARTIFACT``, ``IMAGE_REF``, ``OCI_OUTPUT``, ``BENCHMARK_ARTIFACTS``, ``EVIDENCE_DIR``, ``RELEASE_EVIDENCE_SIGN``

RPM examples:

.. code-block:: bash

   make fedora44
   make fedora44-python
   make centos-stream10
   make test DIST_DIR=rpm/dist

For production RPM builds, prefer ``RPM_REPO_FILE=/path/to/trusted.repo`` with repository signing keys controlled by your organization. The generated CentOS Stream repo enables package GPG checks by default; the generated Fedora repo is intended as a bootstrap convenience and should be replaced with a trusted repo file for hardened release pipelines.

Signing options
---------------

Sign and verify locally after CI:

.. code-block:: bash

   ./scripts/gpg.py --directory /path/to/tar/files --gpg-key-id YOUR_KEY_ID
   ./scripts/cosign.py --directory /path/to/tar/files --key cosign.key

Learn more
----------

- Examples: ``examples/`` (Java, Node.js, signing, testing)
- Makefile: all targets and build details
- Scripts: ``scripts/`` for security scan, tests, signing

Contributions welcome via issues and PRs.
