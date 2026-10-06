# `muse4_vigilance_sleep_edf`

Muse-oriented **vigilance (drowsy-wake vs N1)** windows derived from two open PhysioNet sleep databases, remapped onto a 4-channel Muse layout (proxy). The largest open, subject-split sleep-onset corpus in a Muse channel format; also carries sleep-stage fields.

| | |
|---|---|
| **Config** | `muse4_vigilance_sleep_edf` |
| **Montage** | `muse4` **proxy** (Sleep-EDF and HMC PSG electrodes mapped to Muse positions; not Muse hardware) |
| **Tensor `X`** | `(N, 4, 512)` float32: 2-s windows at 256 Hz, channel order `AF7, AF8, TP9, TP10` |
| **Labels (`y` → `label_names`)** | `drowsy` (0) = hypnogram **W** epochs in the sleep-onset slice; `hypnagogic` (1) = **N1** epochs. `stage_raw` / `stage_coarse` per window are kept for sleep-stage work |
| **Subjects** | **124** subjects / 125 nights: 100 Sleep-EDF (78 cassette, 22 telemetry) + 24 HMC · train/val/test **86 / 19 / 19** |
| **Windows** | **519,009** (drowsy 393,616 · hypnagogic 125,393) |
| **Scale** | microvolts, band-pass 1–45 Hz |
| **Source license(s)** | [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) · [ODC-By-1.0](https://opendatacommons.org/licenses/by/1-0/) |
| **Status** | Primary Muse vigilance release (frozen CBraMod head ships on this proxy; true-Muse calibration still recommended) |

## Sources and licenses

| Source | Version | License (SPDX) | Link |
|---|---|---|---|
| Sleep-EDF Database Expanded | 1.0.0 | `ODC-By-1.0` | [PhysioNet](https://physionet.org/content/sleep-edfx/1.0.0/) |
| Haaglanden Medisch Centrum (HMC) sleep staging database | 1.1 | `CC-BY-4.0` | [PhysioNet](https://physionet.org/content/hmc-sleep-staging/1.1/) |

Full citations, license notices and the list of changes made: [`ATTRIBUTION.md`](ATTRIBUTION.md).
Per-recording `license_spdx`, `source_dataset` and `source_url` are also stored in every manifest.

## How the windows were made

1. Sleep-EDF Expanded (cassette + telemetry) and HMC v1.1 PSG + hypnograms from PhysioNet.
2. Channels: Sleep-EDF has only Fpz-Cz and Pz-Oz, so **AF7 = AF8 = Fpz-Cz** and **TP9 = TP10 = Pz-Oz** (two unique signals, each duplicated). HMC: AF7←F4-M1, AF8←C4-M1, TP9←C3-M2, TP10←O2-M1.
3. FFT band-pass 1–45 Hz and resample to 256 Hz.
4. Slice from 20 min before to 40 min after the **first N1 onset** of each night (`pre_sec`=1200, `post_sec`=2400).
5. 2-s windows, hop 0.5 s (75 % overlap), labelled by majority hypnogram stage (≥ 0.7). Only W and N1 windows are kept.
6. Stored as float32 microvolts. No per-window normalisation.

## Labels

- `y = 0 → drowsy`: window's majority stage is **Wake (W)**, inside a slice around the first N1 onset. This is wake near sleep onset, used as a *drowsy-wake* proxy. It is not a validated drowsiness rating.
- `y = 1 → hypnagogic`: majority stage **N1**.
- N2/N3/REM/unscored windows are excluded from these exports.
- `stage_raw` holds the hypnogram text and `stage_coarse` holds `wake`/`light`/`deep`/`rem`/`unknown`. Both are object arrays, so load with `allow_pickle=True`.
- A window is kept only if one stage covers ≥ 70 % of it (`majority_frac` = 0.7).

## Splits

Subject-level, frozen (`split_policy.json`): SC400 is the test anchor and SC403 the val anchor; the rest were assigned about 70/15/15 **by sorted subject id**. As a result the split is **cross-cohort**:

| Split | Subjects | Composition |
|---|---:|---|
| train | 86 | 76 Sleep-EDF cassette + 10 HMC |
| val | 19 | 14 HMC + 4 Sleep-EDF telemetry + 1 cassette (SC403) |
| test | 19 | 18 Sleep-EDF **telemetry** + 1 cassette (SC400) |

Sleep-EDF telemetry recordings come from a study of temazepam effects on sleep (nights may be drug or placebo), so the test set is mostly a different cohort from training. **Read the published test score (0.747) as a cross-cohort number.** The split is kept frozen for comparability; no alternative split is provided.

**Do not combine with `crown2_vigilance_hmc` / `crown4_vigilance_hmc`.** The 24 HMC subjects here also appear there, and 13 of them are in a different split. If you must pool configs, use [`cross_config/vigilance_hmc_leakfree.json`](../cross_config/vigilance_hmc_leakfree.json).

Split files: `muse4_vigilance_sleep_edf/splits/`. They are frozen; published baselines use them.

## Files

```
muse4_vigilance_sleep_edf/
  README.md  ATTRIBUTION.md
  splits/    train_subjects.json val_subjects.json test_subjects.json subjects.json split_policy.json
  windows/   <recording>_windows.npz + <recording>_manifest.json (SC4xxx, ST7xxx, SNxxx); 6× <recording>_qc.npz
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

REPO, CFG = "windwerfer/neurofeed-eeg-windows", "muse4_vigilance_sleep_edf"
REVISION = "main"  # pin a commit hash when you report benchmark numbers

# 1) small files first: splits + manifests
root = snapshot_download(REPO, repo_type="dataset", revision=REVISION,
                         allow_patterns=[f"{CFG}/splits/*", f"{CFG}/windows/*_manifest.json"])
test_subjects = set(json.load(open(f"{root}/{CFG}/splits/test_subjects.json"))["subjects"])

# 2) fetch only the window files of that split
manifests = [json.load(open(p)) for p in sorted(glob.glob(f"{root}/{CFG}/windows/*_manifest.json"))]
files = [m["npz_path"] for m in manifests if m["subject_id"] in test_subjects]
root = snapshot_download(REPO, repo_type="dataset", revision=REVISION,
                         allow_patterns=[f"{CFG}/{f}" for f in files])

X, y = [], []
for f in files:
    z = np.load(f"{root}/{CFG}/{f}", allow_pickle=True)  # stage_raw / stage_coarse are object arrays
    X.append(z["X"]); y.append(z["y"])
X, y = np.concatenate(X), np.concatenate(y)  # X: (N, 4, 512), y: (N,)
label_names = [str(s) for s in z["label_names"]]  # ['drowsy', 'hypnagogic']
```

## Baselines

| Encoder (frozen) | Task | Test macro-F1 |
|---|---|---:|
| CBraMod + linear head | drowsy vs hypnagogic | **0.747** (cross-cohort test, see Splits) |
| CBraMod + linear head | `stage_coarse` wake vs light (probe) | 0.760 |

All baselines use frozen encoders with a small head, evaluated on held-out subjects. Full metrics:
[`neurofeed_eeg_datasets/baselines`](https://github.com/windwerfer/neurofeed_eeg_datasets/tree/main/baselines).

## Limitations

- **Proxy montage.** These are PSG electrodes, not Muse dry electrodes. Sleep-EDF rows contain only two unique signals (duplicated), and HMC rows use mastoid-referenced F4/C4/C3/O2.
- **Cross-cohort split.** Test is mostly the Sleep-EDF telemetry cohort (temazepam study); see Splits.
- **Overlapping windows.** Hop 0.5 s gives 75 % overlap. Never split by window; always split by subject.
- **Class imbalance** (about 3:1 drowsy:hypnagogic). Report macro-F1 or balanced accuracy.
- `drowsy` means W near sleep onset, not a behavioural drowsiness score. Not for clinical use or diagnosis.
- Overlaps with the crown vigilance configs (the same 24 HMC subjects, different splits).

## Notebooks and scripts

- Training (frozen CBraMod, A-vig + stage probe): [`scripts/train_heads_expanded_sleep_corpus.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/train_heads_expanded_sleep_corpus.py)
- Window export: [`scripts/expand_head_c_sleep_corpus.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/expand_head_c_sleep_corpus.py), [`scripts/expand_head_c_hmc.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/expand_head_c_hmc.py) (need raw PhysioNet data)
- REVE HMC paper compare (5-stage, raw HMC 30-s epochs): [`docs/reve_hmc_paper_compare_gap.md`](https://github.com/windwerfer/neurofeed_train/blob/main/docs/reve_hmc_paper_compare_gap.md) + [`scripts/reve_hmc_paper_compare.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/reve_hmc_paper_compare.py) (needs raw HMC from PhysioNet)
- Head packs: [`neurofeed_heads`](https://github.com/windwerfer/neurofeed_heads)

---
Part of [`windwerfer/neurofeed-eeg-windows`](https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows) ·
packaging repo [`neurofeed_eeg_datasets`](https://github.com/windwerfer/neurofeed_eeg_datasets).
