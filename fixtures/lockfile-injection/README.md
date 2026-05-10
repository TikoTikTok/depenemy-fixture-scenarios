# lockfile-injection fixture

This fixture is designed to trigger `B007`.

## Scenario

The dependency name is `@test-fixture/injected-dep-depenemy-test`, but the lockfile `resolved` URL points at the tarball for `malware-payload`. The host remains `registry.npmjs.org`, so the registry itself looks approved, but the tarball path does not contain the expected normalized package name.

## Expected outcome

- Dependency: `@test-fixture/injected-dep-depenemy-test@1.0.0`
- Expected rules: `B007`
- Expected verdict: block

## Real-world precedent

This mirrors a lockfile injection pattern where an attacker edits `package-lock.json` so a trusted dependency resolves to a completely different tarball. The mismatch between expected package identity and tarball path is the core signal under test.
