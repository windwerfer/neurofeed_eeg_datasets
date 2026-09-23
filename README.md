# neurofeed_eeg_datasets

Public packaging for **derived Muse/Crown EEG window corpora** used to train and evaluate EEG foundation-model heads (neurofeed).

This repo holds **schemas, fixed subject splits, attribution, dataset cards, and prep/upload scripts**. Large window archives (~1.3 G) are published on **Hugging Face Datasets**, not as GitHub blobs. **Hugging Face is the canonical public share path** — not private Kaggle.

## What lives where

| Asset | Where |
|-------|--------|
| Dataset card, ATTRIBUTION, publish plan | [`docs/hf/`](docs/hf/) |
| Window schema / montages / label maps | [`schemas/`](schemas/) (synced from training lab) |
| Fixed subject splits (JSON) | [`splits/`](splits/) |
| Derived window NPZs | **Hugging Face** [`windwerfer/neurofeed-eeg-windows`](https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows) (license other; configs `muse4_*`, `crown8_*`) |
| App head packs | [`neurofeed_heads`](https://github.com/windwerfer/neurofeed_heads) |
| Feedback gym (in progress) | [`neurofeed/feedback_gym`](https://github.com/windwerfer/neurofeed/tree/main/feedback_gym) |
| Training experiments | `muse-eeg-heads` (local/unpublished; a future public train-lab repo is under discussion) |
| Private GPU scratch | Kaggle `muse-eeg-heads-windows` / `muse-eeg-heads-cache` / src / aeng — **private training only**; **never publish cache**; not a public redistribution path |

## Hugging Face dataset

Name: [`windwerfer/neurofeed-eeg-windows`](https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows) — see [`docs/hf/DATASET_CARD.md`](docs/hf/DATASET_CARD.md).

Configs (derived windows only; no raw PhysioNet EDF dump):

- `muse4_vigilance_sleep_edf` — primary (Sleep-EDF + HMC, Muse4 proxy)
- `muse4_attention_*` / `crown8_attention_*` — research; `ship_candidate: false` (Crown attention LOSO ~chance; no shippable Crown packs in neurofeed_heads yet)
- `muse4_engagement_a_eng` — research; mixed open licenses

## Never publish here or on HF

Raw private caches, L-FAME (BY-NC), gated REVE base weights, LUNA, unresolved-license material, or Kaggle `muse-eeg-heads-cache` contents.

## Status

Public release on Hugging Face: [`windwerfer/neurofeed-eeg-windows`](https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows). Schemas/splits/docs live in this GitHub repo; app packs in [`neurofeed_heads`](https://github.com/windwerfer/neurofeed_heads).
