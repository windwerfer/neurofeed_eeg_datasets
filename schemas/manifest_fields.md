# Manifest fields (`<config>/windows/<stem>_manifest.json`)

All manifests are JSON objects. Common fields after the `cards-v1` scrub:

| Field | Present in | Meaning |
|---|---|---|
| `npz_path` | all | Config-relative path of the window file on the Hub, e.g. `windows/SN001_windows.npz` |
| `npz_sha256` | all | SHA-256 of that `.npz` (equals the Hub LFS oid) |
| `license_spdx` | all | SPDX id of the upstream source: `CC0-1.0`, `ODC-By-1.0` or `CC-BY-4.0` |
| `source_dataset` | all | Upstream dataset name and version |
| `source_url` | all | Upstream file URL (PhysioNet recordings) or dataset landing page |
| `source_landing_page` | all | Upstream landing page (license, terms, citation) |
| `license_attribution` | vigilance configs | Free-text attribution line(s) for the data sources (no encoder entries) |
| `n_windows_total`, `n_windows_per_label` (`counts`/`n_windows` in a_eng) | all | Window counts |
| `window_sec`, `hop_sec`, `target_sr` | all | 2.0 s, hop 0.5–1.0 s, 256 Hz |
| `window_shape` | most | `[N, C, 512]` |
| `subject_id` / `subject` / `unique_person_id` | vigilance / attention / a_eng | Key used by the split JSON |
| `recording_id`, `night`, `session`, `study` | where applicable | Recording identity (`study`: Sleep-EDF `cassette` / `telemetry`, `hmc`) |
| `psg_file`, `hypno_file`, `psg_sha256`, `hypno_sha256` | vigilance | Upstream PhysioNet file names and checksums (raw files are **not** redistributed) |
| `bdf`, `events`, `log_file`, `per_task_bdf`, `*_sha256` | attention | Upstream BIDS-relative file paths and checksums |
| `montage` / `montage_id`, `channels`, `channel_strategy`, `channel_note`, `channel_proxy_note` | all | How upstream electrodes map onto the stored channel order |
| `stage_to_label_map`, `stage_to_coarse_map`, `label_rule` | all | Label construction |
| `slice_start_sec`, `pre_sec`, `post_sec`, `around_stage`, `majority_frac` | vigilance | N1-slice recipe (20 min before / 40 min after the first N1, label = majority stage ≥ 0.7 within the window) |
| `order_confound`, `scale_note`, `device_class`, `research_only` | a_eng | Confound and scaling notes |
| `manifest_scrubbed` | all | Marks the portable-path rewrite |

Private absolute paths were removed in `cards-v1`; the window files themselves were not changed.
