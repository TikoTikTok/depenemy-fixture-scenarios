# composite-score fixture

This fixture is designed to trigger `C001` via five component signals.

## Scenario

The package simultaneously exhibits:

- `S007`: ghost repository
- `S008`: bulk publish burst
- `S009`: publisher identity concern
- `R003`: low weekly downloads
- `R006`: too few contributors

Because the composite threshold is 4 and this package triggers 5 contributing signals, `C001` should also fire.

## Expected outcome

- Dependency: `@test-fixture/composite-risk-depenemy-test@0.1.0`
- Expected rules: `S007`, `S008`, `S009`, `R003`, `R006`, `C001`
- Expected verdict: block

## Real-world precedent

This fixture models the combined pattern common in automated typosquatting and dependency confusion campaigns, where multiple weak signals line up at once rather than a single isolated red flag.
