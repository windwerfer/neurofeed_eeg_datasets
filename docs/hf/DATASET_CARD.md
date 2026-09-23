# `windwerfer/neurofeed-eeg-windows`

Hugging Face dataset: **[`windwerfer/neurofeed-eeg-windows`](https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows)**.

## Purpose

Derived EEG windows for training and evaluating Muse-oriented heads. The default pack is a **Muse4** proxy: 2-second windows at 256 Hz, with `X` shaped `(N, 4, 512)` and channel order **AF7, AF8, TP9, TP10**. A separate **Crown8** pack uses `(N, 8, 512)` and must not be mixed with Muse4 examples.

These are derived windows and labels, not a replacement for the original source datasets. Splits are subject-wise where the source corpus supports it; manifests should be treated as the authority for provenance, labels, checksums, and split membership.

## Configurations

**Subject counts (reconciled 2026-09-18):** `vigilance_sleep_edf` 124 subjects (86/19/19); `attention_ds001787` (+crown8) 16 subjects (12/2/2); `attention_ds003969` (+crown8) **64** subjects (60/2/2) — expanded beyond the older 11-subject status writeup; frozen val/test holdouts unchanged. See [`splits/README.md`](../../splits/README.md).

| Config | Montage / shape | Sources and intended use | Status |
|---|---|---|---|
| `muse4_vigilance_sleep_edf` | Muse4, `(N,4,512)` | Sleep-EDF Expanded + HMC; vigilance and Head C stage fields | primary release candidate |
| `muse4_attention_ds001787` | Muse4 proxy, `(N,4,512)` | OpenNeuro ds001787; concentration / mind-wandering research | research only; `ship_candidate: false` |
| `muse4_attention_ds003969` | Muse4 proxy, `(N,4,512)` | OpenNeuro ds003969; meditation/thinking protocol proxy | research only; `ship_candidate: false` |
| `crown8_attention_ds001787` | Crown8, `(N,8,512)` | Crown8 re-parse of ds001787 | research only; `ship_candidate: false` |
| `crown8_attention_ds003969` | Crown8, `(N,8,512)` | Crown8 re-parse of ds003969 | research only; `ship_candidate: false` |
| `muse4_engagement_a_eng` | Muse4 proxy, `(N,4,512)` | Open-license derived low/high engagement windows | research only; not a shipping head |

Sleep-EDF and HMC are not native Muse recordings: they use a documented **Muse4 proxy** mapping. Attention corpora are also source-device data remapped to a Muse-like four-channel layout. Crown8 is a separate montage with channels `CP3, C3, F5, PO3, PO4, F6, C4, CP4` in stream order.

## Limitations and label cautions

- Attention configs have historically near-chance subject holdouts and are **not ship candidates**.
- A-eng is a heterogeneous proxy corpus with task/order and device confounds; it is **not a shipping engagement head**.
- Sleep-EDF/HMC are useful transfer data for vigilance, but their Muse4 geometry is a proxy, not native Muse hardware.
- Labels encode source-specific protocols, not a universal clinical or psychological state. Do not infer diagnosis, attention ability, or sleep disorder from them.
- Do not mix Muse4 and Crown8 examples in one training example or silently treat proxy channels as native channels.
- Check the per-config manifests for preprocessing, units, source IDs, subject splits, and checksums before training.

## Not included

This proposal contains no raw EDF/BDF files, no L-FAME data, no gated REVE weights or positions cache, and no private model/data cache. It is not a mirror of private Kaggle artifacts. Obtain upstream data under its own terms when a reproduction requires it.

## Notebook links

See [`notebooks/README.md`](notebooks/README.md). The planned links are notebooks **02**, **03**, and **04** from the source project; any Kaggle-specific paths must be de-Kaggle'd before publication. Large notebooks do not need to be copied into this dataset—short notes and stable source-repository pointers are preferred.

## Load sketch

After a dataset builder/config is published, the intended interface is:

```python
from datasets import load_dataset

ds = load_dataset("windwerfer/neurofeed-eeg-windows", "muse4_vigilance_sleep_edf")
row = ds["train"][0]
X = row["X"]       # one 4 x 512 float32 window (or 8 x 512 for Crown8)
y = row["label"]
```

The final feature names and split export format are provisional. Pin the dataset revision and consult the published card before using it for a benchmark.

## Provenance and attribution

See [`docs/engagement_a_eng_ATTRIBUTION.md`](docs/engagement_a_eng_ATTRIBUTION.md) for the A-eng source list and [`docs/PUBLISH_PLAN.md`](docs/PUBLISH_PLAN.md) for release and licensing policy. Original sources retain their own licenses and attribution requirements.
