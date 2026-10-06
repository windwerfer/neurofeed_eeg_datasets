# Window NPZ and manifest schema

Applies to every config of [`windwerfer/neurofeed-eeg-windows`](https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows).
One recording (night, session or subject pack) gives one `<stem>_windows.npz` plus one `<stem>_manifest.json` under
`<config>/windows/`. Some configs also ship `<stem>_qc.npz` (light artifact-QC flags).

## Required NPZ keys (all configs)

| Key | Shape / dtype | Notes |
|-----|---------------|-------|
| `X` | `(N, C, 512)` float32 | 2-s windows at 256 Hz. `C` and channel order come from the config's montage (table below) |
| `y` | `(N,)` int64 | Index into `label_names` |
| `starts` | `(N,)` int64 | Window start sample (256 Hz) within the exported slice or recording |
| `label_names` | `(K,)` str | Class names for this file, in index order |

`C` per montage (see `montages.json`; never mix montages in one example or one model input):

| Montage id | C | Channel order in `X` | Configs |
|---|---:|---|---|
| `muse4` (proxy) | 4 | `AF7, AF8, TP9, TP10` | `muse4_*` |
| `crown2_strong` | 2 | `C3, C4` | `crown2_vigilance_hmc` |
| `crown4_hmc` (proxy) | 4 | `C3, C4, F6, PO4` (F6≈F4, PO4≈O2) | `crown4_vigilance_hmc` |
| `crown8` | 8 | `CP3, C3, F5, PO3, PO4, F6, C4, CP4` | `crown8_attention_*` |

Muse4 model order (`AF7, AF8, TP9, TP10`) is not the Muse stream order (`TP9, AF7, AF8, TP10`); see `montages.json`.

## Optional NPZ keys

| Key | Configs | Notes |
|-----|---------|-------|
| `stage_raw` | vigilance (`muse4_vigilance_sleep_edf`, `crown*_vigilance_hmc`) | `(N,)` **object** array of hypnogram text (`Sleep stage W`, `Sleep stage 1`, …). Load with `np.load(..., allow_pickle=True)` |
| `stage_coarse` | vigilance | `(N,)` object: `wake` / `light` / `deep` / `rem` / `unknown` (map in `label_maps.json`) |
| `ch_names` / `channels` | crown vigilance / attention | Channel names, same order as `X` |
| `probe_ids` | `*_attention_ds001787` | Thought-probe index per window |
| `task_ids`, `task_names` | `*_attention_ds003969` | Protocol block per window |
| `montage_id` | `crown8_attention_*` | `crown8` |

## Units and scale (not harmonised across configs)

| Config(s) | Stored scale | Filtering |
|---|---|---|
| `muse4_vigilance_sleep_edf`, `crown*_vigilance_hmc` | microvolts | FFT band-pass 1–45 Hz, then resampled to 256 Hz |
| `muse4_attention_*`, `crown8_attention_*` | volts (raw BioSemi, no re-reference) | resample only, no band-pass |
| `muse4_engagement_a_eng` | dimensionless z-scores, clipped at ±15 | per channel (per window for STEW); see manifest `scale_note` |

Normalise per window/channel (or match your encoder's expected input) before mixing configs.

## Manifests

See [`manifest_fields.md`](manifest_fields.md). Manifests are the authority for provenance, label rule, per-label
counts, source license (`license_spdx`), upstream URL (`source_url`) and the window file checksum (`npz_sha256`,
equal to the Hub LFS sha256 of the `.npz`).

## Splits

Fixed subject-level JSON per config under `<config>/splits/` (`train_subjects.json`, `val_subjects.json`,
`test_subjects.json`, `split_policy.json`; `muse4_engagement_a_eng` uses one `splits.json` keyed by
`unique_person_id`). No subject appears in more than one split *within a config*. Splits are **not**
aligned across configs; see `cross_config/vigilance_hmc_leakfree.json` before combining vigilance configs.

## Label maps

`label_maps.json`: Head A vigilance (`Sleep stage W → drowsy`, `Sleep stage 1 / N1 → hypnagogic`, other stages excluded
from the N1-slice exports), attention (`concentration` / `mind_wandering`), engagement (`low_engagement` /
`high_engagement`), and the `stage_raw → stage_coarse` map.
