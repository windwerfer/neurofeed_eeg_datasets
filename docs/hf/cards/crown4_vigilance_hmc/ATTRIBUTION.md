# Attribution: `crown4_vigilance_hmc`

This config contains **derived EEG windows** (adapted material / a derived database) produced from the sources below.
Each source keeps its own license; this card does not re-license anything. Raw recordings are **not** redistributed,
so get them from the upstream landing pages under their terms.

## Haaglanden Medisch Centrum (HMC) sleep staging database

- **Version:** 1.1
- **Host / landing page:** https://physionet.org/content/hmc-sleep-staging/1.1/
- **DOI:** https://doi.org/10.13026/t79q-fr32
- **License:** `CC-BY-4.0` (Creative Commons Attribution 4.0 International, https://creativecommons.org/licenses/by/4.0/)
- **Used:** PSG recordings SN001–SN154 (151 available)
- **Cite:**
  - Alvarez-Estevez, D., & Rijsman, R. (2022). Haaglanden Medisch Centrum sleep staging database (version 1.1). PhysioNet. https://doi.org/10.13026/t79q-fr32
  - Pollard, T., Moody, B. E., Lehman, L., Gow, B., Fernandes, C., Xie, C., Johnson, A., Mark, R. G., & Heldt, T. (2026). PhysioNet as a global platform for biomedical research. *Nature Health*. https://doi.org/10.1038/s44360-026-00096-z (the standard PhysioNet citation requested on the landing page)

## Changes made

- Selected the sleep-onset slice of each night (20 min before to 40 min after the first N1 onset).
- FFT band-pass 1–45 Hz; resampled to 256 Hz; cut into 2-s windows with 0.5-s hop.
- Re-labelled hypnogram stages: W → `drowsy`, N1 → `hypnagogic`; other stages dropped; kept `stage_raw` / `stage_coarse`.
- Kept C3-M2, C4-M1, F4-M1, O2-M1 and stored them as C3, C4, F6, PO4 (F6/PO4 are proxies).
- Added subject-level train/val/test splits and per-recording manifests.
- Removed private file-system paths from manifests and added `license_spdx` / `source_url` per recording (the window values themselves were not changed by that step).

## Notice

- CC-BY-4.0 sources: the material was adapted as described under *Changes made*, and is offered under the same upstream license terms ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)) with attribution as above. No additional restrictions are applied.

If you publish models, papers or derived data that use these windows, cite the sources above. You may also link
this dataset (`windwerfer/neurofeed-eeg-windows`, config `crown4_vigilance_hmc`, with the revision you used). The upstream authors
and hosts do not endorse this derived dataset.
