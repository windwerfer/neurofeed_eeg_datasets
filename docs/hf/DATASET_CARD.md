---
license: other
license_name: mixed-upstream-cc0-odc-by-cc-by
license_link: https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows/blob/main/LICENSES.md
pretty_name: Neurofeed EEG Windows
task_categories:
  - other
tags:
  - eeg
  - electroencephalography
  - muse
  - neurosity-crown
  - bci
  - time-series
  - sleep
  - vigilance
  - drowsiness
  - attention
  - mind-wandering
  - engagement
  - negative-results
size_categories:
  - 1M<n<10M
viewer: false
configs:
  - config_name: muse4_vigilance_sleep_edf
    data_files: "muse4_vigilance_sleep_edf/windows/*_windows.npz"
  - config_name: crown2_vigilance_hmc
    data_files: "crown2_vigilance_hmc/windows/*_windows.npz"
  - config_name: crown4_vigilance_hmc
    data_files: "crown4_vigilance_hmc/windows/*_windows.npz"
  - config_name: muse4_attention_ds001787
    data_files: "muse4_attention_ds001787/windows/*_windows.npz"
  - config_name: muse4_attention_ds003969
    data_files: "muse4_attention_ds003969/windows/*_windows.npz"
  - config_name: crown8_attention_ds001787
    data_files: "crown8_attention_ds001787/windows/*_windows.npz"
  - config_name: crown8_attention_ds003969
    data_files: "crown8_attention_ds003969/windows/*_windows.npz"
  - config_name: muse4_engagement_a_eng
    data_files: "muse4_engagement_a_eng/windows/*_windows.npz"
---

# Neurofeed EEG Windows

Ready-to-train **2-second, 256 Hz EEG windows** derived from open EEG/PSG datasets and remapped onto consumer-headset
layouts: **Muse** (AF7, AF8, TP9, TP10) and **Neurosity Crown** (C3/C4-centred). Every config ships fixed
**subject-level splits**, per-recording manifests with **per-source license and upstream URL**, frozen-encoder
**baselines**, and honest **negative results**.

- About 1.56 M windows in 8 configs, all from open sources (CC0-1.0, ODC-By-1.0, CC-BY-4.0).
- Derived data only: no raw EDF/BDF, no gated or non-commercial sources, no model weights.
- This is **proxy** data: PSG and research-cap electrodes mapped to headset positions, not recordings from Muse or Crown hardware.

## Configs

| Config | Montage, `X` shape | Labels | Subjects (train/val/test) | Windows | Source license(s) | Frozen baseline (test macro-F1) | Status |
|---|---|---|---|---:|---|---|---|
| [`muse4_vigilance_sleep_edf`](muse4_vigilance_sleep_edf/README.md) | Muse4 proxy `(N,4,512)` | drowsy-wake (W) / hypnagogic (N1) + `stage_raw`/`stage_coarse` | 124 (86/19/19) | 519,009 | ODC-By-1.0 + CC-BY-4.0 | CBraMod **0.747** (cross-cohort test) | primary Muse vigilance release |
| [`crown2_vigilance_hmc`](crown2_vigilance_hmc/README.md) | Crown2 C3,C4 `(N,2,512)` | W / N1 | 151 (106/23/22) | 459,438 | CC-BY-4.0 | CBraMod **0.670** · REVE 0.649 | Crown vigilance ship candidate |
| [`crown4_vigilance_hmc`](crown4_vigilance_hmc/README.md) | Crown4 proxy C3,C4,F6≈F4,PO4≈O2 `(N,4,512)` | W / N1 | 151 (106/23/22) | 459,438 | CC-BY-4.0 | CBraMod **0.680** · REVE 0.681 | Crown vigilance ship candidate |
| [`muse4_attention_ds001787`](muse4_attention_ds001787/README.md) | Muse4 proxy `(N,4,512)` | concentration / mind-wandering (thought probes) | 16 (12/2/2) | 5,185 | CC0-1.0 | LOSO 0.361 (≈ chance) | research, negative result |
| [`muse4_attention_ds003969`](muse4_attention_ds003969/README.md) | Muse4 proxy `(N,4,512)` | meditation / thinking block (protocol proxy) | 64 (60/2/2) | 51,200 | CC0-1.0 | LOSO 0.361 (≈ chance) | research, negative result |
| [`crown8_attention_ds001787`](crown8_attention_ds001787/README.md) | Crown8 `(N,8,512)` | as muse4 sibling (same windows) | 16 (12/2/2) | 5,185 | CC0-1.0 | LOSO 0.351 (≈ chance) | research, negative result |
| [`crown8_attention_ds003969`](crown8_attention_ds003969/README.md) | Crown8 `(N,8,512)` | as muse4 sibling (same windows) | 64 (60/2/2) | 51,200 | CC0-1.0 | LOSO 0.351 (≈ chance) | research, negative result |
| [`muse4_engagement_a_eng`](muse4_engagement_a_eng/README.md) | Muse4 proxy `(N,4,512)` | low / high engagement (5 sources) | 133 persons (93/20/20) | 19,706 | CC0-1.0 + ODC-By-1.0 + CC-BY-4.0 | CBraMod 0.548 · REVE 0.590 | research, confound benchmark |

Each config folder has its own card (`README.md`, with montage, preprocessing, label rules, splits, baselines,
limitations and a load snippet) and `ATTRIBUTION.md` (citations, license notice, changes made).

**Channel orders.** Muse4 `AF7, AF8, TP9, TP10` · Crown2 `C3, C4` · Crown4 `C3, C4, F6, PO4` ·
Crown8 `CP3, C3, F5, PO3, PO4, F6, C4, CP4`. Never mix montages in one example. Details in
[`schemas/montages.json`](schemas/montages.json).

## How to load

The windows are NumPy `.npz` files (`X`, `y`, `starts`, `label_names`, plus optional keys). `datasets.load_dataset` and
the dataset viewer are not supported, so use `huggingface_hub` + NumPy:

```python
# uv add huggingface_hub numpy
import json, numpy as np
from huggingface_hub import hf_hub_download

REPO = "windwerfer/neurofeed-eeg-windows"
path = hf_hub_download(REPO, "crown2_vigilance_hmc/windows/SN001_windows.npz", repo_type="dataset")
z = np.load(path, allow_pickle=True)   # allow_pickle only for stage_raw / stage_coarse (vigilance configs)
X, y = z["X"], z["y"]                  # X: (N, 2, 512) float32, y: (N,) int64
print([str(s) for s in z["label_names"]], X.shape)

man = json.load(open(hf_hub_download(REPO, "crown2_vigilance_hmc/windows/SN001_manifest.json", repo_type="dataset")))
print(man["subject_id"], man["license_spdx"], man["source_url"])
```

Each config card has a full snippet that downloads only one split (manifests → subject ids → `.npz` files). Pin a
commit hash (`revision=`) when you report numbers. Schema: [`schemas/schema_windows.md`](schemas/schema_windows.md),
manifest fields: [`schemas/manifest_fields.md`](schemas/manifest_fields.md).

**Scale differs by config.** Vigilance configs are band-passed microvolts, attention configs are raw volts, and A-eng is
z-scored. Normalise before mixing.

## Splits and combining configs

- Every config has frozen subject-level splits in `<config>/splits/`. No subject is in two splits *within* a config.
  Windows overlap in time, so always split by subject, never by window.
- **Do not combine `muse4_vigilance_sleep_edf` with `crown2_vigilance_hmc` / `crown4_vigilance_hmc`.** The 24 HMC
  subjects of the muse4 config also appear in the crown configs, and 13 of them sit in a different split. If you must pool
  them, use the leak-free union split in [`cross_config/vigilance_hmc_leakfree.json`](cross_config/vigilance_hmc_leakfree.json).
  Results under that split are not comparable to the per-config baselines.
- **Muse4 vigilance test is cross-cohort.** Test is 18 Sleep-EDF telemetry subjects (a temazepam study) + SC400, and val
  is mostly HMC, so the 0.747 is a cross-cohort score. The split stays frozen for comparability.
- **Attention subject IDs collide:** ds001787 and ds003969 both use `sub-001…`, so key subjects as `<dataset>/<sub>`.

## Baselines and negative results

All numbers use **frozen** encoders (CBraMod, or REVE-base where noted) with a small head on held-out subjects.
Full metrics JSON (per class, per fold, confusion matrices):
[`neurofeed_eeg_datasets/baselines`](https://github.com/windwerfer/neurofeed_eeg_datasets/tree/main/baselines).

- **Works:** sleep-onset vigilance (W vs N1) transfers to headset-like channel sets: Muse4 proxy 0.747, Crown2 0.670,
  Crown4 0.680. REVE-base reproduces the published HMC 5-stage linear probe (balanced accuracy 0.649 vs paper 0.647).
- **Does not work (published on purpose):** attention / mind-wandering from 4 or 8 channels across subjects is at chance
  (LOSO 0.36 CBraMod, 0.50 REVE; random ≈ 0.50, collapse ≈ 0.33–0.40). Engagement looks better than it is because of
  task-order confounds (0.55–0.59). Rest vs meditation (ds003816), meditation depth and EEGMAT stress vs calm smokes are also at chance; see the
  [training-lab docs](https://github.com/windwerfer/neurofeed_train/tree/main/docs).

## Notebooks and scripts

Code lives in the public training lab [`neurofeed_train`](https://github.com/windwerfer/neurofeed_train):

- **Crown vigilance, CBraMod:** [`kaggle_kernel_10_hmc_crown_vig`](https://github.com/windwerfer/neurofeed_train/tree/main/kaggle_kernel_10_hmc_crown_vig). Retrain from these windows; also a minimal CBraMod-loading example.
- **Crown vigilance, REVE-base (experimental):** [`kaggle_kernel_11_hmc_crown_vig_reve`](https://github.com/windwerfer/neurofeed_train/tree/main/kaggle_kernel_11_hmc_crown_vig_reve). Bring your own gated REVE weights.
- **Embed-once + LOSO:** [`notebooks/06_reve_attention_loso.ipynb`](https://github.com/windwerfer/neurofeed_train/blob/main/notebooks/06_reve_attention_loso.ipynb) (REVE) and [`scripts/loso_eval_head_a.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/loso_eval_head_a.py) (CBraMod), on the attention configs.
- **HMC paper compare (5-stage, raw HMC):** [`docs/reve_hmc_paper_compare_gap.md`](https://github.com/windwerfer/neurofeed_train/blob/main/docs/reve_hmc_paper_compare_gap.md) + [`scripts/reve_hmc_paper_compare.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/reve_hmc_paper_compare.py).
- Trained head packs: [`neurofeed_heads`](https://github.com/windwerfer/neurofeed_heads).

Encoders are not included here. CBraMod is Apache-2.0; REVE-base is gated, so users fetch it under its own terms.

## Licenses and attribution

This repository is **not** under a single license. Each config keeps the license(s) of its upstream source(s); see
[`LICENSES.md`](LICENSES.md) and each config's `ATTRIBUTION.md` (citations, license notice, list of changes made).
Every manifest also carries `license_spdx`, `source_dataset` and `source_url`.

| Config | Upstream | SPDX |
|---|---|---|
| `muse4_vigilance_sleep_edf` | PhysioNet Sleep-EDF Expanded 1.0.0; PhysioNet HMC 1.1 | `ODC-By-1.0`; `CC-BY-4.0` |
| `crown2_vigilance_hmc`, `crown4_vigilance_hmc` | PhysioNet HMC 1.1 | `CC-BY-4.0` |
| `muse4_attention_ds001787`, `crown8_attention_ds001787` | OpenNeuro ds001787 1.1.1 | `CC0-1.0` |
| `muse4_attention_ds003969`, `crown8_attention_ds003969` | OpenNeuro ds003969 1.0.0 | `CC0-1.0` |
| `muse4_engagement_a_eng` | OpenNeuro ds007169, ds007262, ds007554; PhysioNet EEGMAT 1.0.0; STEW (processed MONSTER mirror) | `CC0-1.0`; `ODC-By-1.0`; `CC-BY-4.0` |

Cite the upstream sources when you use these windows. The upstream authors do not endorse this derived dataset.

## Not included

- Raw EDF/BDF/PSG recordings (get them from PhysioNet / OpenNeuro under their terms).
- Non-commercial, academic-only or gated datasets.
- Model weights or embedding caches (including gated REVE base/positions), private caches, credentials.
- Any claim that proxy labels are native Muse/Crown labels, clinical truth or a validated psychological state.

## Changelog

- **cards-v1** (staged for review): per-config cards and ATTRIBUTION (citations, SPDX, changes made, load snippets),
  manifests scrubbed (portable paths, `license_spdx` + `source_url`), schema docs, cross-config leak-free vigilance split,
  YAML (`viewer: false`, `data_files`, size category, `license_link` → `LICENSES.md`). Window `.npz` files unchanged.
- 2026-09-23: added `crown2_vigilance_hmc`, `crown4_vigilance_hmc`.
- 2026-09-23: initial Muse4 / Crown8 release.

Packaging, schemas and split JSON: [`neurofeed_eeg_datasets`](https://github.com/windwerfer/neurofeed_eeg_datasets).
