# Configuration map

Local source tree: `/workspace/muse-eeg-heads/datasets/`

| HF config | Local corpus | Window path | Montage / shape | Notes |
|---|---|---|---|---|
| `muse4_vigilance_sleep_edf` | `vigilance_sleep_edf` | `/workspace/muse-eeg-heads/datasets/vigilance_sleep_edf/windows/` | Muse4, `(N,4,512)` | Sleep-EDF + HMC; Head C `stage_raw` / `stage_coarse` retained |
| `muse4_attention_ds001787` | `attention_ds001787` | `/workspace/muse-eeg-heads/datasets/attention_ds001787/windows/` | Muse4 proxy, `(N,4,512)` | OpenNeuro ds001787; `ship_candidate: false` |
| `muse4_attention_ds003969` | `attention_ds003969` | `/workspace/muse-eeg-heads/datasets/attention_ds003969/windows/` | Muse4 proxy, `(N,4,512)` | OpenNeuro ds003969; `ship_candidate: false` |
| `crown8_attention_ds001787` | `attention_ds001787_crown8` | `/workspace/muse-eeg-heads/datasets/attention_ds001787_crown8/windows/` | Crown8, `(N,8,512)` | Separate montage; never mix with Muse4 |
| `crown8_attention_ds003969` | `attention_ds003969_crown8` | `/workspace/muse-eeg-heads/datasets/attention_ds003969_crown8/windows/` | Crown8, `(N,8,512)` | Separate montage; never mix with Muse4 |
| `muse4_engagement_a_eng` | `engagement_a_eng` | `/workspace/muse-eeg-heads/datasets/engagement_a_eng/windows/` | Muse4 proxy, `(N,4,512)` | 133-person research corpus; not a shipping head |
| `crown2_vigilance_hmc` | `vigilance_hmc_crown2` | `/workspace/muse-eeg-heads/datasets/vigilance_hmc_crown2/windows/` | Crown2, `(N,2,512)` C3/C4 | HMC-only; ship_candidate Crown vig |
| `crown4_vigilance_hmc` | `vigilance_hmc_crown4` | `/workspace/muse-eeg-heads/datasets/vigilance_hmc_crown4/windows/` | Crown4 HMC proxy, `(N,4,512)` | F6≈F4, PO4≈O2; ship_candidate Crown vig |

The local paths are source-repository pointers, not paths that should be embedded in the final hosted dataset. Export manifests should replace them with portable relative paths and source IDs.

## Reconciled subject counts (2026-09-18)

- vigilance_sleep_edf: 124 subjects / 125 window nights; splits 86/19/19
- attention_ds001787 (+crown8): 16 subjects; splits 12/2/2
- attention_ds003969 (+crown8): 64 subjects; splits 60/2/2 (expanded; frozen holdouts kept)
- engagement_a_eng: 150 packs / ~133 unique persons via `splits.json`
- Older docs citing 11 attention subjects for ds003969 or 12 for ds001787 are superseded by `splits/`.
- vigilance_hmc_crown2 / crown4: 151 subjects; splits 106/23/22 (shared subjects; HMC-only)
