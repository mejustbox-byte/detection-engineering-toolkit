# Release process

1. Align version across pyproject, `__init__`, lock and notes; update RU/EN documentation.
2. Run [VALIDATION.md](VALIDATION.md) checks and inspect for private data.
3. Open a PR, review the diff and wait for Windows/Linux CI on its exact HEAD.
4. Merge, wait for main CI and record the full merge SHA.
5. Run “Выпуск prerelease” in Actions from main: provide the merge SHA as `commit` and the version tag as `tag`, for example `v0.1.0a2`.
6. The build job checks checkout=main SHA and tag=package version, then runs frozen tests, lint, doctor, build and wheel smoke outside the checkout.
7. The publish job uses `contents: write` to create a new GitHub prerelease, downloads the assets and checks SHA256SUMS.
8. Verify the release page, tag commit, all assets and workflow Success. Never move a published tag.

## Artifacts

Wheel, sdist, tracked source ZIP, bilingual notes and SHA256SUMS. The source ZIP includes lock, scripts, tests, docs and workflow. Pip wheel installation is not equivalent to a frozen source install. SHA256SUMS is not a digital signature.

## Failures

Existing tags/releases are not overwritten. If publishing creates a release but asset verification fails, inspect published files first; do not blindly repeat creation. A corrected product receives a new version. Explicitly retain real-lab `not_run` status.
