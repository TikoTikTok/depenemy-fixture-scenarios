# bulk-publish fixture

This fixture is designed to trigger `S008`.

## Scenario

The publisher released five suspicious packages in a short burst window. The metadata includes an explicit `_bulk_publish_context` block so tests can document the surrounding campaign.

## Expected outcome

- Dependency: `@test-fixture/bulk-published-depenemy-test@0.0.1`
- Expected rules: `S008`
- Expected verdict: alert

## Real-world precedent

Bulk registration and bulk publication are common in automated typosquatting and dependency confusion campaigns. The README references the broader ecosystem abuse pattern seen around the ua-parser-js incident timeframe in 2021, though this fixture specifically models the burst heuristic itself.
