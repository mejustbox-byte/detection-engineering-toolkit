# Technology stack

| Component | Pinned version | Role |
|---|---|---|
| Python | source pin 3.12.15 | Local CLI, types and cross-platform runtime |
| uv | 0.12.23 | Lock, frozen sync and build |
| pySigma | 1.5.1 | Rule parsing and model |
| Splunk backend | 2.1.0 | SPL and Windows pipeline |
| Defender backend | 0.3.2 | KustoBackend and M365 Defender pipeline |
| PyYAML | 6.0.3 | Safe YAML parsing/serialization |
| pytest / Ruff | 9.1.1 / 0.16.10 | Regression and lint/format |
| setuptools | 80.9.0 | Wheel/sdist |

Python provides a mature Sigma ecosystem and straightforward installation. Real backends are used rather than a partial custom SPL/KQL implementation. The custom evaluator deliberately handles a few fields and is not presented as a Sigma engine.

`uv.lock` pins transitive versions. CI's Python 3.12 runtime can receive patch updates; reproducibility is scoped to the recorded Python version and lock, not byte-identical wheels across operating systems. Dependency changes require full regressions and query review.
