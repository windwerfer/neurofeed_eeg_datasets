# Baselines and honest negative results

Reference numbers for the derived window configs on Hugging Face
[`windwerfer/neurofeed-eeg-windows`](https://huggingface.co/datasets/windwerfer/neurofeed-eeg-windows).
All runs use **frozen** foundation encoders (no backbone fine-tuning) and a small linear (or MLP) head, evaluated
on **held-out subjects** using the fixed split JSON in [`../splits/`](../splits/). The splits are unchanged and identical to the
`splits/` folders on the Hub.

Each JSON file is the run's full metrics summary (per-class metrics, confusion matrices, per-fold results where
applicable). Private paths and caches were removed. Encoder weights are referenced by public id only: CBraMod is
Apache-2.0; REVE-base is **gated**, so bring your own weights, which are never redistributed here.

Metric: **macro-F1** unless noted. For balanced binary tasks a random predictor scores about **0.50**; a
majority-class collapse scores about **0.33–0.40**.

## Vigilance / sleep (positive results)

| File | Config | Encoder | Protocol | Test macro-F1 |
|---|---|---|---|---:|
| [`a_vig_muse4_cbramod.json`](a_vig_muse4_cbramod.json) | `muse4_vigilance_sleep_edf` | CBraMod | drowsy (W) vs hypnagogic (N1), fixed split 86/19/19 subj | **0.747** (n=61,736) |
| [`head_c_wake_light_muse4_cbramod.json`](head_c_wake_light_muse4_cbramod.json) | `muse4_vigilance_sleep_edf` | CBraMod | `stage_coarse` wake vs light, N1-slice (probe, not 4-way staging) | 0.760 |
| [`crown_hmc_vig_cbramod.json`](crown_hmc_vig_cbramod.json) | `crown2_vigilance_hmc` / `crown4_vigilance_hmc` | CBraMod | W vs N1, fixed split 106/23/22 subj | **0.670** / **0.680** |
| [`crown_hmc_vig_reve.json`](crown_hmc_vig_reve.json) | `crown2_vigilance_hmc` / `crown4_vigilance_hmc` | REVE-base (experimental) | same | 0.649 / 0.681 |
| [`reve_hmc_5stage_paper_compare.json`](reve_hmc_5stage_paper_compare.json) | *(raw HMC, not a window config)* | REVE-base | 5-stage, 30-s epochs, 24 local HMC nights, linear probe | balanced acc **0.649** vs paper 0.647 |

**Muse4 vigilance split is cross-cohort.** The frozen split assigned subjects by sorted id, so test is 18 Sleep-EDF
*telemetry* subjects (the temazepam/placebo study) plus SC400, val is mostly HMC (14 HMC, 4 telemetry, 1 cassette),
and train is mostly Sleep-EDF cassette (76) plus 10 HMC. Read 0.747 as a cross-cohort number. The split stays frozen
so results remain comparable.

## Attention / engagement (negative or near-chance results)

| File | Config | Encoder | Protocol | Result |
|---|---|---|---|---:|
| [`loso_attention_muse4_cbramod.json`](loso_attention_muse4_cbramod.json) | `muse4_attention_ds001787` + `_ds003969` | CBraMod | leave-one-subject-out, 77 folds | macro-F1 **0.361 ± 0.209** |
| [`loso_attention_crown8_cbramod.json`](loso_attention_crown8_cbramod.json) | `crown8_attention_*` | CBraMod | LOSO, 67 folds | 0.351 ± 0.218 |
| [`loso_attention_muse4_reve.json`](loso_attention_muse4_reve.json) | `muse4_attention_*` | REVE-base | embed-once + LOSO, 77 folds (linear / MLP) | 0.480 / **0.500** ± 0.144 |
| [`a_eng_muse4_cbramod.json`](a_eng_muse4_cbramod.json) | `muse4_engagement_a_eng` | CBraMod | low vs high engagement, person-wise split | 0.548 |
| [`a_eng_muse4_reve.json`](a_eng_muse4_reve.json) | `muse4_engagement_a_eng` | REVE-base | same | 0.590 |

Caveats:
- **Subject-ID collision.** ds001787 and ds003969 both use `sub-001…`; the LOSO runs key subjects as
  `<dataset>/<sub>` (see `raw_id_collisions`). Do the same when combining these configs.
- ds003969 labels are a **protocol proxy** (meditation block vs instructed-thinking block), not probe-rated mind-wandering.
- A-eng labels are confounded with task order, cohort and device. Treat the scores as an upper bound on what a
  shortcut can reach, not as engagement decoding.

Smaller negative smokes (rest vs meditation on ds003816, ds001787 meditation-depth Q1, EEGMAT stress vs calm; all
at or near chance) are documented in the training lab:
[`docs/head_a_med_smoke.md`](https://github.com/windwerfer/neurofeed_train/blob/main/docs/head_a_med_smoke.md),
[`docs/head_a_med_depth_smoke.md`](https://github.com/windwerfer/neurofeed_train/blob/main/docs/head_a_med_depth_smoke.md),
[`docs/head_stress_calm_smoke.md`](https://github.com/windwerfer/neurofeed_train/blob/main/docs/head_stress_calm_smoke.md).

## Reproduce

Code lives in [`neurofeed_train`](https://github.com/windwerfer/neurofeed_train): `scripts/train_heads_expanded_sleep_corpus.py`,
`scripts/train_hmc_crown_vig_compare.py` / `train_hmc_crown_vig_reve.py` (notebooks `kaggle_kernel_10` / `11`),
`scripts/loso_eval_head_a.py` / `loso_eval_head_a_crown8.py`, `notebooks/06_reve_attention_loso.ipynb`,
`scripts/train_head_a_eng_cbramod.py` / `train_head_a_eng_reve.py`, and `scripts/reve_hmc_paper_compare.py`
(the paper compare needs raw HMC from PhysioNet). Trained head packs are in
[`neurofeed_heads`](https://github.com/windwerfer/neurofeed_heads).

Licenses of the underlying data: see each config's `ATTRIBUTION.md` on the Hub. The numbers in this folder are
released with the repo's packaging license (Apache-2.0); they do not re-license any data.
