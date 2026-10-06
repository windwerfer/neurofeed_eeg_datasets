# Attribution: `muse4_attention_ds001787`

This config contains **derived EEG windows** (adapted material / a derived database) produced from the sources below.
Each source keeps its own license; this card does not re-license anything. Raw recordings are **not** redistributed,
so get them from the upstream landing pages under their terms.

## EEG meditation study (OpenNeuro ds001787)

- **Version:** 1.1.1
- **Host / landing page:** https://openneuro.org/datasets/ds001787/versions/1.1.1
- **DOI:** https://doi.org/10.18112/openneuro.ds001787.v1.1.1
- **License:** `CC0-1.0` (CC0 1.0 Universal (public domain dedication), https://creativecommons.org/publicdomain/zero/1.0/)
- **Used:** ses-01 BioSemi recordings with thought-probe ratings
- **Cite:**
  - Delorme, A., & Brandmeyer, T. EEG meditation study. OpenNeuro ds001787, v1.1.1. doi:10.18112/openneuro.ds001787.v1.1.1
  - Brandmeyer, T., & Delorme, A. (2018). Reduced mind wandering in experienced meditators and associated EEG correlates. *Experimental Brain Research* 236(9):2519–2528. https://doi.org/10.1007/s00221-016-4811-5

## Changes made

- Selected EEG around answered thought probes (ses-01); dropped ties and incomplete probes.
- Resampled to 256 Hz and cut into 2-s windows (hop 0.5 s).
- Kept 4 electrodes mapped to a Muse layout (P9/P10 stand in for TP9/TP10).
- Derived binary labels from probe self-reports (Q1 vs Q2).
- Added subject-level splits and per-recording manifests.
- Removed private file-system paths from manifests and added `license_spdx` / `source_url` per recording (the window values themselves were not changed by that step).

## Notice

- CC0 sources carry no attribution requirement; citations are given as good scholarly practice.

If you publish models, papers or derived data that use these windows, cite the sources above. You may also link
this dataset (`windwerfer/neurofeed-eeg-windows`, config `muse4_attention_ds001787`, with the revision you used). The upstream authors
and hosts do not endorse this derived dataset.
