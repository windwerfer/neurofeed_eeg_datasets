# `muse4_engagement_a_eng`

Muse4-proxy **low vs high mental workload / engagement** windows pooled from five open datasets. The confounds (task order, cohort, device) are documented, so this config is a **confound benchmark**: a model that scores well here may be reading task order rather than engagement.

| | |
|---|---|
| **Config** | `muse4_engagement_a_eng` |
| **Montage** | `muse4` **proxy**: frontal/temporal electrodes of each source mapped to AF7, AF8, TP9, TP10 (see table below) |
| **Tensor `X`** | `(N, 4, 512)` float32: 2-s windows at 256 Hz, channel order `AF7, AF8, TP9, TP10` |
| **Labels (`y` → `label_names`)** | `low_engagement` (0) / `high_engagement` (1): source-specific task or rating mapping |
| **Subjects** | **133** unique persons / 150 packs · person-wise train/val/test **93 / 20 / 20** persons (104 / 23 / 23 packs) |
| **Windows** | **19,706** (low 9,528 · high 10,178) |
| **Scale** | dimensionless z-scores clipped at ±15 (per channel; STEW per window) |
| **Source license(s)** | [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) · [CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/) · [ODC-By-1.0](https://opendatacommons.org/licenses/by/1-0/) |
| **Status** | Research only, not a shipping engagement head (confounded) |

## Sources and licenses

| Source | Version | License (SPDX) | Link |
|---|---|---|---|
| Multimodal Cognitive Workload n-back Task, 4 Difficulties (OpenNeuro ds007169) | 1.0.5 (current snapshot; export snapshot not recorded) | `CC0-1.0` | [OpenNeuro](https://openneuro.org/datasets/ds007169) |
| Cognitive Workload 8-level arithmetic (OpenNeuro ds007262) | 1.1.0 (current snapshot; export snapshot not recorded) | `CC0-1.0` | [OpenNeuro](https://openneuro.org/datasets/ds007262) |
| Multimodal dataset from the CMx7-MM Experiment (OpenNeuro ds007554) | 1.0.0 | `CC0-1.0` | [OpenNeuro](https://openneuro.org/datasets/ds007554) |
| EEG During Mental Arithmetic Tasks (PhysioNet eegmat) | 1.0.0 | `ODC-By-1.0` | [PhysioNet](https://physionet.org/content/eegmat/1.0.0/) |
| STEW: Simultaneous Task EEG Workload (processed MONSTER mirror) | monster-monash/STEW (Hugging Face) | `CC-BY-4.0` | [Hugging Face (processed mirror); raw data on IEEE DataPort](https://huggingface.co/datasets/monster-monash/STEW) |

Full citations, license notices and the list of changes made: [`ATTRIBUTION.md`](ATTRIBUTION.md).
Per-recording `license_spdx`, `source_dataset` and `source_url` are also stored in every manifest.

## How the windows were made

| Source | Packs | Device / source channels | Mapped to AF7, AF8, TP9, TP10 | Low → High | Known confound |
|---|---:|---|---|---|---|
| ds007169 | 18 | 19-ch mobile EEG | F7, F8, T3, T4 | 1-back → 4-back | strict L1→L4 order |
| ds007262 | 18 | 19-ch mobile EEG (same people as ds007169) | F7, F8, T3, T4 | difficulty 0.6–1.5 → 5.1–6.9 | randomised difficulty (cleanest) |
| ds007554 | 30 | 32-ch EEG | F7, F8, T7, T8 | passive motor → n-back/arithmetic | order not fully counterbalanced |
| eegmat | 36 | 23-ch EEG | F7, F8, T3, T4 | rest → mental arithmetic | rest always first |
| STEW | 48 | 14-ch Emotiv EPOC (hobbyist) | AF3, AF4, T7, T8 | rating ≤ 4 → > 4 | rest then SIMKAP |

Each source: selected the two task conditions above → resampled to **256 Hz** → 2-s windows, hop 1.0 s → **z-scored per channel and clipped at ±15**. STEW comes from the processed MONSTER mirror as pre-segmented 2-s windows at **128 Hz**; each window was **upsampled 128 → 256 Hz** (so content stops at 64 Hz) and z-scored per window. All stored windows are 256 Hz, 512 samples.

## Labels

- Labels are task/difficulty conditions (STEW: post-task self-rating) mapped to two levels. They are **not** a validated engagement measure.
- `order_confound`, `label_rule`, `device_class` and `scale_note` are recorded per pack in the manifests.

## Splits

Person-wise, frozen (`splits/splits.json`, seed 42): 93 / 20 / 20 unique persons. ds007169 and ds007262 share participants (`unique_person_id` = `barras_sub-XXX`), so both tasks of one person stay in one split. This config has one `splits.json` (keys `splits.train|val|test` → person ids; `persons` → packs) instead of `*_subjects.json`.

Split files: `muse4_engagement_a_eng/splits/`. They are frozen; published baselines use them.

## Files

```
muse4_engagement_a_eng/
  README.md  ATTRIBUTION.md
  splits/    splits.json
  windows/   <source>_<subject>_aeng_windows.npz + _aeng_manifest.json (source ∈ ds007169, ds007262, ds007554, eegmat, stew)
```

`npz_sha256` in each manifest equals the Hub LFS sha256 of the matching `.npz`. Schema:
[`schemas/schema_windows.md`](../schemas/schema_windows.md) · fields: [`schemas/manifest_fields.md`](../schemas/manifest_fields.md).

## How to load

There is no Arrow/Parquet export and `datasets.load_dataset` does not apply. Download the `.npz` files and read them with NumPy:

```python
# uv add huggingface_hub numpy
import glob, json
import numpy as np
from huggingface_hub import snapshot_download

REPO, CFG = "windwerfer/neurofeed-eeg-windows", "muse4_engagement_a_eng"
REVISION = "main"  # pin a commit hash when you report benchmark numbers

# 1) small files first: splits + manifests
root = snapshot_download(REPO, repo_type="dataset", revision=REVISION,
                         allow_patterns=[f"{CFG}/splits/*", f"{CFG}/windows/*_manifest.json"])
test_subjects = set(json.load(open(f"{root}/{CFG}/splits/splits.json"))["splits"]["test"])  # unique_person_id

# 2) fetch only the window files of that split
manifests = [json.load(open(p)) for p in sorted(glob.glob(f"{root}/{CFG}/windows/*_manifest.json"))]
files = [m["npz_path"] for m in manifests if m["unique_person_id"] in test_subjects]
root = snapshot_download(REPO, repo_type="dataset", revision=REVISION,
                         allow_patterns=[f"{CFG}/{f}" for f in files])

X, y = [], []
for f in files:
    z = np.load(f"{root}/{CFG}/{f}")
    X.append(z["X"]); y.append(z["y"])
X, y = np.concatenate(X), np.concatenate(y)  # X: (N, 4, 512), y: (N,)
label_names = [str(s) for s in z["label_names"]]  # ['low_engagement', 'high_engagement']
```

## Baselines

| Encoder (frozen) | Test macro-F1 |
|---|---:|
| CBraMod + linear head | 0.548 |
| REVE-base + linear head | 0.590 |

Both count as a misfit given the confounds. An EEGMAT-only stress-vs-calm smoke is at chance (0.495): [`docs/head_stress_calm_smoke.md`](https://github.com/windwerfer/neurofeed_train/blob/main/docs/head_stress_calm_smoke.md).

All baselines use frozen encoders with a small head, evaluated on held-out subjects. Full metrics:
[`neurofeed_eeg_datasets/baselines`](https://github.com/windwerfer/neurofeed_eeg_datasets/tree/main/baselines).

## Limitations

- **Confounded labels:** task order (ds007169, eegmat, STEW), cohort and device type all differ across sources and classes.
- Mixed devices, including a hobbyist Emotiv headset; STEW is upsampled from 128 Hz.
- Data is z-scored, so absolute amplitude information is gone.
- Report per-source results, and prefer ds007262 (randomised difficulty) for any claim about engagement.

## Notebooks and scripts

- Training: [`scripts/train_head_a_eng_cbramod.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/train_head_a_eng_cbramod.py), [`scripts/train_head_a_eng_reve.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/train_head_a_eng_reve.py)
- Corpus build: [`scripts/expand_head_a_eng_corpus.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/expand_head_a_eng_corpus.py) · write-up [`docs/head_a_eng_dual_encoder.md`](https://github.com/windwerfer/neurofeed_train/blob/main/docs/head_a_eng_dual_encoder.md)

---
Part of [`windwerfer/neurofeed-eeg-windows`](https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows) ·
packaging repo [`neurofeed_eeg_datasets`](https://github.com/windwerfer/neurofeed_eeg_datasets).
