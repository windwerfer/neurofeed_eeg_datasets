# `crown8_attention_ds003969`

Crown8-layout **attention / mind-wandering** windows from OpenNeuro ds003969 (breath meditation vs instructed thinking blocks). Published as an **honest negative benchmark**: frozen-encoder subject-held-out scores are near chance.

| | |
|---|---|
| **Config** | `crown8_attention_ds003969` |
| **Montage** | `crown8`: CP3, C3, F5, PO3, PO4, F6, C4, CP4 (native 10-10 electrodes from the 64-ch cap; Crown positions, not Crown hardware) |
| **Tensor `X`** | `(N, 8, 512)` float32: 2-s windows at 256 Hz, channel order `CP3, C3, F5, PO3, PO4, F6, C4, CP4` |
| **Labels (`y` → `label_names`)** | `concentration` (0) = breath-meditation block / `mind_wandering` (1) = instructed-thinking block (**protocol proxy**) |
| **Subjects** | **64** · train/val/test **60 / 2 / 2** (frozen val = sub-026, sub-028; test = sub-025, sub-027) |
| **Windows** | **51,200** (concentration 25,600 · mind_wandering 25,600) |
| **Scale** | volts (raw), unfiltered |
| **Source license(s)** | [CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/) |
| **Status** | Research / negative-result data (`ship_candidate: false`) |

## Sources and licenses

| Source | Version | License (SPDX) | Link |
|---|---|---|---|
| Meditation vs thinking task (OpenNeuro ds003969) | 1.0.0 | `CC0-1.0` | [OpenNeuro](https://openneuro.org/datasets/ds003969/versions/1.0.0) |

Full citations, license notices and the list of changes made: [`ATTRIBUTION.md`](ATTRIBUTION.md).
Per-recording `license_spdx`, `source_dataset` and `source_url` are also stored in every manifest.

## How the windows were made

1. ds003969 BDF recordings of the `med1breath` (breath meditation) and `think1` (instructed thinking) blocks (OpenNeuro v1.0.0, 1024 Hz).
2. Channels: BioSemi A/B labels → 10-10 names; picked the 8 Crown positions in Crown stream order. Windows are aligned 1:1 with `muse4_attention_ds003969` (same `starts` and `y`).
3. Resampled to 256 Hz. **No band-pass, no re-referencing.** Stored in **volts**.
4. Trimmed 30 s at block edges; 2-s windows, hop 1.0 s; capped at 400 windows per block (800 per subject, balanced).
5. Block label: `med*` → `concentration`, `think*` → `mind_wandering` (protocol proxy).

## Labels

- Labels are **block-level protocol labels**, not self-reports. Instructed thinking is not spontaneous mind-wandering, so treat `mind_wandering` here as `think_block`.
- `task_ids` / `task_names` hold the block per window.

## Splits

Subject-level, frozen: train 60, val sub-026, sub-028, test sub-025, sub-027. Frozen val/test subjects were chosen *before* the corpus was expanded and include earlier failed holdouts on purpose (honest, hard test). Treat val/test as a small spot check, and prefer LOSO across all subjects.

`muse4` sibling `muse4_attention_ds003969` uses the identical split.

Split files: `crown8_attention_ds003969/splits/`. They are frozen; published baselines use them.

## Files

```
crown8_attention_ds003969/
  README.md  ATTRIBUTION.md
  splits/    train_subjects.json val_subjects.json test_subjects.json subjects.json split_policy.json
  windows/   subXXX_windows.npz + subXXX_manifest.json
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

REPO, CFG = "windwerfer/neurofeed-eeg-windows", "crown8_attention_ds003969"
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
X, y = np.concatenate(X), np.concatenate(y)  # X: (N, 8, 512), y: (N,)
label_names = [str(s) for s in z["label_names"]]  # ['concentration', 'mind_wandering']
```

## Baselines

| Encoder (frozen) | Protocol | Macro-F1 |
|---|---|---:|
| CBraMod + linear | LOSO over crown8 ds001787 + ds003969, 67 folds | **0.351 ± 0.218** |
| CBraMod + linear (muse4 sibling, reference) | LOSO, 77 folds | 0.361 |

Chance for a balanced random predictor is about 0.50; majority-class collapse gives about 0.33–0.40.

All baselines use frozen encoders with a small head, evaluated on held-out subjects. Full metrics:
[`neurofeed_eeg_datasets/baselines`](https://github.com/windwerfer/neurofeed_eeg_datasets/tree/main/baselines).

## Limitations

- Subject-held-out performance is **at or near chance** with frozen encoders (see Baselines). That is the main finding, and it is why these configs are research/negative-result data, not a shippable attention decoder.
- **Subject-ID collision:** ds001787 and ds003969 both use `sub-001…`. Key subjects as `<dataset>/<sub>` when combining.
- Raw-volt scale, unfiltered: normalise before training.
- Overlapping windows: split by subject only.
- `mind_wandering` is an instructed-thinking block, not spontaneous mind-wandering.
- Do not mix with Muse4 configs in one example; `muse4_attention_ds003969` has the same windows on the Muse4 proxy layout.

## Notebooks and scripts

- [`notebooks/06_reve_attention_loso.ipynb`](https://github.com/windwerfer/neurofeed_train/blob/main/notebooks/06_reve_attention_loso.ipynb): embed-once + leave-one-subject-out on the attention configs (REVE-base, bring your own weights); CBraMod twin [`scripts/loso_eval_head_a.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/loso_eval_head_a.py)
- Crown8 LOSO: [`scripts/loso_eval_head_a_crown8.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/loso_eval_head_a_crown8.py) · write-ups [`docs/loso_head_a.md`](https://github.com/windwerfer/neurofeed_train/blob/main/docs/loso_head_a.md), [`docs/crown8_attention_loso.md`](https://github.com/windwerfer/neurofeed_train/blob/main/docs/crown8_attention_loso.md), [`docs/reve_attention_loso.md`](https://github.com/windwerfer/neurofeed_train/blob/main/docs/reve_attention_loso.md)

---
Part of [`windwerfer/neurofeed-eeg-windows`](https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows) ·
packaging repo [`neurofeed_eeg_datasets`](https://github.com/windwerfer/neurofeed_eeg_datasets).
