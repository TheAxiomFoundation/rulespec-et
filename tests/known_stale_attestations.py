"""Encoding-manifest state recorded on 2026-10-14.

KNOWN_STALE_ATTESTATIONS lists manifest claims that were already stale. Each
entry is one claim in one manifest under .axiom/encoding-manifests/: the
file it attests, the sha256 the manifest records for that file, the sha256
the file had on 2026-10-14, the sha256 of the manifest file itself, and the
commits that changed the file after it was attested.

All of these changes landed in July 2026 (rulespec-et#8), while this
repository's generated-RuleSpec guard was off (run-generated-guard: false
until 2026-10-11), so CI never compared the edited files with their
manifests.

The listed manifests are manual attestations (runner: manual-attestation,
schema axiom-encode/applied-rulespec/v1), not encoder apply records. Listing
a claim here records the drift. It does not attest the current bytes, and
the manifest still attests the earlier ones.

KNOWN_UNMANIFESTED_MODULES lists the RuleSpec modules that had no encoding
manifest on 2026-10-14. Any other module without one fails.

Both lists are closed and may only shrink. test_encoding_manifests.py fails
if a listed file changes again, if a listed manifest is edited or removed
other than by an encoder replacement, if a module loses its manifest, or if
an entry is added or rewritten (each entry's digest must be in that file's
ADOPTED_LIST_SHA256). It warns when an entry resolves, for example once the
supervised encoder replaces a module's manifest; delete the entry then. New
drift is fixed through the encoder, not listed.
"""

from __future__ import annotations

from typing import NamedTuple


class StaleAttestation(NamedTuple):
    manifest: str
    manifest_sha256: str
    path: str
    attested_sha256: str
    current_sha256: str
    changed_by: tuple[str, ...]
    change: str


KNOWN_STALE_ATTESTATIONS: tuple[StaleAttestation, ...] = (
    StaleAttestation(
        manifest=".axiom/encoding-manifests/et/statutes/composed/pilot-worker-disposable-income-pipeline.json",
        manifest_sha256="363df9ff48056684ed6d86f61aa6643c1bbb553edc3d8562115f41a2346fb44b",
        path="et/statutes/composed/pilot-worker-disposable-income-pipeline.yaml",
        attested_sha256="4eb9bb6848a36a2f7a521cfdf3b313654d2d71b6d05c4a70ba2b93d2ffa8487c",
        current_sha256="a7bb30fa7e6dc67c4017ec7f327cb6ab8973af06b47a1005e05b6b1a9bf2f37b",
        changed_by=("2be2724994e517d2c151f1a0337d46230ebce163",),
        change=(
            "no formula, parameter or import changed: module citation list "
            "collapsed to one corpus_citation_path, upstream_source_check "
            "removed"
        ),
    ),
    StaleAttestation(
        manifest=".axiom/encoding-manifests/et/statutes/proc-1341-2024/value-added-tax-proclamation.json",
        manifest_sha256="52f4c38e4c6d52290113febe7e39bcd1d6c54a31a8d5f33597ac067c52d5ad81",
        path="et/statutes/proc-1341-2024/value-added-tax-proclamation.yaml",
        attested_sha256="4d5a0edbbefe60edd0ca100942f0349a200d51ec69b5a4996cd38b1526488a2b",
        current_sha256="3ea9da6146aee2d63aad171e5ad0ce0c483d941973707c93ef7b6b956f10cf37",
        changed_by=("2be2724994e517d2c151f1a0337d46230ebce163",),
        change=(
            "no formula, parameter or import changed: module citation list "
            "collapsed to one corpus_citation_path, upstream_source_check "
            "removed, 4 deferred outputs declared"
        ),
    ),
    StaleAttestation(
        manifest=".axiom/encoding-manifests/et/statutes/proc-1395-2025/income-tax-amendment-2025.json",
        manifest_sha256="5601c16bab5e13b13b65152851a04f9c8e15777be7cb63c7e3ad384d9b40a9e8",
        path="et/statutes/proc-1395-2025/income-tax-amendment-2025.yaml",
        attested_sha256="c9566a71c18c8f3e67d2830ce4245ca27241731aceec57e365f094b029bfe329",
        current_sha256="531ec1d2c3abee8d326a2dd524dd8f7669007b78f24332fc64a7509292cc04f3",
        changed_by=("2be2724994e517d2c151f1a0337d46230ebce163",),
        change=(
            "no formula, parameter or import changed: upstream_source_check removed"
        ),
    ),
    StaleAttestation(
        manifest=".axiom/encoding-manifests/et/statutes/proc-714-2011/public-servants-pension.json",
        manifest_sha256="823d94821261e3a00a7d4ca9f547a51fe0b732ec08fc418326f5d2d0a99a06a3",
        path="et/statutes/proc-714-2011/public-servants-pension.yaml",
        attested_sha256="a33a633721b42f9931a7cc14ad0c7f3ea260083e45abc50f394722c5c502d219",
        current_sha256="4714cdd1877a1e9dc2ec741b772ae8ccdda0bce760dd503358147bda5abbbd21",
        changed_by=("2be2724994e517d2c151f1a0337d46230ebce163",),
        change=("no formula, parameter or import changed: 3 proof excerpts changed"),
    ),
)

KNOWN_UNMANIFESTED_MODULES: tuple[str, ...] = (
    "et/regulations/dir-1021-2024/vat-electricity-water-exemption-directive.yaml",
)
