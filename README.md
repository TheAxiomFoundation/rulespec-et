# rulespec-et

Ethiopia RuleSpec source registry.

This repository targets the Ethiopia tax-benefit surface: employment and business income tax under the Federal Income Tax Proclamation No. 979/2016 as amended by the Income Tax (Amendment) Proclamation No. 1395/2025 (including the minimum alternative tax and the presumptive turnover schedule), pension contributions under the Private Organization Employees' Pension Proclamation No. 715/2011 and the Public Servants' Pension Proclamation No. 714/2011 (each as amended), value added tax under the VAT Proclamation No. 1341/2024, and the transfer programmes needed for household-level calculations (the urban and rural Productive Safety Net Programme arms, school feeding and school uniforms, and fuel subsidies). Ethiopia is a federation, but the modelled instruments are federal; all encoded law lives under a single `et/` national namespace.

Ethiopia's fiscal year runs 8 July to 7 July (Hamle 1 in the Ethiopian calendar). The validation year for encoded amounts is **EFY2025/26** (from July 2025); effective dates follow each proclamation's own commencement provision.

## Source priority

Policy must come from the furthest upstream available source.

1. Federal Negarit Gazeta proclamation prints (House of Peoples' Representatives; bilingual Amharic/English — the English text is citable) and Council of Ministers regulations — the authentic text of the income tax, pension, and VAT law and their amendments. Gazette-facsimile mirrors are acceptable when the official portal does not serve the print, recorded with the host in manifest metadata.
2. Ministry of Revenues directives and guidance only after the governing proclamation is identified.
3. Ministry programme documentation (PSNP implementation manuals, school feeding and uniform programme documents, petroleum pricing/subsidy instruments) for rules set administratively rather than by proclamation.
4. Oracles only for household-level parity tests against an external source that can calculate the same household case, never as law.

## Oracle scope

An oracle is an executable, pinned external calculator that accepts household-level inputs and returns household-level tax-benefit outputs comparable to Axiom outputs. Aggregate simulators, distributional reports, parameter documentation, and public model summaries are not oracles for RuleSpec parity, even when they are useful as background references.

The Ethiopia household oracle is **ETMOD**, the SOUTHMOD tax-benefit microsimulation model for Ethiopia (UNU-WIDER). ETMOD is wired by six per-case comparison suites in [axiom-oracles](https://github.com/TheAxiomFoundation/axiom-oracles) (`comparisons/et-*.yaml`), run on system ET_2025 (EFY2025/26). The SOUTHMOD_A4.0 Adhesion Agreement bars giving the bundle to third parties, so those suites run only on the machine that holds it, never on shared CI; the committed reports are the record. `data/oracles/oracle-index.json` pins the bundle hash and lists each suite with the outputs it compares.

## Listing gates

This repo carries `app_visibility = "experimental"` in `.axiom/registry.toml` and stays out of app surfaces until:

1. The encoded surface covers the flagship calculation (employment income tax gross-to-net for a formal employee) end to end with companion tests.
2. Oracle parity suites exist and pass against ETMOD for the encoded surface. Status: **partially met**. Six suites compare this repository with ETMOD: 32 of 34 comparisons match, and the other 2 are dispositioned ETMOD findings on the minimum alternative tax in `et-business-mat` (see `data/oracles/oracle-index.json`). Some agreement is not independent validation: `et-dispy` compares a single-employee composition, not a provision of law, so it tests only the imported tax and pension arithmetic, and in `et-presumptive` and `et-vat` both sides share a reading the law leaves open (a marginal reading of the Article 50 table, and a cliff at the Directive 1021/2024 thresholds). The compared modules are not supervised-encoder output ([#19](https://github.com/TheAxiomFoundation/rulespec-et/issues/19)), so the suites must be re-run after the supervised re-encode, and not every module has a comparison (the Directive 1021/2024 module and the Proclamation 714/2011 employee and civil service office shares have none).
3. Citation paths are stable (proclamation-number form against the Federal Negarit Gazeta prints).
