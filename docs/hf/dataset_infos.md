# Configuration map

| HF config | Training-lab corpus name | Montage / shape | Subjects (train/val/test) | Windows | Notes |
|---|---|---|---|---:|---|
| `muse4_vigilance_sleep_edf` | `vigilance_sleep_edf` | Muse4 proxy `(N,4,512)` | 124 (86/19/19) | 519,009 | Sleep-EDF + HMC; `stage_raw` / `stage_coarse` kept; cross-cohort test |
| `crown2_vigilance_hmc` | `vigilance_hmc_crown2` | Crown2 `(N,2,512)` C3/C4 | 151 (106/23/22) | 459,438 | HMC-only |
| `crown4_vigilance_hmc` | `vigilance_hmc_crown4` | Crown4 proxy `(N,4,512)` | 151 (106/23/22) | 459,438 | HMC-only; F6≈F4, PO4≈O2 |
| `muse4_attention_ds001787` | `attention_ds001787` | Muse4 proxy `(N,4,512)` | 16 (12/2/2) | 5,185 | thought-probe labels; `ship_candidate: false` |
| `muse4_attention_ds003969` | `attention_ds003969` | Muse4 proxy `(N,4,512)` | 64 (60/2/2) | 51,200 | block labels; `ship_candidate: false` |
| `crown8_attention_ds001787` | `attention_ds001787_crown8` | Crown8 `(N,8,512)` | 16 (12/2/2) | 5,185 | aligned with muse4 sibling |
| `crown8_attention_ds003969` | `attention_ds003969_crown8` | Crown8 `(N,8,512)` | 64 (60/2/2) | 51,200 | aligned with muse4 sibling |
| `muse4_engagement_a_eng` | `engagement_a_eng` | Muse4 proxy `(N,4,512)` | 133 persons (93/20/20) | 19,706 | 5 sources; confounded; research only |

Split JSON in this repo: `splits/<training-lab corpus name>/`, identical to `<HF config>/splits/` on the Hub.
Cross-config note: `splits/cross_config/vigilance_hmc_leakfree.json` (Hub: `cross_config/`).
Window counts come from the per-recording manifests (`n_windows_total`).
