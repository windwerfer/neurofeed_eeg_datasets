# Fixed subject splits

Copied from the training lab (`muse-eeg-heads/datasets/*/splits`). **No subject appears in more than one split.**

Live counts reconciled 2026-09-18 against on-disk window packs (not the older `attention_corpora_status.md` snapshot from 2026-09-07).

| Corpus | Subjects in catalog | train / val / test | Windows on disk | Notes |
|--------|--------------------:|--------------------|----------------:|-------|
| `vigilance_sleep_edf` | 124 | 86 / 19 / 19 | 125 nights | Sleep-EDF + HMC; Muse4 proxy |
| `attention_ds001787` | 16 | 12 / 2 / 2 | 16 packs | OpenNeuro CC0; frozen val=`sub-006,015` test=`sub-019,013` |
| `attention_ds001787_crown8` | 16 | 12 / 2 / 2 | 16 packs | Same subject splits as muse4 sibling |
| `attention_ds003969` | 64 | 60 / 2 / 2 | 64 packs | Expanded past v0 “11 subjects”; frozen val=`sub-026,028` test=`sub-025,027` |
| `attention_ds003969_crown8` | 64 | 60 / 2 / 2 | 64 packs | Same subject splits as muse4 sibling |
| `engagement_a_eng` | see `splits.json` | unique-person ~70/15/15 | 150 packs | Barras shared person IDs |

**Attention:** still `ship_candidate: false` (honest holdouts historically near chance). Larger N does not by itself make a public head.

Validate in the lab with `python scripts/dataset/validate_splits.py` before treating a revision as frozen for Hugging Face.
