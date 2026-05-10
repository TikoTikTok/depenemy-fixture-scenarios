# typosquat fixture

This fixture is designed to trigger `R009`.

## Scenario

The application depends on `expres` instead of `express`. That is a one-character deletion and a classic typosquatting pattern.

## Expected outcome

- Dependency: `expres@4.18.1`
- Expected rules: `R009`
- Expected verdict: alert

## Real-world precedent

Typosquatting has repeatedly affected npm, including `crossenv` targeting `cross-env` and `babelcli` targeting `babel-cli` in 2017. This fixture keeps the package name intentionally real-looking to exercise edit-distance matching.
