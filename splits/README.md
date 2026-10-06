# Fixed subject splits

Copied from the training lab (`muse-eeg-heads/datasets/*/splits`). **No subject appears in more than one split.**

Live counts reconciled 2026-09-18 against on-disk window packs (not the older `attention_corpora_status.md` snapshot from 2026-09-07).

| Corpus | Subjects in catalog | train / val / test | Windows on disk | Notes |
|--------|--------------------:|--------------------|----------------:|-------|
| `vigilance_sleep_edf` | 124 | 86 / 19 / 19 | 125 nights | Sleep-EDF + HMC; Muse4 proxy |
| `vigilance_hmc_crown2` | 151 | 106 / 23 / 22 | 151 packs | HMC-only Crown2 C3/C4; HF `crown2_vigilance_hmc`; **ship_candidate** Crown vig |
| `vigilance_hmc_crown4` | 151 | 106 / 23 / 22 | 151 packs | HMC-only Crown4 proxy C3/C4/F6/PO4 (F6≈F4, PO4≈O2); HF `crown4_vigilance_hmc`; **ship_candidate** Crown vig |
| `attention_ds001787` | 16 | 12 / 2 / 2 | 16 packs | OpenNeuro CC0; frozen val=`sub-006,015` test=`sub-019,013` |
| `attention_ds001787_crown8` | 16 | 12 / 2 / 2 | 16 packs | Same subject splits as muse4 sibling |
| `attention_ds003969` | 64 | 60 / 2 / 2 | 64 packs | Expanded past v0 “11 subjects”; frozen val=`sub-026,028` test=`sub-025,027` |
| `attention_ds003969_crown8` | 64 | 60 / 2 / 2 | 64 packs | Same subject splits as muse4 sibling |
| `engagement_a_eng` | see `splits.json` | unique-person ~70/15/15 | 150 packs | Barras shared person IDs |

**Attention:** still `ship_candidate: false` (honest holdouts historically near chance). Larger N does not by itself make a public head.

Validate in the lab with `uv run python scripts/dataset/validate_splits.py` before treating a revision as frozen for Hugging Face.

**Crown HMC vig:** HMC-only (not Sleep-EDF). Proxy montage caveats apply. Never mix with muse4 / crown8 attention packs.

## Cross-config caveats

- **Do not combine `vigilance_sleep_edf` (HF `muse4_vigilance_sleep_edf`) with `vigilance_hmc_crown2|4`.** The 24 HMC subjects
  (SN001–SN025 without SN014) appear in both, and 13 of them sit in different splits. Splits are leak-free only *within* a config.
  If you must pool configs, use [`cross_config/vigilance_hmc_leakfree.json`](cross_config/vigilance_hmc_leakfree.json): a union
  split that puts each subject in the most held-out split it has anywhere (test > val > train), plus the list of conflicting subjects.
  Results under the union split are not comparable to the published per-config baselines.
- **`vigilance_sleep_edf` is cross-cohort by construction.** Subjects were assigned by sorted id, so train = 76 Sleep-EDF
  cassette + 10 HMC, val = 14 HMC + 4 telemetry + SC403, and test = 18 Sleep-EDF telemetry (temazepam study) + SC400. Frozen as-is.
- **Attention subject IDs collide** across ds001787 and ds003969 (`sub-001…`); key as `<dataset>/<sub>` when pooling.
