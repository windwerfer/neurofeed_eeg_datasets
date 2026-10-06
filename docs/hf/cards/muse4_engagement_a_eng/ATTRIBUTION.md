# Attribution: `muse4_engagement_a_eng`

This config contains **derived EEG windows** (adapted material / a derived database) produced from the sources below.
Each source keeps its own license; this card does not re-license anything. Raw recordings are **not** redistributed,
so get them from the upstream landing pages under their terms.

## Multimodal Cognitive Workload n-back Task, 4 Difficulties (OpenNeuro ds007169)

- **Version:** 1.0.5 (current snapshot; export snapshot not recorded)
- **Host / landing page:** https://openneuro.org/datasets/ds007169
- **DOI:** https://doi.org/10.18112/openneuro.ds007169.v1.0.5
- **License:** `CC0-1.0` (CC0 1.0 Universal (public domain dedication), https://creativecommons.org/publicdomain/zero/1.0/)
- **Used:** main-phase 1-back and 4-back blocks
- **Cite:**
  - Barras, M., & Booth, L. Multimodal Cognitive Workload n-back Task, 4 Difficulties. OpenNeuro ds007169. doi:10.18112/openneuro.ds007169.v1.0.5

## Cognitive Workload 8-level arithmetic (OpenNeuro ds007262)

- **Version:** 1.1.0 (current snapshot; export snapshot not recorded)
- **Host / landing page:** https://openneuro.org/datasets/ds007262
- **DOI:** https://doi.org/10.18112/openneuro.ds007262.v1.1.0
- **License:** `CC0-1.0` (CC0 1.0 Universal (public domain dedication), https://creativecommons.org/publicdomain/zero/1.0/)
- **Used:** main-phase trials at the lowest and highest difficulty levels
- **Cite:**
  - Barras, M., & Booth, L. Cognitive Workload 8-level arithmetic. OpenNeuro ds007262. doi:10.18112/openneuro.ds007262.v1.1.0

## Multimodal dataset from the CMx7-MM Experiment (OpenNeuro ds007554)

- **Version:** 1.0.0
- **Host / landing page:** https://openneuro.org/datasets/ds007554
- **DOI:** https://doi.org/10.18112/openneuro.ds007554.v1.0.0
- **License:** `CC0-1.0` (CC0 1.0 Universal (public domain dedication), https://creativecommons.org/publicdomain/zero/1.0/)
- **Used:** ses-01 passive-motor and n-back/arithmetic tasks
- **Cite:**
  - Ajra, Z., Vergotte, G., Perrey, S., Evra, L., Pla, S., Dray, G., Montmain, J., & Xu, B. Multimodal dataset from the CMx7-MM Experiment. OpenNeuro ds007554, v1.0.0. doi:10.18112/openneuro.ds007554.v1.0.0

## EEG During Mental Arithmetic Tasks (PhysioNet eegmat)

- **Version:** 1.0.0
- **Host / landing page:** https://physionet.org/content/eegmat/1.0.0/
- **DOI:** https://doi.org/10.13026/C2JQ1P
- **License:** `ODC-By-1.0` (Open Data Commons Attribution License v1.0, https://opendatacommons.org/licenses/by/1-0/)
- **Used:** rest (_1) and mental-arithmetic (_2) recordings
- **Cite:**
  - Zyma, I., Tukaev, S., Seleznov, I., Kiyono, K., Popov, A., Chernykh, M., & Shpenkov, O. (2019). Electroencephalograms during Mental Arithmetic Task Performance. *Data* 4(1):14. https://doi.org/10.3390/data4010014
  - Pollard, T., Moody, B. E., Lehman, L., Gow, B., Fernandes, C., Xie, C., Johnson, A., Mark, R. G., & Heldt, T. (2026). PhysioNet as a global platform for biomedical research. *Nature Health*. https://doi.org/10.1038/s44360-026-00096-z (the standard PhysioNet citation requested on the landing page)

## STEW: Simultaneous Task EEG Workload (processed MONSTER mirror)

- **Version:** monster-monash/STEW (Hugging Face)
- **Host / landing page:** https://huggingface.co/datasets/monster-monash/STEW
- **License:** `CC-BY-4.0` (Creative Commons Attribution 4.0 International, https://creativecommons.org/licenses/by/4.0/)
- **Used:** processed 2-s / 128 Hz segments of the 48 participants
- **Cite:**
  - Lim, W. L., Sourina, O., & Wang, L. (2018). STEW: Simultaneous Task EEG Workload Data Set. *IEEE Transactions on Neural Systems and Rehabilitation Engineering* 26(11):2106–2114. https://doi.org/10.1109/TNSRE.2018.2872924
  - Lim, W. L., Sourina, O., & Wang, L. (2020). STEW: Simultaneous task EEG workload data set. IEEE DataPort. https://ieee-dataport.org/open-access/stew-simultaneous-task-eeg-workload-dataset (CC BY 4.0)
  - Dempster, A., et al. (2025). MONSTER: Monash Scalable Time Series Evaluation Repository. arXiv:2502.15122

## Changes made

- Selected two task conditions per source and mapped them to low/high engagement (see table).
- Mapped four electrodes per source onto a Muse layout (AF7, AF8, TP9, TP10).
- Resampled to 256 Hz (STEW: upsampled from 128 Hz) and cut into 2-s windows (hop 1.0 s).
- Z-scored per channel (STEW: per window) and clipped at ±15.
- Added person-wise splits (shared Barras participants kept together) and per-pack manifests.
- Removed private file-system paths from manifests and added `license_spdx` / `source_url` per recording (the window values themselves were not changed by that step).

## Notice

- CC-BY-4.0 sources: the material was adapted as described under *Changes made*, and is offered under the same upstream license terms ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)) with attribution as above. No additional restrictions are applied.
- CC0 sources carry no attribution requirement; citations are given as good scholarly practice.
- ODC-By-1.0 sources: this is a derived database. Under ODC-By 1.0 any public use must keep the attribution notices above.

If you publish models, papers or derived data that use these windows, cite the sources above. You may also link
this dataset (`windwerfer/neurofeed-eeg-windows`, config `muse4_engagement_a_eng`, with the revision you used). The upstream authors
and hosts do not endorse this derived dataset.
