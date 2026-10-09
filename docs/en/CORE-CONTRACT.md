# Product contract

## Scenario to rule

A technique ID has the form `Tdddd` or `Tdddd.ddd`. Generation supports only four built-in records. UUIDs depend on scenario ID and namespace v1, not execution time. Rules match `Image|endswith`; T1016 additionally uses `CommandLine|contains|all: ['/all']`. This is substring matching, not argument parsing: `/alligator` also contains `/all`.

## Conversion

Every call creates a fresh `SigmaCollection` because processing pipelines may mutate rules. Splunk uses `splunk_windows_pipeline`; Defender uses `microsoft_365_defender_pipeline`. `convert-file` accepts external YAML containing one or more backend-supported rules. Arbitrary logsources, correlation and every Sigma modifier are not guaranteed; conversion errors return exit code 2. This version does not expose custom pipelines or SIEM configuration through the CLI.

## Labelled cases

```json
[
  {"id":"positive","expected":true,"event":{"Image":"C:\\Windows\\System32\\whoami.exe","CommandLine":"whoami"}},
  {"id":"negative","expected":false,"event":{"Image":"C:\\Windows\\System32\\notepad.exe"}}
]
```

`id` is a unique string, `expected` is boolean, and `event` is an object. Present `Image` and `CommandLine` values must be strings. Missing Image never matches. String suffix/substring checks use `casefold`. Time, parent process, user and host are not evaluated. `validate` does not accept external Sigma rules or establish backend semantic equivalence.

## Inputs and packages

UTF-8 JSON/YAML with an 8 MiB limit per read file. YAML uses `safe_load`; Atomic metadata must be JSON-compatible and acyclic. This is a size bound, not a sandbox or complete exhaustion defense.

A package contains seven artifacts and a manifest. Schema version 1 records the product version. Verification also accepts the old 0.1.0a1 manifest without schema_version. The exact file list is required; digests are 64 lowercase hexadecimal characters. The manifest is neither hashed nor signed: modifying both a file and the manifest can evade detection. File symlinks are rejected, but verification does not defend against concurrent local modification.

## Atomic

The YAML technique, GUID and Windows platform are checked. The hash covers the same snapshot that was parsed. `source_commit` is not verified through Git or a network. Commands are data; behavior, dependencies and cleanup require manual review. `--lab-ack` is not an executor.
