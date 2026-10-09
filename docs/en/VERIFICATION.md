# Verification status

## 0.1.0a2

Local Linux checks passed: 31 tests, Ruff lint/format, doctor, external Sigma conversion and documentation links. Clean wheel installation outside the checkout passed doctor and all four bundle/integrity workflows.

[Implementation CI for 0.1.0a2](https://github.com/mejustbox-byte/detection-engineering-toolkit/actions/runs/37956459675) passed on Windows and Linux for commit `591dbdbd656f5143933c8397f517dbe5b9cb40d5`: 31 tests per OS, lint/format, doctor, build, bundle/integrity and wheel installation outside the checkout. Check separate Actions runs for the final merge commit and release; evidence from a different SHA does not replace that check.

## Published baseline 0.1.0a1

- Merge commit: `5e7800fb8c042bdc171d7b5aa8ed810a63673fa6`.
- [Linux/Windows CI](https://github.com/mejustbox-byte/detection-engineering-toolkit/actions/runs/37953235395): success, 20 tests per OS, lint, build and bundle smoke.
- [Release workflow](https://github.com/mejustbox-byte/detection-engineering-toolkit/actions/runs/37953436439): success, wheel installation outside the checkout and downloaded SHA256 verification.
- [Prerelease](https://github.com/mejustbox-byte/detection-engineering-toolkit/releases/tag/v0.1.0a1): wheel, sdist, source ZIP, notes and SHA256SUMS.

## Not run

Real Windows VM tests with upstream Atomic; Splunk/Defender delivery and query matches; real test cleanup; full macOS validation; full dependency/CVE audit. These remain `not_run` even when offline CI is green.

Evidence levels are described in [VALIDATION.md](VALIDATION.md). Lab evidence should include versions, UTC timestamps and each stage's result.
