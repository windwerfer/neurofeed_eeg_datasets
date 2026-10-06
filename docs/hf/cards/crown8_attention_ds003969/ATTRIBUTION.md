# Attribution: `crown8_attention_ds003969`

This config contains **derived EEG windows** (adapted material / a derived database) produced from the sources below.
Each source keeps its own license; this card does not re-license anything. Raw recordings are **not** redistributed,
so get them from the upstream landing pages under their terms.

## Meditation vs thinking task (OpenNeuro ds003969)

- **Version:** 1.0.0
- **Host / landing page:** https://openneuro.org/datasets/ds003969/versions/1.0.0
- **DOI:** https://doi.org/10.18112/openneuro.ds003969.v1.0.0
- **License:** `CC0-1.0` (CC0 1.0 Universal (public domain dedication), https://creativecommons.org/publicdomain/zero/1.0/)
- **Used:** med1breath and think1 blocks
- **Cite:**
  - Delorme, A., & Braboszcz, C. Meditation vs thinking task. OpenNeuro ds003969, v1.0.0. doi:10.18112/openneuro.ds003969.v1.0.0
  - Braboszcz, C., Cahn, B. R., Levy, J., Fernandez, M., & Delorme, A. (2017). Increased gamma brainwave amplitude compared to control in three different meditation traditions. *PLoS ONE* 12(1):e0170647. https://doi.org/10.1371/journal.pone.0170647

## Changes made

- Selected the med1breath and think1 blocks; trimmed 30 s at block edges; capped 400 windows per block.
- Resampled to 256 Hz and cut into 2-s windows (hop 1.0 s).
- Kept the 8 Crown-position electrodes in Crown stream order.
- Assigned block-level labels (meditation → `concentration`, thinking → `mind_wandering`).
- Added subject-level splits and per-recording manifests.
- Removed private file-system paths from manifests and added `license_spdx` / `source_url` per recording (the window values themselves were not changed by that step).

## Notice

- CC0 sources carry no attribution requirement; citations are given as good scholarly practice.

If you publish models, papers or derived data that use these windows, cite the sources above. You may also link
this dataset (`windwerfer/neurofeed-eeg-windows`, config `crown8_attention_ds003969`, with the revision you used). The upstream authors
and hosts do not endorse this derived dataset.
