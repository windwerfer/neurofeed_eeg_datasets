# `$config`

$summary

| | |
|---|---|
| **Config** | `$config` |
| **Montage** | $montage |
| **Tensor `X`** | `$shape` float32: 2-s windows at 256 Hz, channel order `$channels` |
| **Labels (`y` → `label_names`)** | $labels |
| **Subjects** | $subjects |
| **Windows** | $windows |
| **Scale** | $scale |
| **Source license(s)** | $licenses_inline |
| **Status** | $status |

## Sources and licenses

| Source | Version | License (SPDX) | Link |
|---|---|---|---|
$sources_table

Full citations, license notices and the list of changes made: [`ATTRIBUTION.md`](ATTRIBUTION.md).
Per-recording `license_spdx`, `source_dataset` and `source_url` are also stored in every manifest.

## How the windows were made

$preprocessing

## Labels

$label_details

## Splits

$splits

Split files: `$config/splits/`. They are frozen; published baselines use them.

## Files

```
$config/
  README.md  ATTRIBUTION.md
  splits/    $split_files
  windows/   $file_pattern
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

REPO, CFG = "windwerfer/neurofeed-eeg-windows", "$config"
REVISION = "main"  # pin a commit hash when you report benchmark numbers

# 1) small files first: splits + manifests
root = snapshot_download(REPO, repo_type="dataset", revision=REVISION,
                         allow_patterns=[f"{CFG}/splits/*", f"{CFG}/windows/*_manifest.json"])
$split_load

# 2) fetch only the window files of that split
manifests = [json.load(open(p)) for p in sorted(glob.glob(f"{root}/{CFG}/windows/*_manifest.json"))]
files = [m["npz_path"] for m in manifests if m["$subject_key"] in test_subjects]
root = snapshot_download(REPO, repo_type="dataset", revision=REVISION,
                         allow_patterns=[f"{CFG}/{f}" for f in files])

X, y = [], []
for f in files:
    z = np.load(f"{root}/{CFG}/{f}"$allow_pickle
    X.append(z["X"]); y.append(z["y"])
X, y = np.concatenate(X), np.concatenate(y)  # X: $shape_n, y: (N,)
label_names = [str(s) for s in z["label_names"]]  # $label_list
```

## Baselines

$baselines

All baselines use frozen encoders with a small head, evaluated on held-out subjects. Full metrics:
[`neurofeed_eeg_datasets/baselines`](https://github.com/windwerfer/neurofeed_eeg_datasets/tree/main/baselines).

## Limitations

$limitations

## Notebooks and scripts

$notebooks

---
Part of [`windwerfer/neurofeed-eeg-windows`](https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows) ·
packaging repo [`neurofeed_eeg_datasets`](https://github.com/windwerfer/neurofeed_eeg_datasets).
