# update-python-venv-requirements-and-sbom
Update Python modules in a project's VENV dir, update requirements.txt and also update the Software Bill of material (SBOM)

# Background
Vulnerabilities in dependencies like log4j have shown, that there is the need to understand which application contain which
dependencies to be able to react. Do you operate Internet-facing applications? Maybe in setups that you can't just update with
pkg|yum|apt upgrade|update?

One day we may process vulnerability feeds with machine-readable advisories and match them
against an asset repository with SBOM descriptions. Everything is there to do that. Advisories, vulnerability feeds, software
such as CycloneDX to track dependencies. There are still gaps in tooling. Another missing part are SBOM descriptions for projects.

This tool is a personal helper script to generate and update SBOM files.
