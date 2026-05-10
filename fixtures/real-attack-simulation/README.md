# real-attack-simulation fixture

This fixture is designed to trigger `S006` and `B005`.

## Scenario

Version `1.13.0` previously had provenance attestation, but version `1.14.1` does not. At the same time, the lockfile integrity differs from the registry integrity for the `1.14.1` tarball.

## Expected outcome

- Dependency: `@test-fixture/axios-pattern-depenemy-test@1.14.1`
- Expected rules: `S006`, `B005`
- Expected verdict: block

## Real-world precedent

This simulates the Axios 1.14.1 supply chain attack from April 2024. The fixture combines provenance regression with an integrity mismatch to model a package that no longer appears to be published through the expected trusted pipeline.
