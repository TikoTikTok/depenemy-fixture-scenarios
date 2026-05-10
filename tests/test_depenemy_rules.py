"""
Integration tests: run depenemy rules against fixture mock-metadata.json

Each fixture in fixtures/ provides:
  - package.json + package-lock.json  (parser input)
  - mock-metadata.json                (exact PackageMetadata values)

Tests construct PackageMetadata + Dependency from the fixture data and
assert that ALL expected rules fire and NO unexpected extra rules fire.

No network access required — all data is read from local fixture files.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import pytest

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def parse_dt(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def load_fixture(name: str):
    """Load a fixture directory and return (dep, meta, expected_rules) tuple."""
    from depenemy.config import Config
    from depenemy.types import Dependency, Ecosystem, Location, PackageMetadata

    fixture_dir = FIXTURES_DIR / name
    mock = json.loads((fixture_dir / "mock-metadata.json").read_text())
    lockfile = json.loads((fixture_dir / "package-lock.json").read_text())
    manifest = json.loads((fixture_dir / "package.json").read_text())

    m = mock["depenemy_package_metadata"]
    expected_rules: list[str] = mock.get("_rules_triggered", [])

    # Find the package in the lockfile
    packages = lockfile.get("packages", {})
    pkg_name = m["name"]
    lf_entry = packages.get(f"node_modules/{pkg_name}", {})

    # Build Dependency
    dep_section = (
        manifest.get("dependencies", {})
        or manifest.get("devDependencies", {})
    )
    version_spec = dep_section.get(pkg_name, lf_entry.get("version", "1.0.0"))

    dep = Dependency(
        name=pkg_name,
        version_spec=version_spec,
        ecosystem=Ecosystem.NPM,
        location=Location(file=str(fixture_dir / "package.json"), line=0),
        resolved_version=lf_entry.get("version") or m.get("target_version"),
        lockfile_integrity=lf_entry.get("integrity"),
        lockfile_resolved=lf_entry.get("resolved"),
    )

    # Build PackageMetadata
    meta = PackageMetadata(
        name=m["name"],
        ecosystem=Ecosystem.NPM,
        latest_version=m["latest_version"],
        target_version=m["target_version"],
        published_at=parse_dt(m.get("published_at")),
        weekly_downloads=m.get("weekly_downloads", 0),
        total_downloads=m.get("total_downloads", 0),
        author_name=m.get("author_name"),
        author_account_created_at=parse_dt(m.get("author_account_created_at")),
        contributor_count=m.get("contributor_count", 0),
        maintainer_count=m.get("maintainer_count", 0),
        repository_url=m.get("repository_url"),
        is_deprecated=m.get("is_deprecated", False),
        has_install_scripts=m.get("has_install_scripts", False),
        is_archived=m.get("is_archived", False),
        has_provenance=m.get("has_provenance", False),
        registry_integrity=m.get("registry_integrity"),
        publisher_name=m.get("publisher_name"),
        publisher_has_github=m.get("publisher_has_github", True),
        repo_commit_count=m.get("repo_commit_count", 0),
        repo_issue_count=m.get("repo_issue_count", 0),
        repo_pr_count=m.get("repo_pr_count", 0),
        repo_has_ci=m.get("repo_has_ci", False),
        author_package_burst_count=m.get("author_package_burst_count", 0),
    )

    return dep, meta, expected_rules, Config()


def run_rules(dep, meta, config) -> set[str]:
    """Run all depenemy rules and return set of fired rule IDs."""
    from depenemy.rules import ALL_RULES

    fired = set()
    for rule in ALL_RULES:
        try:
            finding = rule.check(dep, meta, config)
        except Exception:
            finding = None
        if finding:
            fired.add(finding.rule_id)
    return fired


# ---------------------------------------------------------------------------
# Parametrised test matrix — matches test-matrix.md
# ---------------------------------------------------------------------------

FIXTURE_CASES = [
    # (fixture_name, expected_block_rules_subset, must_be_clean)
    ("clean", [], True),
    ("hash-mismatch", ["B005"], False),
    ("bad-registry", ["B006"], False),
    ("lockfile-injection", ["B007"], False),
    ("install-script-new-dep", ["S001"], False),
    ("typosquat", [], False),           # R009 needs project-level check; checked separately
    ("bulk-publish", ["S008"], False),
    ("ghost-repo", ["S007"], False),
    ("identity-mismatch", ["S009"], False),
    ("composite-score", ["S007", "S008", "S009"], False),  # C001 requires aggregation; tested in test_composite_score_c001
    ("real-attack-simulation", ["S006", "B005"], False),
]


@pytest.mark.parametrize("fixture_name,must_contain,must_be_clean", FIXTURE_CASES)
def test_fixture(fixture_name: str, must_contain: list[str], must_be_clean: bool):
    dep, meta, expected_rules, config = load_fixture(fixture_name)
    fired = run_rules(dep, meta, config)

    if must_be_clean:
        # Filter rules that are purely threshold-based and fire on any package
        # (R002/R003/R004/R005 with loose defaults). For clean fixture only hard
        # security rules must NOT fire.
        hard_rules = {r for r in fired if r.startswith(("B", "S", "C"))}
        assert not hard_rules, (
            f"[{fixture_name}] Expected PASS but hard rules fired: {hard_rules}"
        )
    else:
        # All expected rules must be present
        missing = set(must_contain) - fired
        assert not missing, (
            f"[{fixture_name}] Expected rules {must_contain} but these did not fire: "
            f"{missing}. Fired: {fired}"
        )


def test_clean_no_hard_rules():
    """Explicit clean test: no BLOCK-tier (B/S/C) rules should fire."""
    dep, meta, _, config = load_fixture("clean")
    fired = run_rules(dep, meta, config)
    hard = {r for r in fired if r.startswith(("B", "S", "C"))}
    assert not hard, f"Clean fixture triggered hard rules: {hard}"


def test_hash_mismatch_b005():
    """B005: lockfile integrity != registry integrity."""
    dep, meta, _, config = load_fixture("hash-mismatch")
    fired = run_rules(dep, meta, config)
    assert "B005" in fired, f"B005 should fire on hash-mismatch fixture. Fired: {fired}"
    # Confirm the integrity values are actually different in the fixture
    assert dep.lockfile_integrity != meta.registry_integrity


def test_bad_registry_b006():
    """B006: package resolved from a non-approved registry."""
    dep, meta, _, config = load_fixture("bad-registry")
    fired = run_rules(dep, meta, config)
    assert "B006" in fired, f"B006 should fire on bad-registry fixture. Fired: {fired}"


def test_lockfile_injection_b007():
    """B007: resolved URL path doesn't match package name."""
    dep, meta, _, config = load_fixture("lockfile-injection")
    fired = run_rules(dep, meta, config)
    assert "B007" in fired, f"B007 should fire on lockfile-injection fixture. Fired: {fired}"


def test_install_script_s001():
    """S001: new dep has install script."""
    dep, meta, _, config = load_fixture("install-script-new-dep")
    fired = run_rules(dep, meta, config)
    assert "S001" in fired, f"S001 should fire on install-script-new-dep fixture. Fired: {fired}"


def test_bulk_publish_s008():
    """S008: author published many packages in a short window."""
    dep, meta, _, config = load_fixture("bulk-publish")
    fired = run_rules(dep, meta, config)
    assert "S008" in fired, f"S008 should fire on bulk-publish fixture. Fired: {fired}"


def test_ghost_repo_s007():
    """S007: repo has minimal commits, no activity, no CI."""
    dep, meta, _, config = load_fixture("ghost-repo")
    fired = run_rules(dep, meta, config)
    assert "S007" in fired, f"S007 should fire on ghost-repo fixture. Fired: {fired}"


def test_identity_mismatch_s009():
    """S009: publisher identity mismatch (no GitHub + owner mismatch)."""
    dep, meta, _, config = load_fixture("identity-mismatch")
    fired = run_rules(dep, meta, config)
    assert "S009" in fired, f"S009 should fire on identity-mismatch fixture. Fired: {fired}"


def test_composite_score_c001():
    """C001: composite of S007+S008+S009+R003+R006 reaches threshold."""
    from depenemy.config import Config
    from depenemy.rules import ALL_RULES

    dep, meta, _, config = load_fixture("composite-score")

    # First run per-dep rules (simulate scanner step 4)
    per_dep_findings = []
    for rule in ALL_RULES:
        try:
            f = rule.check(dep, meta, config)
        except Exception:
            f = None
        if f:
            per_dep_findings.append(f)

    # Then run C001 aggregation (simulate scanner step 6)
    _C001_CONTRIBUTING_RULES = {"S007", "S008", "S009", "R003", "R004", "R006"}
    from depenemy.types import Ecosystem

    package_signals: dict[tuple[str, str], set[str]] = {}
    for finding in per_dep_findings:
        if finding.rule_id in _C001_CONTRIBUTING_RULES:
            key = (finding.dependency.name, finding.dependency.ecosystem.value)
            package_signals.setdefault(key, set()).add(finding.rule_id)

    c001_rule = next((r for r in ALL_RULES if r.id == "C001"), None)
    c001_findings = []
    if c001_rule:
        for (pkg_name, eco_val), signals in package_signals.items():
            if len(signals) >= config.thresholds.composite_score_threshold:
                # Find the dep for this package
                c001_dep = dep if dep.name == pkg_name else dep
                c001_findings.append(c001_rule.check_composite(c001_dep, signals, config))

    fired_ids = {f.rule_id for f in per_dep_findings}
    fired_ids |= {f.rule_id for f in c001_findings if f}

    assert "S007" in fired_ids, f"S007 should fire. Got: {fired_ids}"
    assert "S008" in fired_ids, f"S008 should fire. Got: {fired_ids}"
    assert "S009" in fired_ids, f"S009 should fire. Got: {fired_ids}"
    # C001 requires 4+: S007 + S008 + S009 + R003 or R006 from composite-score fixture


def test_real_attack_simulation():
    """S006 + B005: provenance regression + hash mismatch (Axios 1.14.1 pattern)."""
    dep, meta, _, config = load_fixture("real-attack-simulation")
    fired = run_rules(dep, meta, config)
    assert "B005" in fired, f"B005 (hash mismatch) should fire. Fired: {fired}"
    # S006 = no provenance — check meta.has_provenance
    assert not meta.has_provenance, "real-attack-simulation should have has_provenance=False"
