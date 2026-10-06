# Licenses: `windwerfer/neurofeed-eeg-windows`

This dataset is a collection of **derived EEG windows**. It has **no single license**: each config keeps the license(s)
of the upstream source(s) it was derived from. Nothing here re-licenses upstream material, and the Apache-2.0 license
of the GitHub packaging repo (`neurofeed_eeg_datasets`, scripts and docs) does **not** apply to the window data.

| Config | Upstream source(s) | SPDX | License text |
|---|---|---|---|
| `muse4_vigilance_sleep_edf` | Sleep-EDF Database Expanded 1.0.0 (PhysioNet) | `ODC-By-1.0` | https://opendatacommons.org/licenses/by/1-0/ |
| | HMC sleep staging database 1.1 (PhysioNet) | `CC-BY-4.0` | https://creativecommons.org/licenses/by/4.0/ |
| `crown2_vigilance_hmc` | HMC sleep staging database 1.1 (PhysioNet) | `CC-BY-4.0` | https://creativecommons.org/licenses/by/4.0/ |
| `crown4_vigilance_hmc` | HMC sleep staging database 1.1 (PhysioNet) | `CC-BY-4.0` | https://creativecommons.org/licenses/by/4.0/ |
| `muse4_attention_ds001787` / `crown8_attention_ds001787` | OpenNeuro ds001787 1.1.1 | `CC0-1.0` | https://creativecommons.org/publicdomain/zero/1.0/ |
| `muse4_attention_ds003969` / `crown8_attention_ds003969` | OpenNeuro ds003969 1.0.0 | `CC0-1.0` | https://creativecommons.org/publicdomain/zero/1.0/ |
| `muse4_engagement_a_eng` | OpenNeuro ds007169, ds007262, ds007554 | `CC0-1.0` | https://creativecommons.org/publicdomain/zero/1.0/ |
| | PhysioNet EEG During Mental Arithmetic Tasks (eegmat) 1.0.0 | `ODC-By-1.0` | https://opendatacommons.org/licenses/by/1-0/ |
| | STEW, processed MONSTER mirror (`monster-monash/STEW`) | `CC-BY-4.0` | https://creativecommons.org/licenses/by/4.0/ |

Per-recording `license_spdx` is stored in every manifest (`<config>/windows/*_manifest.json`).
Citations and the list of changes made (as CC BY 4.0 and ODC-By 1.0 require) are in each config's `ATTRIBUTION.md`.

Licenses were checked against the upstream landing pages on 2026-10-06. If an upstream license changes, the upstream
terms take precedence for that source's derived windows.

The small JSON/Markdown metadata written for this repo (cards, split files, schemas) is offered under Apache-2.0,
matching the packaging repo.
