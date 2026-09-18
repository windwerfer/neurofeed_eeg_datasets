# neurofeed_eeg_datasets

Public packaging for **derived Muse/Crown EEG window corpora** used to train and evaluate EEG foundation-model heads (neurofeed / muse-eeg-heads).

This repo holds **schemas, fixed subject splits, attribution, dataset cards, and prep/upload scripts**. Large window archives (~1.3 G) are published on **Hugging Face Datasets**, not as GitHub blobs.

## What lives where

| Asset | Where |
|-------|--------|
| Dataset card, ATTRIBUTION, publish plan | [`docs/hf/`](docs/hf/) |
| Window schema / montages / label maps | [`schemas/`](schemas/) (synced from training lab) |
| Fixed subject splits (JSON) | forthcoming under `splits/` |
| Derived window NPZs | **Hugging Face** (configs; not in this git tree) |
| Training experiments | `muse-eeg-heads` (private/lab) |
| App head packs | [`neurofeed_heads`](https://github.com/windwerfer/neurofeed_heads) |

## Proposed HF dataset

Name: `muse-eeg-windows` (org TBD) — see [`docs/hf/DATASET_CARD.md`](docs/hf/DATASET_CARD.md).

Configs (derived windows only; no raw PhysioNet EDF dump):

- `muse4_vigilance_sleep_edf` — primary (Sleep-EDF + HMC, Muse4 proxy)
- `muse4_attention_*` / `crown8_attention_*` — research; `ship_candidate: false`
- `muse4_engagement_a_eng` — research; mixed open licenses

## Never publish here or on HF

Raw private caches, L-FAME (BY-NC), gated REVE base weights, LUNA, unresolved-license material.

## Status

Scaffolding for first public release. Window upload to Hugging Face is not done yet.
