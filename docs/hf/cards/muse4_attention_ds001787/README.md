# `muse4_attention_ds001787`

Muse4-proxy **attention / mind-wandering** windows from OpenNeuro ds001787 with rare **thought-probe** labels. Published as an **honest negative benchmark**: frozen-encoder subject-held-out scores are near chance.

| | |
|---|---|
| **Config** | `muse4_attention_ds001787` |
| **Montage** | `muse4` **proxy**: AF7, AF8 native; TP9/TP10 ← P9/P10 (BioSemi-64 has no TP9/TP10) |
| **Tensor `X`** | `(N, 4, 512)` float32: 2-s windows at 256 Hz, channel order `AF7, AF8, TP9, TP10` |
| **Labels (`y` → `label_names`)** | `concentration` (0) / `mind_wandering` (1), from **thought-probe self-reports** (Q1 vs Q2) |
| **Subjects** | **16** · train/val/test **12 / 2 / 2** (frozen val = sub-006, sub-015; test = sub-019, sub-013) |
| **Windows** | **5,185** (concentration 3,145 · mind_wandering 2,040) |
| **Scale** | volts (raw), unfiltered |
| **Source license(s)** | [CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/) |
| **Status** | Research / negative-result data (`ship_candidate: false`) |

## Sources and licenses

| Source | Version | License (SPDX) | Link |
|---|---|---|---|
| EEG meditation study (OpenNeuro ds001787) | 1.1.1 | `CC0-1.0` | [OpenNeuro](https://openneuro.org/datasets/ds001787/versions/1.1.1) |

Full citations, license notices and the list of changes made: [`ATTRIBUTION.md`](ATTRIBUTION.md).
Per-recording `license_spdx`, `source_dataset` and `source_url` are also stored in every manifest.

## How the windows were made

1. ds001787 ses-01 BioSemi-64 BDF + events + probe log files (OpenNeuro v1.1.1).
2. Channels: AF7, AF8 native; TP9/TP10 ← P9/P10 (BioSemi-64 has no TP9/TP10)
3. Resampled to 256 Hz. **No band-pass, no re-referencing.** Stored in **volts**.
4. For each answered thought probe, 2-s windows (hop 0.5 s) from the ~10 s before the Q1 prompt.
5. Label from the probe answers: Q1 > Q2 → `concentration`, Q1 < Q2 → `mind_wandering`; ties and incomplete probes dropped.

## Labels

- At each probe participants rated meditation depth (Q1, 0–3) and mind-wandering depth (Q2, 0–3). Q1 > Q2 → `concentration`, Q1 < Q2 → `mind_wandering`, ties dropped.
- Do **not** map the raw event values 2/4 directly to classes; use the probe answers.
- `probe_ids` groups the windows of one probe (they share a label; never split them).

## Splits

Subject-level, frozen: train 12, val sub-006, sub-015, test sub-019, sub-013. Frozen val/test subjects were chosen *before* the corpus was expanded and include earlier failed holdouts on purpose (honest, hard test). Treat val/test as a small spot check, and prefer LOSO across all subjects.

`crown8` sibling `crown8_attention_ds001787` uses the identical split.

Split files: `muse4_attention_ds001787/splits/`. They are frozen; published baselines use them.

## Files

```
muse4_attention_ds001787/
  README.md  ATTRIBUTION.md
  splits/    train_subjects.json val_subjects.json test_subjects.json subjects.json split_policy.json
  windows/   subXXX_ses01_windows.npz + subXXX_ses01_manifest.json
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

REPO, CFG = "windwerfer/neurofeed-eeg-windows", "muse4_attention_ds001787"
REVISION = "main"  # pin a commit hash when you report benchmark numbers

# 1) small files first: splits + manifests
root = snapshot_download(REPO, repo_type="dataset", revision=REVISION,
                         allow_patterns=[f"{CFG}/splits/*", f"{CFG}/windows/*_manifest.json"])
test_subjects = set(json.load(open(f"{root}/{CFG}/splits/test_subjects.json"))["subjects"])

# 2) fetch only the window files of that split
manifests = [json.load(open(p)) for p in sorted(glob.glob(f"{root}/{CFG}/windows/*_manifest.json"))]
files = [m["npz_path"] for m in manifests if m["subject"] in test_subjects]
root = snapshot_download(REPO, repo_type="dataset", revision=REVISION,
                         allow_patterns=[f"{CFG}/{f}" for f in files])

X, y = [], []
for f in files:
    z = np.load(f"{root}/{CFG}/{f}")
    X.append(z["X"]); y.append(z["y"])
X, y = np.concatenate(X), np.concatenate(y)  # X: (N, 4, 512), y: (N,)
label_names = [str(s) for s in z["label_names"]]  # ['concentration', 'mind_wandering']
```

## Baselines

| Encoder (frozen) | Protocol | Macro-F1 |
|---|---|---:|
| CBraMod + linear | LOSO over ds001787 + ds003969 (muse4), 77 folds | **0.361 ± 0.209** |
| REVE-base + MLP | embed-once LOSO, same 77 folds | 0.500 ± 0.144 (≈ chance) |

Chance for a balanced random predictor is about 0.50; majority-class collapse gives about 0.33–0.40.
A meditation-depth variant (Q1 ≤ 1 vs ≥ 2) is also at chance: [`docs/head_a_med_depth_smoke.md`](https://github.com/windwerfer/neurofeed_train/blob/main/docs/head_a_med_depth_smoke.md).

All baselines use frozen encoders with a small head, evaluated on held-out subjects. Full metrics:
[`neurofeed_eeg_datasets/baselines`](https://github.com/windwerfer/neurofeed_eeg_datasets/tree/main/baselines).

## Limitations

- Subject-held-out performance is **at or near chance** with frozen encoders (see Baselines). That is the main finding, and it is why these configs are research/negative-result data, not a shippable attention decoder.
- **Subject-ID collision:** ds001787 and ds003969 both use `sub-001…`. Key subjects as `<dataset>/<sub>` when combining.
- Raw-volt scale, unfiltered: normalise before training.
- Overlapping windows: split by subject only.

## Notebooks and scripts

- [`notebooks/06_reve_attention_loso.ipynb`](https://github.com/windwerfer/neurofeed_train/blob/main/notebooks/06_reve_attention_loso.ipynb): embed-once + leave-one-subject-out on the attention configs (REVE-base, bring your own weights); CBraMod twin [`scripts/loso_eval_head_a.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/loso_eval_head_a.py)
- Crown8 LOSO: [`scripts/loso_eval_head_a_crown8.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/loso_eval_head_a_crown8.py) · write-ups [`docs/loso_head_a.md`](https://github.com/windwerfer/neurofeed_train/blob/main/docs/loso_head_a.md), [`docs/crown8_attention_loso.md`](https://github.com/windwerfer/neurofeed_train/blob/main/docs/crown8_attention_loso.md), [`docs/reve_attention_loso.md`](https://github.com/windwerfer/neurofeed_train/blob/main/docs/reve_attention_loso.md)

---
Part of [`windwerfer/neurofeed-eeg-windows`](https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows) ·
packaging repo [`neurofeed_eeg_datasets`](https://github.com/windwerfer/neurofeed_eeg_datasets).
