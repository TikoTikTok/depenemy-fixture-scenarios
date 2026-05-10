# install-script-new-dep fixture

This fixture is designed to trigger `S001`.

## Scenario

The mocked npm metadata shows that the package exposes a `postinstall` script. The lockfile also includes `hasInstallScript: true` for documentation, but the metadata file is the authoritative source for the rule input.

## Expected outcome

- Dependency: `@test-fixture/postinstall-pkg-depenemy-test@0.9.1`
- Expected rules: `S001`
- Expected verdict: block

## Real-world precedent

This mirrors the event-stream incident from November 2018, where a malicious dependency (`flatmap-stream`) was added and used install-time execution to exfiltrate wallet data. Reference: CVE-2018-18074.
