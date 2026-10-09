# Security

## Support

Development targets the current 0.1.0a2 prerelease. No SLA or long-term support policy has been announced. Older prereleases have no separate maintenance branch.

## Reporting a vulnerability

Check the repository Security tab and use private vulnerability reporting only if it is actually available. A dedicated private channel is not currently confirmed. Do not publish credentials, real events, exploit data or internal endpoints in an issue. Report ordinary bugs with a sanitized reproduction using synthetic inputs.

## Safe use

- Obtain code and release assets from the expected owner/repository and verify checksums.
- Keep inputs, reports and real logs outside the checkout; output is Git-ignored, but this does not prevent manual additions.
- Review external Sigma/Atomic YAML. Safe parsing does not establish command safety.
- `--lab-ack` outputs a command as text. Execute ShowDetails/CheckPrereqs/Cleanup manually only in the reviewed laboratory.
- The SHA256 manifest is unsigned and cannot prevent coordinated replacement of the entire package.

A full dependency/CVE audit and independent security assessment have not been run. See the [threat model](THREAT-MODEL.md) for implementation limits.
