# Fixed subject splits

Copied from the training lab (`muse-eeg-heads/datasets/*/splits`). **No subject appears in more than one split.**

| Corpus | Files | Notes |
|--------|-------|--------|
| `vigilance_sleep_edf` | `subjects.json`, `train/val/test_subjects.json`, `split_policy.json` | Sleep-EDF + HMC; stable subject keys |
| `attention_ds001787` | same pattern | OpenNeuro CC0; muse4 |
| `attention_ds001787_crown8` | same pattern | Crown8 sibling; do not mix montages |
| `attention_ds003969` | same pattern | OpenNeuro CC0; muse4 |
| `attention_ds003969_crown8` | same pattern | Crown8 sibling |
| `engagement_a_eng` | `splits.json` | Unique-person policy (Barras shared IDs) |

Validate in the lab with `python scripts/dataset/validate_splits.py` before treating a revision as frozen for Hugging Face.
