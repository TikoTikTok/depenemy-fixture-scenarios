# depenemy fixture test matrix

| Fixture Directory | Dependency Package Name | Rule ID(s) | Expected Verdict | Severity | Real-World Precedent | CVE/Incident Reference |
| --- | --- | --- | --- | --- | --- | --- |
| `clean` | `@test-fixture/well-maintained-depenemy-test` | none | PASS | PASS | Healthy baseline package | N/A |
| `hash-mismatch` | `@test-fixture/hash-tampered-depenemy-test` | `B005` | BLOCK | ERROR | Tampered tarball / lockfile integrity mismatch | Axios 1.14.1 supply chain attack (Apr 2024) |
| `bad-registry` | `@test-fixture/private-mirror-depenemy-test` | `B006` | BLOCK | ERROR | Dependency confusion / malicious mirror host | Alex Birsan dependency confusion research (2021) |
| `lockfile-injection` | `@test-fixture/injected-dep-depenemy-test` | `B007` | BLOCK | ERROR | Lockfile `resolved` path swapped to a different tarball | npm lockfile injection attack pattern |
| `install-script-new-dep` | `@test-fixture/postinstall-pkg-depenemy-test` | `S001` | BLOCK | ERROR | Malicious install hook in transitive dependency | event-stream / flatmap-stream (Nov 2018, CVE-2018-18074) |
| `typosquat` | `expres` | `R009` | ALERT | WARNING | Popular-package misspelling used for typosquatting | `crossenv` / `babelcli` typosquatting incidents (2017) |
| `bulk-publish` | `@test-fixture/bulk-published-depenemy-test` | `S008` | ALERT | WARNING | Burst registration of many lookalike packages | ua-parser-js ecosystem abuse pattern (Oct 2021, CVE-2021-41265 context) |
| `ghost-repo` | `@test-fixture/ghost-repo-depenemy-test` | `S007` | ALERT | WARNING | Facade repository with little real engineering activity | Dependency confusion / typosquatting campaigns (2022-2024) |
| `identity-mismatch` | `@test-fixture/identity-mismatch-depenemy-test` | `S009` | ALERT | WARNING | Compromised publisher identity vs legitimate project identity | node-ipc protestware incident (Mar 2022) |
| `composite-score` | `@test-fixture/composite-risk-depenemy-test` | `S007`, `S008`, `S009`, `R003`, `R006`, `C001` | BLOCK | ERROR | Multi-signal malicious package profile | Automated typosquatting / dependency confusion campaigns |
| `real-attack-simulation` | `@test-fixture/axios-pattern-depenemy-test` | `S006`, `B005` | BLOCK | ERROR | Provenance regression and tarball tampering in a popular package | Axios 1.14.1 incident (Apr 2024) |
