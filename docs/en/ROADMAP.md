# Roadmap

| Milestone | Outcome | Status |
|---|---|---|
| Offline MVP | Four scenarios, Sigma, SPL/KQL, cases, Atomic plan | Implemented in 0.1.0a1 |
| Working workflows | doctor, external Sigma, integrity, snapshot provenance, RU/EN | Implemented in 0.1.0a2 |
| Laboratory validation | Windows VM, real Atomic GUIDs, delivery and matches in both SIEMs | Not run |
| Operational suitability | Deployment tuning, false-positive baseline, data-source profiles | Planned |
| Catalogue expansion | More specific scenarios and ATT&CK dataset provenance | Planned |
| Artifact protection | Signatures, dependency audit and supply-chain provenance | Planned |

The next priority is laboratory evidence for existing rules, not increasing technique counts. Acceptance requires recorded versions, one upstream GUID, observable telemetry, query match, a negative case and cleanup. Stable/production-ready status is withheld until that evidence exists.

SIEM APIs and an automatic runner have no approved implementation. They require a separate threat model, isolation and credential management before implementation.
