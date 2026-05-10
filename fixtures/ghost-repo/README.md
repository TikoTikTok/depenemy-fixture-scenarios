# ghost-repo fixture

This fixture is designed to trigger `S007`.

## Scenario

The linked GitHub repository looks like a facade: one commit, no issues, no pull requests, and no CI workflow. That satisfies all three ghost-repo signals.

## Expected outcome

- Dependency: `@test-fixture/ghost-repo-depenemy-test@1.0.0`
- Expected rules: `S007`
- Expected verdict: alert

## Real-world precedent

Attackers often create a minimally populated repository to make a malicious package appear legitimate. This pattern has shown up repeatedly in dependency confusion and typosquatting campaigns from 2022 through 2024.
