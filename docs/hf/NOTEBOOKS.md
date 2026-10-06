# Notebooks and scripts linked from the dataset cards

All code lives in the public training lab [`neurofeed_train`](https://github.com/windwerfer/neurofeed_train). These are
the entries the Hugging Face cards link to:

| What | Link | Used by configs |
|---|---|---|
| Crown vigilance retrain, frozen **CBraMod** (also a minimal CBraMod-loading example) | [`kaggle_kernel_10_hmc_crown_vig`](https://github.com/windwerfer/neurofeed_train/tree/main/kaggle_kernel_10_hmc_crown_vig) | `crown2_vigilance_hmc`, `crown4_vigilance_hmc` |
| Crown vigilance retrain, frozen **REVE-base** (experimental; bring your own gated weights) | [`kaggle_kernel_11_hmc_crown_vig_reve`](https://github.com/windwerfer/neurofeed_train/tree/main/kaggle_kernel_11_hmc_crown_vig_reve) | `crown2_vigilance_hmc`, `crown4_vigilance_hmc` |
| **Embed-once + LOSO** (REVE-base) | [`notebooks/06_reve_attention_loso.ipynb`](https://github.com/windwerfer/neurofeed_train/blob/main/notebooks/06_reve_attention_loso.ipynb) | `muse4_attention_*` |
| LOSO with frozen CBraMod | [`scripts/loso_eval_head_a.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/loso_eval_head_a.py), [`scripts/loso_eval_head_a_crown8.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/loso_eval_head_a_crown8.py) | `muse4_attention_*`, `crown8_attention_*` |
| **HMC paper compare** (REVE 5-stage linear probe on raw HMC 30-s epochs) | [`docs/reve_hmc_paper_compare_gap.md`](https://github.com/windwerfer/neurofeed_train/blob/main/docs/reve_hmc_paper_compare_gap.md) + [`scripts/reve_hmc_paper_compare.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/reve_hmc_paper_compare.py) | crown / muse4 vigilance (context) |
| Muse4 vigilance + sleep-stage probe training | [`scripts/train_heads_expanded_sleep_corpus.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/train_heads_expanded_sleep_corpus.py) | `muse4_vigilance_sleep_edf` |
| Engagement training | [`scripts/train_head_a_eng_cbramod.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/train_head_a_eng_cbramod.py), [`scripts/train_head_a_eng_reve.py`](https://github.com/windwerfer/neurofeed_train/blob/main/scripts/train_head_a_eng_reve.py) | `muse4_engagement_a_eng` |

Older maintainer notebooks (01, 03, 04, 05, 07, 08) are in `neurofeed_train/archive/`. They are not linked from the cards
because they depend on private scratch inputs.

Before linking any new notebook publicly, strip private paths, private dataset names and secrets, and read the windows from
this Hugging Face dataset.
