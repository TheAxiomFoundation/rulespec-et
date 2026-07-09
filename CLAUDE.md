# rulespec-et Agent Notes

This repo stores Ethiopia RuleSpec source registry materials, oracle references, and encoded policy rules. The modelled instruments are federal; all encoded law lives under a single `et/` national namespace.

## Scope

- `et/statutes/`: Federal proclamations — the Federal Income Tax Proclamation No. 979/2016 as amended by Proclamation No. 1395/2025 (employment and business schedules, minimum alternative tax, presumptive turnover schedule), the pension proclamations (No. 715/2011 private-organization, No. 714/2011 public servants, each as amended), the VAT Proclamation No. 1341/2024, and other primary law needed for tax-benefit modeling.
- `et/regulations/`: Council of Ministers regulations made under the proclamations (e.g., the income tax regulation No. 410/2017).
- `et/policies/`: ministry directives captured as verified reproductions where a gazette print is not digitized, and social-protection programme rules (the PSNP arms, school feeding and uniforms, fuel subsidies) set administratively.
- `programs/`: declarative compose specs (one per jurisdiction/program/period).
- `data/corpus/`, `data/coverage/`, `data/oracles/`: source inventory, coverage backlog, and comparison references. These are never legal authority.

## Do

- Start from the furthest upstream source: Federal Negarit Gazeta proclamation prints first (bilingual; the English text is citable — record whether a mirror host served the facsimile), Council of Ministers regulations next, Ministry of Revenues directives and programme manuals only after the governing proclamation is identified.
- Add RuleSpec under `et/statutes/`, `et/regulations/`, or `et/policies/` with companion `.test.yaml` files.
- Cite corpus paths from modules via `module.source_verification.corpus_citation_path` (or `corpus_citation_paths`).
- Use EFY2025/26 as the validation year (Ethiopia's fiscal year runs 8 July–7 July; ETMOD system ET_2025 corresponds to it, carrying the Proclamation 1395/2025 schedules effective July 2025). Indexed/annual values must be corpus-grounded, never invented.
- Keep exact oracle versions in `data/oracles/oracle-index.json`. The ETMOD bundle (SOUTHMOD A4.0) is licensed and non-redistributable — never commit bundle bytes, dataset rows, or model XML; only comparison statistics and ETMOD-produced values may be recorded.
- Sync `axiom-encode` and `.axiom/toolchain.toml` before substantial encoding runs (fetch origin and read the current version before every encode run and before choosing any version-bump number).

## Do Not

- Use Ministry of Revenues calculators, payroll summaries, or third-party alerts as the first legal source when a proclamation governs the rule.
- Invent, round, or interpolate any Ethiopian monetary amount, rate band, or threshold. Every number must come verbatim from a captured official provision.
- Migrate ETMOD, EUROMOD/SOUTHMOD, or agency calculator code mechanically as RuleSpec.
- Add generated source payload dumps, formula artifacts, `parameters.yaml`, or standalone YAML fixtures outside allowed RuleSpec roots.
- Hand-copy proclamation text into RuleSpec without a corpus `citation_path`.
