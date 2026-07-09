# rulespec-et

Ethiopia RuleSpec source registry.

This repository targets the Ethiopia tax-benefit surface: employment and business income tax under the Federal Income Tax Proclamation No. 979/2016 as amended by the Income Tax (Amendment) Proclamation No. 1395/2025 (including the minimum alternative tax and the presumptive turnover schedule), pension contributions under the Private Organization Employees' Pension Proclamation No. 715/2011 and the Public Servants' Pension Proclamation No. 714/2011 (each as amended), value added tax under the VAT Proclamation No. 1341/2024, and the transfer programmes needed for household-level calculations (the urban and rural Productive Safety Net Programme arms, school feeding and school uniforms, and fuel subsidies). Ethiopia is a federation, but the modelled instruments are federal; all encoded law lives under a single `et/` national namespace.

Ethiopia's fiscal year runs 8 July to 7 July (Hamle 1 in the Ethiopian calendar). The validation year for encoded amounts is **EFY2025/26** (from July 2025); effective dates follow each proclamation's own commencement provision.

## Source Priority

Policy must come from the furthest upstream available source.

1. Federal Negarit Gazeta proclamation prints (House of Peoples' Representatives; bilingual Amharic/English — the English text is citable) and Council of Ministers regulations — the authentic text of the income tax, pension, and VAT law and their amendments. Gazette-facsimile mirrors are acceptable when the official portal does not serve the print, recorded with the host in manifest metadata.
2. Ministry of Revenues directives and guidance only after the governing proclamation is identified.
3. Ministry programme documentation (PSNP implementation manuals, school feeding and uniform programme documents, petroleum pricing/subsidy instruments) for rules set administratively rather than by proclamation.
4. Oracles only for household-level parity tests against an external source that can calculate the same household case, never as law.

## Oracle Scope

An oracle is an executable, pinned external calculator that accepts household-level inputs and returns household-level tax-benefit outputs comparable to Axiom outputs. Aggregate simulators, distributional reports, parameter documentation, and public model summaries are not oracles for RuleSpec parity, even when they are useful as background references.

ETMOD (the SOUTHMOD tax-benefit model for Ethiopia, UNU-WIDER, run on the EUROMOD engine) is the parity oracle for this repository. The SOUTHMOD bundle is licensed and non-redistributable: it is referenced by path/sha only, and no bundle bytes, dataset rows, or model XML appear in this repository or its validation artifacts — only comparison statistics and model-produced values.

## Listing gates

This repo carries `app_visibility = "experimental"` in `.axiom/registry.toml` and stays out of app surfaces until:

1. The encoded surface covers the flagship calculation (employment income tax gross-to-net for a formal employee) end to end with companion tests.
2. Oracle parity suites exist and pass against ETMOD for the encoded surface.
3. Citation paths are stable (proclamation-number form against the Federal Negarit Gazeta prints).
