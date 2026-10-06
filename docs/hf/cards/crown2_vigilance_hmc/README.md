# `crown2_vigilance_hmc`

**Vigilance (drowsy-wake vs N1)** windows from the open HMC sleep database using the two **central** electrodes C3/C4. These are real C3/C4 positions, which the Neurosity Crown also has. Useful for any central-channel sleep-onset or drowsiness model.

| | |
|---|---|
| **Config** | `crown2_vigilance_hmc` |
| **Montage** | `crown2_strong`: C3, C4 (true central positions from PSG, mastoid-referenced; not Crown hardware) |
| **Tensor `X`** | `(N, 2, 512)` float32: 2-s windows at 256 Hz, channel order `C3, C4` |
| **Labels (`y` → `label_names`)** | `drowsy` (0) = hypnogram **W** epochs in the sleep-onset slice; `hypnagogic` (1) = **N1** epochs. `stage_raw` / `stage_coarse` per window are kept for sleep-stage work |
| **Subjects** | **151** HMC subjects (1 night each) · train/val/test **106 / 23 / 22** (random, seed 42; same split as `crown4_vigilance_hmc`) |
| **Windows** | **459,438** (drowsy 328,946 · hypnagogic 130,492) |
| **Scale** | microvolts, band-pass 1–45 Hz |
| **Source license(s)** | [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) |
| **Status** | Ship candidate for Crown vigilance (proxy); clears the 0.60 test macro-F1 bar |

## Sources and licenses

| Source | Version | License (SPDX) | Link |
|---|---|---|---|
| Haaglanden Medisch Centrum (HMC) sleep staging database | 1.1 | `CC-BY-4.0` | [PhysioNet](https://physionet.org/content/hmc-sleep-staging/1.1/) |

Full citations, license notices and the list of changes made: [`ATTRIBUTION.md`](ATTRIBUTION.md).
Per-recording `license_spdx`, `source_dataset` and `source_url` are also stored in every manifest.

## How the windows were made

1. HMC v1.1 PSG + hypnograms from PhysioNet (all 151 available recordings).
2. Channels: C3 ← `EEG C3-M2`, C4 ← `EEG C4-M1`. No fabricated channels.
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

Subject-level, frozen, random with seed 42: 106 / 23 / 22 subjects, identical to `crown4_vigilance_hmc`.

**Do not combine with `muse4_vigilance_sleep_edf`.** Its 24 HMC subjects are also here, and 13 of them sit in a different split. If you must pool configs, use [`cross_config/vigilance_hmc_leakfree.json`](../cross_config/vigilance_hmc_leakfree.json).

Split files: `crown2_vigilance_hmc/splits/`. They are frozen; published baselines use them.

## Files

```
crown2_vigilance_hmc/
  README.md  ATTRIBUTION.md
  splits/    train_subjects.json val_subjects.json test_subjects.json subjects.json split_policy.json
  windows/   SNxxx_windows.npz + SNxxx_manifest.json
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

REPO, CFG = "windwerfer/neurofeed-eeg-windows", "crown2_vigilance_hmc"
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
X, y = np.concatenate(X), np.concatenate(y)  # X: (N, 2, 512), y: (N,)
label_names = [str(s) for s in z["label_names"]]  # ['drowsy', 'hypnagogic']
```

## Baselines

| Encoder (frozen) | Test macro-F1 |
|---|---:|
| CBraMod + linear head | **0.670** |
| REVE-base + linear head (experimental) | 0.649 |

All baselines use frozen encoders with a small head, evaluated on held-out subjects. Full metrics:
[`neurofeed_eeg_datasets/baselines`](https://github.com/windwerfer/neurofeed_eeg_datasets/tree/main/baselines).

## Limitations

- PSG electrodes (wet, mastoid reference), not the Crown's dry electrodes or reference. Expect a domain gap on device.
- Overlapping windows (75 %): split by subject only. Class imbalance about 2.5:1.
- `drowsy` means W near sleep onset, not a behavioural drowsiness score. Not for clinical use.
- HMC-only; same subjects as `crown4_vigilance_hmc`. Do not mix with Muse4 configs.

## Notebooks and scripts

- [`kaggle_kernel_10_hmc_crown_vig`](https://github.com/windwerfer/neurofeed_train/tree/main/kaggle_kernel_10_hmc_crown_vig): frozen CBraMod Crown vigilance retrain from these windows (also a minimal CBraMod-loading example)
- [`kaggle_kernel_11_hmc_crown_vig_reve`](https://github.com/windwerfer/neurofeed_train/tree/main/kaggle_kernel_11_hmc_crown_vig_reve): same with frozen REVE-base (experimental; bring your own gated weights)
- REVE HMC paper compare (5-stage, raw HMC 30-s epochs): [`docs/reve_hmc_paper_compare_gap.md`](https://github.com/windwerfer/neurofeed_train/blob/main/docs/reve_hmc_paper_compare_gap.md) + [`scripts/reve_hmc_paper_compare.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/reve_hmc_paper_compare.py) (needs raw HMC from PhysioNet)
- Head packs: [`neurofeed_heads`](https://github.com/windwerfer/neurofeed_heads) (`packs/cbramod-a-vig-crown2-hmc`, `packs/reve-a-vig-crown2-hmc`)

---
Part of [`windwerfer/neurofeed-eeg-windows`](https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows) ·
packaging repo [`neurofeed_eeg_datasets`](https://github.com/windwerfer/neurofeed_eeg_datasets).
