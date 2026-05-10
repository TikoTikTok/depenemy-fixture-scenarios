# identity-mismatch fixture

This fixture is designed to trigger `S009`.

## Scenario

The npm publisher is `attacker-npm-user`, but the linked source repository belongs to `legitorg`. The publisher also has no matching GitHub account in the mocked user lookup.

## Expected outcome

- Dependency: `@test-fixture/identity-mismatch-depenemy-test@2.3.0`
- Expected rules: `S009`
- Expected verdict: alert

## Real-world precedent

This models the account-takeover pattern associated with the node-ipc protestware incident in March 2022, where npm publication identity diverged from what consumers expected from the legitimate project.
