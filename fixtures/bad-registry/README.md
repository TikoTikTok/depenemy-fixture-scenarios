# bad-registry fixture

This fixture is designed to trigger `B006`.

## Scenario

The lockfile `resolved` URL points to `npm.evil-corp-internal.example.com` instead of `registry.npmjs.org`. The integrity still matches the mocked registry metadata, so the only issue is the non-approved registry host.

## Expected outcome

- Dependency: `@test-fixture/private-mirror-depenemy-test@3.1.0`
- Expected rules: `B006`
- Expected verdict: block

## Real-world precedent

This simulates either a misconfigured internal Artifactory/Nexus proxy or an attacker-controlled registry override. The closest real-world precedent is dependency confusion, including Alex Birsan's 2021 research showing how private package resolution flows can be abused.
