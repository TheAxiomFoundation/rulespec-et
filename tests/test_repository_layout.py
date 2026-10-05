from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
JURISDICTION_DIR_RE = re.compile(r"^[a-z]{2}(-[a-z0-9-]+)*$")
CONTENT_DIRS = ("statutes", "regulations", "policies", "legislation")
IGNORED_DIRS = {".git", ".pytest_cache", ".ruff_cache", ".venv", "__pycache__"}
ALLOWED_ROOT_DIRS = {".axiom", ".github", "bulk", "data", "docs", "tests", "et"}
ALLOWED_ROOT_FILES = {
    ".gitignore",
    "CLAUDE.md",
    "LICENSE",
    "LICENSE-CODE",
    "NOTICE",
    "README.md",
    "known-missing-money-atoms.yaml",
    "known-validation-gaps.yaml",
    "oracle-coverage-pending.yaml",
    "variables.toml",
}


def jurisdiction_dirs() -> list[Path]:
    return sorted(
        child
        for child in ROOT.iterdir()
        if child.is_dir()
        and JURISDICTION_DIR_RE.match(child.name)
        and any((child / marker).is_dir() for marker in CONTENT_DIRS)
    )


def rulespec_content_roots() -> list[Path]:
    return [
        jurisdiction / marker
        for jurisdiction in jurisdiction_dirs()
        for marker in CONTENT_DIRS
        if (jurisdiction / marker).is_dir()
    ]


def iter_rulespec_files() -> list[Path]:
    files: list[Path] = []
    for root in rulespec_content_roots():
        files.extend(
            path
            for path in root.rglob("*.yaml")
            if not path.name.endswith(".test.yaml")
        )
    return sorted(files)


def test_only_ethiopia_namespace_present() -> None:
    """The modelled instruments are federal: the only jurisdiction directory is et/."""
    names = {d.name for d in jurisdiction_dirs()}
    assert names <= {"et"}, f"unexpected jurisdiction dirs: {names - {'et'}}"


def test_et_content_buckets_exist() -> None:
    for marker in ("statutes", "regulations", "policies"):
        assert (ROOT / "et" / marker).is_dir(), f"missing et/{marker}"


def test_root_directories_are_allowed() -> None:
    # The org validate-rulespec workflow checks out sibling toolchain repos
    # (axiom-encode, axiom-rules-engine, ...) into a `_axiom/` directory and
    # skips any `_`- or `.`-prefixed directory during shard discovery. Mirror
    # that: ignore underscore/dot-prefixed dirs so CI's transient checkouts do
    # not trip the layout gate.
    found = {
        child.name
        for child in ROOT.iterdir()
        if child.is_dir()
        and child.name not in IGNORED_DIRS
        and not child.name.startswith(("_", "."))
    }
    unexpected = found - ALLOWED_ROOT_DIRS
    assert not unexpected, f"unexpected root directories: {unexpected}"


def test_root_files_are_allowed() -> None:
    # In a git worktree checkout `.git` is a gitdir-pointer file rather than
    # a directory, so exclude it here just as IGNORED_DIRS excludes the
    # `.git` directory in normal clones.
    found = {
        child.name
        for child in ROOT.iterdir()
        if child.is_file() and child.name != ".git"
    }
    unexpected = found - ALLOWED_ROOT_FILES
    assert not unexpected, f"unexpected root files: {unexpected}"


def test_every_rulespec_has_companion_test() -> None:
    """Any encoded rule module must ship a companion .test.yaml alongside it."""
    for path in iter_rulespec_files():
        companion = path.with_name(path.name[: -len(".yaml")] + ".test.yaml")
        assert companion.exists(), f"{path} is missing companion {companion.name}"


def test_money_atom_ratchet_is_nonnegative_int() -> None:
    payload = yaml.safe_load((ROOT / "known-missing-money-atoms.yaml").read_text())
    allowed = payload["total_allowed"]
    assert isinstance(allowed, int) and allowed >= 0


ORACLE_INDEX = ROOT / "data/oracles/oracle-index.json"
SOURCE_MAP = ROOT / "data/coverage/tax-benefit-source-map.json"
MODEL_ID = "etmod"
MODEL_NAME = "ETMOD"
SYSTEM_RE = re.compile(r"\b([A-Z]{2})_\d{4}\b")
# The other SOUTHMOD countries' model names (whose lower case is the model
# id), country names, and system or dataset-configuration prefixes. None
# belongs in Ethiopia's oracle index or source map; a record pasted from
# another country's repository is caught here.
OTHER_SOUTHMOD_NAMES = (
    "GHAMOD",
    "Ghana",
    "UGAMOD",
    "Uganda",
    "MicroZAMOD",
    "Zambia",
    "RWAMOD",
    "Rwanda",
)
OTHER_SOUTHMOD_SYSTEM_RE = re.compile(r"\b(?:gh|ug|zm|rw)_\d{4}", re.IGNORECASE)


def load_oracle() -> tuple[dict, dict]:
    payload = json.loads(ORACLE_INDEX.read_text())
    assert payload["jurisdiction"] == "et"
    oracles = payload["oracles"]
    assert len(oracles) == 1, "expected exactly one oracle (ETMOD)"
    return payload, oracles[0]


def rule_names(module: Path) -> set[str]:
    payload = yaml.safe_load(module.read_text())
    return {rule["name"] for rule in payload.get("rules", [])}


def test_oracle_index_records_etmod_wired() -> None:
    _, oracle = load_oracle()
    assert oracle["id"] == MODEL_ID
    assert oracle["name"] == MODEL_NAME
    assert oracle["url"].startswith("https://www.wider.unu.edu/about/")
    assert MODEL_ID in oracle["url"]
    assert oracle["authority"] == "wired_per_case_parity"
    assert oracle["availability_check"]["status"] == "wired_per_case_parity"
    detail = oracle["availability_check"]["detail"]
    assert "~/" not in detail and "/Users/" not in detail, "local path in detail"


def test_oracle_systems_and_names_are_ethiopian() -> None:
    _, oracle = load_oracle()
    wired = oracle["wired"]
    system_texts = [wired["system"], oracle["systems"]]
    system_texts += [suite["system"] for suite in wired["suites"] if "system" in suite]
    for text in system_texts:
        prefixes = set(SYSTEM_RE.findall(text))
        assert prefixes == {"ET"}, f"system text {text!r} has prefixes {prefixes}"
    assert wired["dataset_configuration"].startswith("et_")
    for suite in wired["suites"]:
        assert suite["suite"].startswith("et-"), suite["suite"]


def test_oracle_suite_counts_are_consistent() -> None:
    _, oracle = load_oracle()
    wired = oracle["wired"]
    suites = wired["suites"]
    for suite in suites:
        name = suite["suite"]
        assert suite["matched"] + suite["dispositioned"] == suite["comparisons"], name
        assert len(suite["axiom_outputs"]) == len(suite[f"{MODEL_ID}_variables"]), name
    totals = wired["totals"]
    assert totals["suites"] == len(suites)
    for key in ("cases", "comparisons", "matched", "dispositioned"):
        assert totals[key] == sum(suite[key] for suite in suites), key


def test_oracle_axiom_outputs_resolve_to_module_rules() -> None:
    _, oracle = load_oracle()
    for suite in oracle["wired"]["suites"]:
        for output in suite["axiom_outputs"]:
            match = re.fullmatch(r"et:([a-z0-9/_-]+)#([a-z0-9_]+)", output)
            assert match, f"{suite['suite']}: malformed output {output!r}"
            path, name = match.groups()
            module = ROOT / "et" / f"{path}.yaml"
            assert module.is_file(), f"{suite['suite']}: {output} has no module"
            assert name in rule_names(module), f"{suite['suite']}: {output} undefined"


def test_source_map_tracks_resolve() -> None:
    payload = json.loads(SOURCE_MAP.read_text())
    assert payload["jurisdiction"] == "et"
    _, oracle = load_oracle()
    suite_names = {suite["suite"] for suite in oracle["wired"]["suites"]}
    mapped: set[str] = set()
    for track in payload["tracks"]:
        for module in track.get("rulespec_modules", []):
            assert (ROOT / module).is_file(), f"{track['id']}: {module} missing"
            mapped.add(module)
        for suite in track.get("oracle_suites", []):
            assert suite in suite_names, f"{track['id']}: unknown suite {suite}"
    encoded = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "et").rglob("*.yaml")
        if not path.name.endswith(".test.yaml")
        and "programs" not in path.relative_to(ROOT / "et").parts
    }
    unmapped = encoded - mapped
    assert not unmapped, f"encoded modules missing from the source map: {unmapped}"


def test_no_other_southmod_country_in_oracle_metadata() -> None:
    for path in (ORACLE_INDEX, SOURCE_MAP):
        text = path.read_text()
        lowered = text.lower()
        for name in OTHER_SOUTHMOD_NAMES:
            assert name.lower() not in lowered, f"{path.name} names {name}"
        found = OTHER_SOUTHMOD_SYSTEM_RE.findall(text)
        assert not found, f"{path.name} has other-country systems {found}"


def test_toolchain_pins_are_full_shas() -> None:
    import tomllib

    payload = tomllib.loads((ROOT / ".axiom/toolchain.toml").read_text())
    toolchain = payload["toolchain"]
    assert set(toolchain) == {
        "axiom_corpus_release",
        "axiom_corpus_release_content_sha256",
        "validation_waiver_set_sha256",
    }
    assert re.fullmatch(
        r"[a-z]{2}-rulespec-\d{4}-\d{2}-\d{2}", toolchain["axiom_corpus_release"]
    ), "release must be an immutable dated name"
    sha256_re = re.compile(r"^[0-9a-f]{64}$")
    assert sha256_re.match(toolchain["axiom_corpus_release_content_sha256"])
    assert sha256_re.match(toolchain["validation_waiver_set_sha256"])
