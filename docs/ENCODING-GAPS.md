# Encoding gaps

## `et/statutes/proc-1341-2024/value-added-tax-proclamation.yaml`

- Literal: `200`
- Encodes: the monthly domestic-electricity exemption threshold of 200 kWh.
- Provisions searched: every provision in the pinned Ethiopia corpus release was searched for the literal; the relevant occurrence is in `et/regulation/dir-1021-2024/vat-electricity-water-exemption-directive`, while the module's current `et/statute/proc-1341-2024/value-added-tax-proclamation` citation contains the encoded 15 percent standard VAT rate but not the 200 kWh threshold. The directive contains the encoded 200 kWh and 15 cubic-meter thresholds but does not contain the 15 percent standard rate.
- Judgment: the encoded value is supported and is probably correct; the gap is structural, not a wrong value or a missing corpus source. The module spans two instruments, and the single-provision numeric-grounding model has no consolidating provision that contains all three grounding values (`0.15`, `200`, and `15`).
