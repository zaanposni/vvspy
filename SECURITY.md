# Security Policy

## Supported Versions

Only the latest release receives security fixes.

| Version | Supported          |
| ------- | ------------------ |
| 2.x.x   | :white_check_mark: |
| 1.x.x   | :x:                |

vvspy supports all Python versions that have not reached their
[end of life](https://devguide.python.org/versions/).

## Reporting a Vulnerability

Please do not report vulnerabilities in public issues. Instead, report them privately via
[GitHub Security Advisories](https://github.com/zaanposni/vvspy/security/advisories/new)
or via mail at <vvspy-vul@zaanposni.com>.

## Release Integrity

Releases are built and published to PyPI by GitHub Actions using
[Trusted Publishing](https://docs.pypi.org/trusted-publishers/). Every release
on PyPI comes with a [digital attestation](https://docs.pypi.org/attestations/)
linking it to the workflow run and commit it was built from.
