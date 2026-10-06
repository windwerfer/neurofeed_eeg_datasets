# neurofeed_eeg_datasets

Public packaging for **derived Muse/Crown EEG window corpora** used to train and evaluate EEG foundation-model heads (neurofeed).

This repo holds **schemas, fixed subject splits, attribution, dataset cards, and prep/upload scripts**. Large window archives (~1.3 G) are published on **Hugging Face Datasets**, not as GitHub blobs. **Hugging Face is the canonical public share path** — not private Kaggle.

## What lives where

| Asset | Where |
|-------|--------|
| Root Hub card, license summary, publish plan | [`docs/hf/`](docs/hf/) ([`DATASET_CARD.md`](docs/hf/DATASET_CARD.md), [`LICENSES.md`](docs/hf/LICENSES.md)) |
| Per-config cards + ATTRIBUTION (one template) | [`docs/hf/cards/`](docs/hf/cards/) |
| Frozen-encoder baselines + negative results | [`baselines/`](baselines/) |
| Window schema / montages / label maps | [`schemas/`](schemas/) (synced from training lab) |
| Fixed subject splits (JSON), cross-config leak-free vigilance list | [`splits/`](splits/) |
| Derived window NPZs | **Hugging Face** [`windwerfer/neurofeed-eeg-windows`](https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows) (mixed upstream licenses CC0-1.0 / ODC-By-1.0 / CC-BY-4.0; configs `muse4_*`, `crown8_*`, `crown2_vigilance_hmc`, `crown4_vigilance_hmc`) |
| App head packs | [`neurofeed_heads`](https://github.com/windwerfer/neurofeed_heads) |
| Feedback gym (in progress) | [`neurofeed/feedback_gym`](https://github.com/windwerfer/neurofeed/tree/main/feedback_gym) |
| Training experiments | [`neurofeed_train`](https://github.com/windwerfer/neurofeed_train) (public train/eval lab) |
| Private GPU scratch | private Kaggle datasets: **maintainer training only**; never published; not a redistribution path |

## Hugging Face dataset

Name: [`windwerfer/neurofeed-eeg-windows`](https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows). The Hub README is [`docs/hf/DATASET_CARD.md`](docs/hf/DATASET_CARD.md); per-config cards are in [`docs/hf/cards/`](docs/hf/cards/).

Load with `huggingface_hub` + NumPy (`uv add huggingface_hub numpy`); each config card has a split-aware snippet.

Configs (derived windows only; no raw PhysioNet EDF dump):

- `muse4_vigilance_sleep_edf` — primary Muse path (Sleep-EDF + HMC, Muse4 proxy)
- `crown2_vigilance_hmc` / `crown4_vigilance_hmc` — **Crown vig ship proxy** (HMC-only CC-BY-4.0; C3/C4 and C3/C4/F6/PO4 with F6≈F4, PO4≈O2; do not mix with muse4)
- `muse4_attention_*` / `crown8_attention_*` — research; `ship_candidate: false` (Crown **attention** still not shippable)
- `muse4_engagement_a_eng` — research; mixed open licenses

## Never publish here or on HF

Raw EDF/BDF recordings, private caches (including private Kaggle scratch datasets), non-commercial (BY-NC) or academic-only corpora, gated REVE base/positions weights, LUNA, unresolved-license material, credentials or private paths.

## Status

Public release on Hugging Face: [`windwerfer/neurofeed-eeg-windows`](https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows). Schemas/splits/docs live in this GitHub repo; app packs in [`neurofeed_heads`](https://github.com/windwerfer/neurofeed_heads).


## License

- **Packaging / docs / scripts in this repo** (schemas, fixed subject splits, attribution docs, prep/upload scripts authored here): **[Apache-2.0](LICENSE)** — see [`LICENSE`](LICENSE).
- **Derived window NPZs on Hugging Face** ([`windwerfer/neurofeed-eeg-windows`](https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows)): remain under their **source corpus licenses** (see [`docs/hf/LICENSES.md`](docs/hf/LICENSES.md)). This Apache grant does **not** re-license those materials or change the HF license metadata.
