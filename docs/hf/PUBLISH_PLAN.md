# Publish plan for `muse-eeg-windows`

## Release order

1. Freeze subject-wise split JSON, manifests, labels, channel order, preprocessing notes, and SHA256 checksums.
2. Publish `muse4_vigilance_sleep_edf` first, with Sleep-EDF/HMC attribution and a clear Muse4-proxy statement.
3. Publish Crown8 attention configs only as separately named research configs after shape/order QC.
4. Publish Muse4 attention and `muse4_engagement_a_eng` as research/reproducibility data only; retain `ship_candidate: false` and the known holdout limitations.
5. Tag an immutable dataset revision and update the card with measured sizes, feature schema, and source-specific license links.

## Never publish in this dataset

- Raw EDF/BDF/PSG files or private source caches.
- L-FAME or any BY-NC/restricted academic-only corpus.
- Gated REVE weights, REVE position/model caches, CBraMod caches, or private credentials.
- Private Kaggle dataset contents or artifacts that are not explicitly cleared for redistribution.
- Secrets, tokens, personal recordings, or files whose provenance/license is unresolved.
- A claim that proxy sleep, attention, or engagement labels are native Muse labels or clinical truth.

## HF vs GitHub vs OpenNeuro vs Kaggle

| Location | Put here | Do not put here |
|---|---|---|
| Hugging Face | Versioned derived windows, labels, manifests, checksums, card, and small usage notes | Raw upstream recordings, gated weights, private cache |
| GitHub (`muse-eeg-heads`) | Scripts, schemas, split policy, QC reports, docs, and reproducible export code | Large binaries and credentials |
| OpenNeuro | Cite and obtain the original OpenNeuro source datasets under their records/licenses | Treating this derived dataset as an OpenNeuro mirror |
| Kaggle | Temporary/private scratch only when access is intentional and documented | Canonical public release, gated data, or a second conflicting source of truth |

## PhysioNet windows-only policy

PhysioNet sources (including Sleep-EDF and EEGMAT) are provenance sources, not files to mirror here. Upload only derived windows when the applicable terms permit redistribution; retain source name, URL, license/SPDX value, processing recipe, and checksums. Do not upload raw PhysioNet EDF/PSG files, credentials, or private downloads. Users who need the raw source must retrieve it from PhysioNet under its current access terms.

For HMC and all other sources, apply the same rule: verify the current upstream terms before each release, and keep attribution next to the affected config.
