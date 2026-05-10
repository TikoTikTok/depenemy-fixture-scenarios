# hash-mismatch fixture

This fixture is designed to trigger `B005`.

## Scenario

The package looks healthy in every other respect, but the lockfile integrity was tampered. The lockfile contains a synthetic malicious hash while the mocked npm registry response returns a different synthetic canonical hash.

## Expected outcome

- Dependency: `@test-fixture/hash-tampered-depenemy-test@2.0.1`
- Expected rules: `B005`
- Expected verdict: block

## Real-world precedent

This is based on the Axios 1.14.1 supply chain attack from April 2024, where researchers documented a tampered package publication flow. In this fixture, the lockfile hash was modified to match a malicious tarball while the registry record still exposes the original integrity value.
