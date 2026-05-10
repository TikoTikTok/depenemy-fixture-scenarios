# depenemy fixture scenarios

Test fixtures for the [depenemy](https://github.com/W3OSC/depenemy) npm supply chain security scanner.

Each fixture is a self-contained npm project paired with synthetic API responses so scanner tests run **without live network access**.

## What's here

- **`fixtures/`** — deterministic fixture scenarios (clean + various attack patterns)
- **`tests/`** — pytest unit tests validating depenemy rule evaluation against each fixture
- **`test-matrix.md`** — mapping of fixture → rule ID → expected verdict

## CI demo

This repository is the reference integration-test target for [W3OSC/depenemy PR #4](https://github.com/W3OSC/depenemy/pull/4).

The workflow runs three jobs on every push:

| Job | Fixture path | Expected result |
|-----|-------------|-----------------|
| `unit-tests` | `tests/` (mock metadata) | ✅ all rules pass |
| `scan-clean` | `fixtures/clean` | ✅ 0 findings |
| `scan-attack` | `fixtures/real-attack-simulation` | ⚠️ findings detected (expected) |

### Using the depenemy action in your own workflow

```yaml
- name: Run depenemy supply chain scan
  id: scan
  uses: W3OSC/depenemy@v1          # or TikoTikTok/depenemy@feat/github-action-docker for pre-release
  with:
    paths: .                        # directory containing package.json / package-lock.json
    fail-on: error                  # block the build on ERROR-severity findings
    upload-sarif: "false"           # set to "true" if GitHub Advanced Security is enabled
    token: ${{ secrets.GITHUB_TOKEN }}

- name: Upload SARIF
  if: always()
  continue-on-error: true
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: ${{ steps.scan.outputs.sarif-file }}
```

## Fixture directory structure

```text
fixtures/
├── clean/                    # healthy baseline — no findings expected
├── hash-mismatch/            # B005 — lockfile integrity tampered
├── bad-registry/             # B006 — tarball from unapproved host
├── lockfile-injection/       # B007 — resolved path swapped
├── install-script-new-dep/   # S001 — postinstall script in new dependency
├── typosquat/                # R009 — misspelled popular package name
├── bulk-publish/             # S008 — burst of packages from same publisher
├── ghost-repo/               # S007 — minimal facade repository
├── identity-mismatch/        # S009 — publisher ≠ repository owner
├── composite-score/          # C001 — multiple signals exceed threshold
└── real-attack-simulation/   # S006 + B005 — provenance regression + tampering
```

Each fixture contains:
- `package.json` — minimal app manifest
- `package-lock.json` — lockfile v3
- `mock-metadata.json` — mocked npm/GitHub API responses + normalized `depenemy_package_metadata`
- `README.md` — scenario narrative and expected rule IDs

## Running tests locally

```bash
pip install git+https://github.com/W3OSC/depenemy.git pytest
pytest tests/test_depenemy_rules.py -v
```
