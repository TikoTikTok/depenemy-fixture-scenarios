# clean fixture

This fixture simulates a healthy, well-maintained open source library. No depenemy rules should fire.

## Expected outcome

- Dependency: `@test-fixture/well-maintained-depenemy-test@1.2.3`
- Expected rules: none
- Expected verdict: pass / green light

## Why it should pass

- Lockfile and registry integrity match exactly.
- The tarball resolves from `registry.npmjs.org`.
- The tarball path contains the expected package name.
- Downloads, contributors, repository activity, CI, and publisher history all look healthy.
- Provenance is present and there are no install scripts.

Use this as the baseline control fixture for parser and rules tests.
