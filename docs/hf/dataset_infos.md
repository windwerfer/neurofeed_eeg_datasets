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

The local paths are source-repository pointers, not paths that should be embedded in the final hosted dataset. Export manifests should replace them with portable relative paths and source IDs.
