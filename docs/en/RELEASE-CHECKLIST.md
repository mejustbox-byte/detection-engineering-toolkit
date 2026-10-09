# Release checklist

Complete this form for a specific release commit; an unchecked item is not a pass.

- [ ] Package version, runtime version, lock and tag agree.
- [ ] All commands and RU/EN documentation match the implementation.
- [ ] PR diff reviewed; Windows/Linux CI passed on the exact HEAD.
- [ ] Merge SHA matches main; main CI passed.
- [ ] Frozen installation, tests, lint/format and doctor passed.
- [ ] Wheel installed outside the checkout; bundle integrity passed.
- [ ] Source ZIP contains all tracked source and bilingual docs.
- [ ] No secrets, real events or private endpoints.
- [ ] Real Atomic/SIEM stages have justified pass/fail/not_run statuses.
- [ ] Prerelease flag and limitations included in notes.
- [ ] New tag points to the checked SHA and has never moved.
- [ ] Wheel/sdist/source/notes/SHA256SUMS published.
- [ ] Downloaded assets passed SHA256 checks.

See [RELEASE.md](RELEASE.md) and [VERIFICATION.md](VERIFICATION.md).
