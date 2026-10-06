# Scripts

Packaging helpers for the Hugging Face dataset
[`windwerfer/neurofeed-eeg-windows`](https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows).
Window binaries (`*.npz`) are never committed here; they live only on the Hub.

Use [`uv`](https://docs.astral.sh/uv/) (not pip). The scripts below use only the standard library.

## `scrub_manifests.py`: portable, license-tagged manifests

Rewrites every `<config>/windows/*_manifest.json` for public release:

- `npz_path` becomes config-relative (`windows/<file>.npz`, the name on the Hub)
- raw-source paths (`psg_path`, `hypno_path`, `bdf`, `events`, `log_file`, `per_task_bdf[].bdf`) are
  dropped or turned into upstream-relative paths (e.g. `sub-001/ses-01/eeg/…bdf`)
- adds `license_spdx`, `source_dataset`, `source_url` (upstream file or landing page) and `source_landing_page`
- removes encoder entries (CBraMod etc.) from the data `license_attribution` block
- leaves `npz_sha256` untouched; `.npz` files are not modified

```bash
# 1) metadata-only snapshot of the Hub repo (no npz)
uv run --with huggingface_hub python -c "
from huggingface_hub import snapshot_download
snapshot_download('windwerfer/neurofeed-eeg-windows', repo_type='dataset',
                  local_dir='hf_snapshot', ignore_patterns=['*.npz'])"

# 2) scrub (optionally verify npz_sha256 against Hub LFS oids: {repo_path: sha256} JSON)
uv run python scripts/scrub_manifests.py --in hf_snapshot --out hf_scrubbed [--lfs-oids oids.json]
```

The script fails (non-zero exit) if any private path pattern (`/workspace`, `/tmp/kaggle`, `/kaggle/`,
`/home/`, `muse-eeg-heads-cache`, …) survives, or if a checksum would change.

## Pre-push check

```bash
rg -n '/workspace|/tmp/kaggle|muse-eeg-heads-cache|/home/|hf_[A-Za-z0-9]{30,}|ghp_[A-Za-z0-9]{20,}' <changed files>
```
