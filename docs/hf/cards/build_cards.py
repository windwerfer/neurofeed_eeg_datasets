#!/usr/bin/env python3
"""Render per-config dataset cards (README.md + ATTRIBUTION.md) from one template.

    uv run python docs/hf/cards/build_cards.py

Writes docs/hf/cards/<config>/README.md and ATTRIBUTION.md. The relative links inside
the cards follow the Hugging Face repo layout (<config>/README.md next to schemas/).
"""
from __future__ import annotations

from pathlib import Path
from string import Template

HERE = Path(__file__).resolve().parent
CARD = Template((HERE / "TEMPLATE.md").read_text())
ATTR = Template((HERE / "ATTRIBUTION_TEMPLATE.md").read_text())

LICENSES = {
    "CC0-1.0": ("CC0 1.0 Universal (public domain dedication)", "https://creativecommons.org/publicdomain/zero/1.0/"),
    "ODC-By-1.0": ("Open Data Commons Attribution License v1.0", "https://opendatacommons.org/licenses/by/1-0/"),
    "CC-BY-4.0": ("Creative Commons Attribution 4.0 International", "https://creativecommons.org/licenses/by/4.0/"),
}
PHYSIONET_STD = (
    "Pollard, T., Moody, B. E., Lehman, L., Gow, B., Fernandes, C., Xie, C., Johnson, A., Mark, R. G., & Heldt, T. "
    "(2026). PhysioNet as a global platform for biomedical research. *Nature Health*. "
    "https://doi.org/10.1038/s44360-026-00096-z (the standard PhysioNet citation requested on the landing page)"
)

SOURCES = {
    "sleep_edf": dict(
        name="Sleep-EDF Database Expanded", version="1.0.0", spdx="ODC-By-1.0",
        url="https://physionet.org/content/sleep-edfx/1.0.0/", doi="https://doi.org/10.13026/C2X676",
        host="PhysioNet",
        cite=[
            "B Kemp, AH Zwinderman, B Tuk, HAC Kamphuisen, JJL Oberyé. Analysis of a sleep-dependent neuronal feedback "
            "loop: the slow-wave microcontinuity of the EEG. *IEEE-BME* 47(9):1185–1194 (2000).",
            PHYSIONET_STD,
        ],
        subsets="sleep-cassette (SC) and sleep-telemetry (ST) recordings",
    ),
    "hmc": dict(
        name="Haaglanden Medisch Centrum (HMC) sleep staging database", version="1.1", spdx="CC-BY-4.0",
        url="https://physionet.org/content/hmc-sleep-staging/1.1/", doi="https://doi.org/10.13026/t79q-fr32",
        host="PhysioNet",
        cite=[
            "Alvarez-Estevez, D., & Rijsman, R. (2022). Haaglanden Medisch Centrum sleep staging database "
            "(version 1.1). PhysioNet. https://doi.org/10.13026/t79q-fr32",
            PHYSIONET_STD,
        ],
        subsets="PSG recordings SN001–SN154 (151 available)",
    ),
    "ds001787": dict(
        name="EEG meditation study (OpenNeuro ds001787)", version="1.1.1", spdx="CC0-1.0",
        url="https://openneuro.org/datasets/ds001787/versions/1.1.1", doi="https://doi.org/10.18112/openneuro.ds001787.v1.1.1",
        host="OpenNeuro",
        cite=[
            "Delorme, A., & Brandmeyer, T. EEG meditation study. OpenNeuro ds001787, v1.1.1. "
            "doi:10.18112/openneuro.ds001787.v1.1.1",
            "Brandmeyer, T., & Delorme, A. (2018). Reduced mind wandering in experienced meditators and associated EEG "
            "correlates. *Experimental Brain Research* 236(9):2519–2528. https://doi.org/10.1007/s00221-016-4811-5",
        ],
        subsets="ses-01 BioSemi recordings with thought-probe ratings",
    ),
    "ds003969": dict(
        name="Meditation vs thinking task (OpenNeuro ds003969)", version="1.0.0", spdx="CC0-1.0",
        url="https://openneuro.org/datasets/ds003969/versions/1.0.0", doi="https://doi.org/10.18112/openneuro.ds003969.v1.0.0",
        host="OpenNeuro",
        cite=[
            "Delorme, A., & Braboszcz, C. Meditation vs thinking task. OpenNeuro ds003969, v1.0.0. "
            "doi:10.18112/openneuro.ds003969.v1.0.0",
            "Braboszcz, C., Cahn, B. R., Levy, J., Fernandez, M., & Delorme, A. (2017). Increased gamma brainwave "
            "amplitude compared to control in three different meditation traditions. *PLoS ONE* 12(1):e0170647. "
            "https://doi.org/10.1371/journal.pone.0170647",
        ],
        subsets="med1breath and think1 blocks",
    ),
    "ds007169": dict(
        name="Multimodal Cognitive Workload n-back Task, 4 Difficulties (OpenNeuro ds007169)", version="1.0.5 (current snapshot; export snapshot not recorded)",
        spdx="CC0-1.0", url="https://openneuro.org/datasets/ds007169", doi="https://doi.org/10.18112/openneuro.ds007169.v1.0.5",
        host="OpenNeuro",
        cite=["Barras, M., & Booth, L. Multimodal Cognitive Workload n-back Task, 4 Difficulties. OpenNeuro ds007169. "
              "doi:10.18112/openneuro.ds007169.v1.0.5"],
        subsets="main-phase 1-back and 4-back blocks",
    ),
    "ds007262": dict(
        name="Cognitive Workload 8-level arithmetic (OpenNeuro ds007262)", version="1.1.0 (current snapshot; export snapshot not recorded)",
        spdx="CC0-1.0", url="https://openneuro.org/datasets/ds007262", doi="https://doi.org/10.18112/openneuro.ds007262.v1.1.0",
        host="OpenNeuro",
        cite=["Barras, M., & Booth, L. Cognitive Workload 8-level arithmetic. OpenNeuro ds007262. "
              "doi:10.18112/openneuro.ds007262.v1.1.0"],
        subsets="main-phase trials at the lowest and highest difficulty levels",
    ),
    "ds007554": dict(
        name="Multimodal dataset from the CMx7-MM Experiment (OpenNeuro ds007554)", version="1.0.0",
        spdx="CC0-1.0", url="https://openneuro.org/datasets/ds007554", doi="https://doi.org/10.18112/openneuro.ds007554.v1.0.0",
        host="OpenNeuro",
        cite=["Ajra, Z., Vergotte, G., Perrey, S., Evra, L., Pla, S., Dray, G., Montmain, J., & Xu, B. Multimodal dataset "
              "from the CMx7-MM Experiment. OpenNeuro ds007554, v1.0.0. doi:10.18112/openneuro.ds007554.v1.0.0"],
        subsets="ses-01 passive-motor and n-back/arithmetic tasks",
    ),
    "eegmat": dict(
        name="EEG During Mental Arithmetic Tasks (PhysioNet eegmat)", version="1.0.0", spdx="ODC-By-1.0",
        url="https://physionet.org/content/eegmat/1.0.0/", doi="https://doi.org/10.13026/C2JQ1P",
        host="PhysioNet",
        cite=[
            "Zyma, I., Tukaev, S., Seleznov, I., Kiyono, K., Popov, A., Chernykh, M., & Shpenkov, O. (2019). "
            "Electroencephalograms during Mental Arithmetic Task Performance. *Data* 4(1):14. https://doi.org/10.3390/data4010014",
            PHYSIONET_STD,
        ],
        subsets="rest (_1) and mental-arithmetic (_2) recordings",
    ),
    "stew": dict(
        name="STEW: Simultaneous Task EEG Workload (processed MONSTER mirror)", version="monster-monash/STEW (Hugging Face)",
        spdx="CC-BY-4.0", url="https://huggingface.co/datasets/monster-monash/STEW", doi=None,
        host="Hugging Face (processed mirror); raw data on IEEE DataPort",
        cite=[
            "Lim, W. L., Sourina, O., & Wang, L. (2018). STEW: Simultaneous Task EEG Workload Data Set. *IEEE Transactions "
            "on Neural Systems and Rehabilitation Engineering* 26(11):2106–2114. https://doi.org/10.1109/TNSRE.2018.2872924",
            "Lim, W. L., Sourina, O., & Wang, L. (2020). STEW: Simultaneous task EEG workload data set. IEEE DataPort. "
            "https://ieee-dataport.org/open-access/stew-simultaneous-task-eeg-workload-dataset (CC BY 4.0)",
            "Dempster, A., et al. (2025). MONSTER: Monash Scalable Time Series Evaluation Repository. arXiv:2502.15122",
        ],
        subsets="processed 2-s / 128 Hz segments of the 48 participants",
    ),
}

NB = "https://github.com/windwerfer/neurofeed_train/blob/main"
NB_TREE = "https://github.com/windwerfer/neurofeed_train/tree/main"
LINK_K10 = f"[`kaggle_kernel_10_hmc_crown_vig`]({NB_TREE}/kaggle_kernel_10_hmc_crown_vig): frozen CBraMod Crown vigilance retrain from these windows (also a minimal CBraMod-loading example)"
LINK_K11 = f"[`kaggle_kernel_11_hmc_crown_vig_reve`]({NB_TREE}/kaggle_kernel_11_hmc_crown_vig_reve): same with frozen REVE-base (experimental; bring your own gated weights)"
LINK_NB06 = f"[`notebooks/06_reve_attention_loso.ipynb`]({NB}/notebooks/06_reve_attention_loso.ipynb): embed-once + leave-one-subject-out on the attention configs (REVE-base, bring your own weights); CBraMod twin [`scripts/loso_eval_head_a.py`]({NB}/scripts/loso_eval_head_a.py)"
LINK_HMC = f"REVE HMC paper compare (5-stage, raw HMC 30-s epochs): [`docs/reve_hmc_paper_compare_gap.md`]({NB}/docs/reve_hmc_paper_compare_gap.md) + [`scripts/reve_hmc_paper_compare.py`]({NB}/scripts/reve_hmc_paper_compare.py) (needs raw HMC from PhysioNet)"

VIG_LABELS = ("`drowsy` (0) = hypnogram **W** epochs in the sleep-onset slice; `hypnagogic` (1) = **N1** epochs. "
              "`stage_raw` / `stage_coarse` per window are kept for sleep-stage work")
VIG_LABEL_DETAILS = (
    "- `y = 0 → drowsy`: window's majority stage is **Wake (W)**, inside a slice around the first N1 onset. "
    "This is wake near sleep onset, used as a *drowsy-wake* proxy. It is not a validated drowsiness rating.\n"
    "- `y = 1 → hypnagogic`: majority stage **N1**.\n"
    "- N2/N3/REM/unscored windows are excluded from these exports.\n"
    "- `stage_raw` holds the hypnogram text and `stage_coarse` holds `wake`/`light`/`deep`/`rem`/`unknown`. Both are object arrays, "
    "so load with `allow_pickle=True`.\n"
    "- A window is kept only if one stage covers ≥ 70 % of it (`majority_frac` = 0.7)."
)
ATT_SPLIT_NOTE = ("Frozen val/test subjects were chosen *before* the corpus was expanded and include earlier failed "
                  "holdouts on purpose (honest, hard test). Treat val/test as a small spot check, and prefer LOSO across all subjects.")

def vig_pre(src_desc: str, montage_desc: str) -> str:
    return (
        f"1. {src_desc}\n"
        f"2. Channels: {montage_desc}\n"
        "3. FFT band-pass 1–45 Hz and resample to 256 Hz.\n"
        "4. Slice from 20 min before to 40 min after the **first N1 onset** of each night (`pre_sec`=1200, `post_sec`=2400).\n"
        "5. 2-s windows, hop 0.5 s (75 % overlap), labelled by majority hypnogram stage (≥ 0.7). Only W and N1 windows are kept.\n"
        "6. Stored as float32 microvolts. No per-window normalisation."
    )

CONFIGS = {
    "muse4_vigilance_sleep_edf": dict(
        summary=("Muse-oriented **vigilance (drowsy-wake vs N1)** windows derived from two open PhysioNet sleep databases, "
                 "remapped onto a 4-channel Muse layout (proxy). The largest open, subject-split sleep-onset corpus in a Muse "
                 "channel format; also carries sleep-stage fields."),
        montage="`muse4` **proxy** (Sleep-EDF and HMC PSG electrodes mapped to Muse positions; not Muse hardware)",
        shape="(N, 4, 512)", channels="AF7, AF8, TP9, TP10",
        labels=VIG_LABELS,
        subjects="**124** subjects / 125 nights: 100 Sleep-EDF (78 cassette, 22 telemetry) + 24 HMC · train/val/test **86 / 19 / 19**",
        windows="**519,009** (drowsy 393,616 · hypnagogic 125,393)",
        scale="microvolts, band-pass 1–45 Hz",
        sources=["sleep_edf", "hmc"],
        status="Primary Muse vigilance release (frozen CBraMod head ships on this proxy; true-Muse calibration still recommended)",
        preprocessing=vig_pre(
            "Sleep-EDF Expanded (cassette + telemetry) and HMC v1.1 PSG + hypnograms from PhysioNet.",
            "Sleep-EDF has only Fpz-Cz and Pz-Oz, so **AF7 = AF8 = Fpz-Cz** and **TP9 = TP10 = Pz-Oz** (two "
            "unique signals, each duplicated). HMC: AF7←F4-M1, AF8←C4-M1, TP9←C3-M2, TP10←O2-M1."),
        label_details=VIG_LABEL_DETAILS,
        splits=(
            "Subject-level, frozen (`split_policy.json`): SC400 is the test anchor and SC403 the val anchor; the rest were assigned "
            "about 70/15/15 **by sorted subject id**. As a result the split is **cross-cohort**:\n\n"
            "| Split | Subjects | Composition |\n|---|---:|---|\n"
            "| train | 86 | 76 Sleep-EDF cassette + 10 HMC |\n"
            "| val | 19 | 14 HMC + 4 Sleep-EDF telemetry + 1 cassette (SC403) |\n"
            "| test | 19 | 18 Sleep-EDF **telemetry** + 1 cassette (SC400) |\n\n"
            "Sleep-EDF telemetry recordings come from a study of temazepam effects on sleep (nights may be drug or placebo), so "
            "the test set is mostly a different cohort from training. **Read the published test score (0.747) as a cross-cohort number.** "
            "The split is kept frozen for comparability; no alternative split is provided.\n\n"
            "**Do not combine with `crown2_vigilance_hmc` / `crown4_vigilance_hmc`.** The 24 HMC subjects here also appear "
            "there, and 13 of them are in a different split. If you must pool configs, use "
            "[`cross_config/vigilance_hmc_leakfree.json`](../cross_config/vigilance_hmc_leakfree.json)."
        ),
        split_files="train_subjects.json val_subjects.json test_subjects.json subjects.json split_policy.json",
        file_pattern="<recording>_windows.npz + <recording>_manifest.json (SC4xxx, ST7xxx, SNxxx); 6× <recording>_qc.npz",
        split_load='test_subjects = set(json.load(open(f"{root}/{CFG}/splits/test_subjects.json"))["subjects"])',
        subject_key="subject_id", allow_pickle=True,
        label_list="['drowsy', 'hypnagogic']",
        baselines=("| Encoder (frozen) | Task | Test macro-F1 |\n|---|---|---:|\n"
                   "| CBraMod + linear head | drowsy vs hypnagogic | **0.747** (cross-cohort test, see Splits) |\n"
                   "| CBraMod + linear head | `stage_coarse` wake vs light (probe) | 0.760 |"),
        limitations=(
            "- **Proxy montage.** These are PSG electrodes, not Muse dry electrodes. Sleep-EDF rows contain only two unique signals "
            "(duplicated), and HMC rows use mastoid-referenced F4/C4/C3/O2.\n"
            "- **Cross-cohort split.** Test is mostly the Sleep-EDF telemetry cohort (temazepam study); see Splits.\n"
            "- **Overlapping windows.** Hop 0.5 s gives 75 % overlap. Never split by window; always split by subject.\n"
            "- **Class imbalance** (about 3:1 drowsy:hypnagogic). Report macro-F1 or balanced accuracy.\n"
            "- `drowsy` means W near sleep onset, not a behavioural drowsiness score. Not for clinical use or diagnosis.\n"
            "- Overlaps with the crown vigilance configs (the same 24 HMC subjects, different splits)."
        ),
        notebooks=(
            f"- Training (frozen CBraMod, A-vig + stage probe): [`scripts/train_heads_expanded_sleep_corpus.py`]({NB}/scripts/train_heads_expanded_sleep_corpus.py)\n"
            f"- Window export: [`scripts/expand_head_c_sleep_corpus.py`]({NB}/scripts/expand_head_c_sleep_corpus.py), [`scripts/expand_head_c_hmc.py`]({NB}/scripts/expand_head_c_hmc.py) (need raw PhysioNet data)\n"
            f"- {LINK_HMC}\n"
            "- Head packs: [`neurofeed_heads`](https://github.com/windwerfer/neurofeed_heads)"
        ),
        changes=[
            "Selected the sleep-onset slice of each night (20 min before to 40 min after the first N1 onset).",
            "FFT band-pass 1–45 Hz; resampled to 256 Hz; cut into 2-s windows with 0.5-s hop.",
            "Re-labelled hypnogram stages: W → `drowsy`, N1 → `hypnagogic`; other stages dropped; kept `stage_raw` / `stage_coarse`.",
            "Remapped electrodes onto a Muse 4-channel layout (Sleep-EDF Fpz-Cz/Pz-Oz duplicated; HMC F4/C4/C3/O2 → AF7/AF8/TP9/TP10).",
            "Added subject-level train/val/test splits, per-recording manifests, light QC flags (6 files).",
        ],
    ),
    "crown2_vigilance_hmc": dict(
        summary=("**Vigilance (drowsy-wake vs N1)** windows from the open HMC sleep database using the two **central** electrodes "
                 "C3/C4. These are real C3/C4 positions, which the Neurosity Crown also has. Useful for any central-channel "
                 "sleep-onset or drowsiness model."),
        montage="`crown2_strong`: C3, C4 (true central positions from PSG, mastoid-referenced; not Crown hardware)",
        shape="(N, 2, 512)", channels="C3, C4",
        labels=VIG_LABELS,
        subjects="**151** HMC subjects (1 night each) · train/val/test **106 / 23 / 22** (random, seed 42; same split as `crown4_vigilance_hmc`)",
        windows="**459,438** (drowsy 328,946 · hypnagogic 130,492)",
        scale="microvolts, band-pass 1–45 Hz",
        sources=["hmc"],
        status="Ship candidate for Crown vigilance (proxy); clears the 0.60 test macro-F1 bar",
        preprocessing=vig_pre("HMC v1.1 PSG + hypnograms from PhysioNet (all 151 available recordings).",
                              "C3 ← `EEG C3-M2`, C4 ← `EEG C4-M1`. No fabricated channels."),
        label_details=VIG_LABEL_DETAILS,
        splits=("Subject-level, frozen, random with seed 42: 106 / 23 / 22 subjects, identical to `crown4_vigilance_hmc`.\n\n"
                "**Do not combine with `muse4_vigilance_sleep_edf`.** Its 24 HMC subjects are also here, and 13 of them sit in a "
                "different split. If you must pool configs, use "
                "[`cross_config/vigilance_hmc_leakfree.json`](../cross_config/vigilance_hmc_leakfree.json)."),
        split_files="train_subjects.json val_subjects.json test_subjects.json subjects.json split_policy.json",
        file_pattern="SNxxx_windows.npz + SNxxx_manifest.json",
        split_load='test_subjects = set(json.load(open(f"{root}/{CFG}/splits/test_subjects.json"))["subjects"])',
        subject_key="subject_id", allow_pickle=True,
        label_list="['drowsy', 'hypnagogic']",
        baselines=("| Encoder (frozen) | Test macro-F1 |\n|---|---:|\n"
                   "| CBraMod + linear head | **0.670** |\n| REVE-base + linear head (experimental) | 0.649 |"),
        limitations=(
            "- PSG electrodes (wet, mastoid reference), not the Crown's dry electrodes or reference. Expect a domain gap on device.\n"
            "- Overlapping windows (75 %): split by subject only. Class imbalance about 2.5:1.\n"
            "- `drowsy` means W near sleep onset, not a behavioural drowsiness score. Not for clinical use.\n"
            "- HMC-only; same subjects as `crown4_vigilance_hmc`. Do not mix with Muse4 configs."
        ),
        notebooks=f"- {LINK_K10}\n- {LINK_K11}\n- {LINK_HMC}\n- Head packs: [`neurofeed_heads`](https://github.com/windwerfer/neurofeed_heads) (`packs/cbramod-a-vig-crown2-hmc`, `packs/reve-a-vig-crown2-hmc`)",
        changes=[
            "Selected the sleep-onset slice of each night (20 min before to 40 min after the first N1 onset).",
            "FFT band-pass 1–45 Hz; resampled to 256 Hz; cut into 2-s windows with 0.5-s hop.",
            "Re-labelled hypnogram stages: W → `drowsy`, N1 → `hypnagogic`; other stages dropped; kept `stage_raw` / `stage_coarse`.",
            "Kept only the channels C3-M2 and C4-M1 (stored as C3, C4).",
            "Added subject-level train/val/test splits and per-recording manifests.",
        ],
    ),
    "crown4_vigilance_hmc": dict(
        summary=("**Vigilance (drowsy-wake vs N1)** windows from the open HMC sleep database on a 4-channel layout that "
                 "approximates Neurosity Crown positions: C3, C4 (true) plus F6≈F4 and PO4≈O2 (nearest available PSG electrodes)."),
        montage="`crown4_hmc` **proxy**: C3, C4, F6≈F4, PO4≈O2 (not full Crown8, not Muse4)",
        shape="(N, 4, 512)", channels="C3, C4, F6, PO4",
        labels=VIG_LABELS,
        subjects="**151** HMC subjects · train/val/test **106 / 23 / 22** (random, seed 42; same split as `crown2_vigilance_hmc`)",
        windows="**459,438** (drowsy 328,946 · hypnagogic 130,492)",
        scale="microvolts, band-pass 1–45 Hz",
        sources=["hmc"],
        status="Ship candidate for Crown vigilance (proxy); clears the 0.60 test macro-F1 bar",
        preprocessing=vig_pre("HMC v1.1 PSG + hypnograms from PhysioNet (all 151 available recordings).",
                              "C3 ← `EEG C3-M2`, C4 ← `EEG C4-M1`, **F6 ≈ `EEG F4-M1`**, **PO4 ≈ `EEG O2-M1`** (honest nearest-neighbour proxies)."),
        label_details=VIG_LABEL_DETAILS,
        splits=("Subject-level, frozen, random with seed 42: 106 / 23 / 22 subjects, identical to `crown2_vigilance_hmc`.\n\n"
                "**Do not combine with `muse4_vigilance_sleep_edf`.** Its 24 HMC subjects are also here, and 13 of them sit in a "
                "different split. If you must pool configs, use "
                "[`cross_config/vigilance_hmc_leakfree.json`](../cross_config/vigilance_hmc_leakfree.json)."),
        split_files="train_subjects.json val_subjects.json test_subjects.json subjects.json split_policy.json",
        file_pattern="SNxxx_windows.npz + SNxxx_manifest.json",
        split_load='test_subjects = set(json.load(open(f"{root}/{CFG}/splits/test_subjects.json"))["subjects"])',
        subject_key="subject_id", allow_pickle=True,
        label_list="['drowsy', 'hypnagogic']",
        baselines=("| Encoder (frozen) | Test macro-F1 |\n|---|---:|\n"
                   "| CBraMod + linear head | **0.680** |\n| REVE-base + linear head (experimental) | 0.681 |"),
        limitations=(
            "- F6 and PO4 are **approximations** (F4 and O2), and all channels are wet PSG electrodes with a mastoid reference.\n"
            "- Overlapping windows (75 %): split by subject only. Class imbalance about 2.5:1.\n"
            "- `drowsy` means W near sleep onset, not a behavioural drowsiness score. Not for clinical use.\n"
            "- HMC-only; same subjects as `crown2_vigilance_hmc`. Do not mix with Muse4 or Crown8 configs."
        ),
        notebooks=f"- {LINK_K10}\n- {LINK_K11}\n- {LINK_HMC}\n- Head packs: [`neurofeed_heads`](https://github.com/windwerfer/neurofeed_heads) (`packs/cbramod-a-vig-crown4-hmc`, `packs/reve-a-vig-crown4-hmc`)",
        changes=[
            "Selected the sleep-onset slice of each night (20 min before to 40 min after the first N1 onset).",
            "FFT band-pass 1–45 Hz; resampled to 256 Hz; cut into 2-s windows with 0.5-s hop.",
            "Re-labelled hypnogram stages: W → `drowsy`, N1 → `hypnagogic`; other stages dropped; kept `stage_raw` / `stage_coarse`.",
            "Kept C3-M2, C4-M1, F4-M1, O2-M1 and stored them as C3, C4, F6, PO4 (F6/PO4 are proxies).",
            "Added subject-level train/val/test splits and per-recording manifests.",
        ],
    ),
}

ATT_PRE_1787 = (
    "1. ds001787 ses-01 BioSemi-64 BDF + events + probe log files (OpenNeuro v1.1.1).\n"
    "2. {montage}\n"
    "3. Resampled to 256 Hz. **No band-pass, no re-referencing.** Stored in **volts**.\n"
    "4. For each answered thought probe, 2-s windows (hop 0.5 s) from the ~10 s before the Q1 prompt.\n"
    "5. Label from the probe answers: Q1 > Q2 → `concentration`, Q1 < Q2 → `mind_wandering`; ties and incomplete probes dropped."
)
ATT_PRE_3969 = (
    "1. ds003969 BDF recordings of the `med1breath` (breath meditation) and `think1` (instructed thinking) blocks (OpenNeuro v1.0.0, 1024 Hz).\n"
    "2. {montage}\n"
    "3. Resampled to 256 Hz. **No band-pass, no re-referencing.** Stored in **volts**.\n"
    "4. Trimmed 30 s at block edges; 2-s windows, hop 1.0 s; capped at 400 windows per block (800 per subject, balanced).\n"
    "5. Block label: `med*` → `concentration`, `think*` → `mind_wandering` (protocol proxy)."
)
ATT_LIM_COMMON = (
    "- Subject-held-out performance is **at or near chance** with frozen encoders (see Baselines). That is the main finding, and "
    "it is why these configs are research/negative-result data, not a shippable attention decoder.\n"
    "- **Subject-ID collision:** ds001787 and ds003969 both use `sub-001…`. Key subjects as `<dataset>/<sub>` when combining.\n"
    "- Raw-volt scale, unfiltered: normalise before training.\n"
    "- Overlapping windows: split by subject only."
)

def att_cfg(ds, montage_key):
    is1787 = ds == "ds001787"
    muse = montage_key == "muse4"
    if muse:
        montage = ("`muse4` **proxy**: AF7, AF8 native; TP9/TP10 ← P9/P10 (BioSemi-64 has no TP9/TP10)" if is1787 else
                   "`muse4` **proxy**: AF7, AF8 native; TP9/TP10 ← TP7/TP8 (no TP9/TP10 in the cap)")
        shape, chans = "(N, 4, 512)", "AF7, AF8, TP9, TP10"
    else:
        montage = "`crown8`: CP3, C3, F5, PO3, PO4, F6, C4, CP4 (native 10-10 electrodes from the 64-ch cap; Crown positions, not Crown hardware)"
        shape, chans = "(N, 8, 512)", "CP3, C3, F5, PO3, PO4, F6, C4, CP4"
    nsub = 16 if is1787 else 64
    split = "12 / 2 / 2" if is1787 else "60 / 2 / 2"
    val, test = (("sub-006, sub-015", "sub-019, sub-013") if is1787 else ("sub-026, sub-028", "sub-025, sub-027"))
    windows = ("**5,185** (concentration 3,145 · mind_wandering 2,040)" if is1787 else
               "**51,200** (concentration 25,600 · mind_wandering 25,600)")
    sibling = (f"`crown8_attention_{ds}`" if muse else f"`muse4_attention_{ds}`")
    pre = (ATT_PRE_1787 if is1787 else ATT_PRE_3969).format(
        montage=("Channels: " + montage.split(": ", 1)[1]) if muse else
        ("Channels: BioSemi A/B labels → 10-10 names; picked the 8 Crown positions in Crown stream order. "
         f"Windows are aligned 1:1 with {sibling} (same `starts` and `y`)."))
    if is1787:
        labels = "`concentration` (0) / `mind_wandering` (1), from **thought-probe self-reports** (Q1 vs Q2)"
        label_details = ("- At each probe participants rated meditation depth (Q1, 0–3) and mind-wandering depth (Q2, 0–3). "
                         "Q1 > Q2 → `concentration`, Q1 < Q2 → `mind_wandering`, ties dropped.\n"
                         "- Do **not** map the raw event values 2/4 directly to classes; use the probe answers.\n"
                         "- `probe_ids` groups the windows of one probe (they share a label; never split them).")
    else:
        labels = "`concentration` (0) = breath-meditation block / `mind_wandering` (1) = instructed-thinking block (**protocol proxy**)"
        label_details = ("- Labels are **block-level protocol labels**, not self-reports. Instructed thinking is not spontaneous "
                         "mind-wandering, so treat `mind_wandering` here as `think_block`.\n"
                         "- `task_ids` / `task_names` hold the block per window.")
    baselines = ("| Encoder (frozen) | Protocol | Macro-F1 |\n|---|---|---:|\n"
                 + ("| CBraMod + linear | LOSO over ds001787 + ds003969 (muse4), 77 folds | **0.361 ± 0.209** |\n"
                    "| REVE-base + MLP | embed-once LOSO, same 77 folds | 0.500 ± 0.144 (≈ chance) |" if muse else
                    "| CBraMod + linear | LOSO over crown8 ds001787 + ds003969, 67 folds | **0.351 ± 0.218** |\n"
                    "| CBraMod + linear (muse4 sibling, reference) | LOSO, 77 folds | 0.361 |")
                 + "\n\nChance for a balanced random predictor is about 0.50; majority-class collapse gives about 0.33–0.40.")
    if is1787 and muse:
        baselines += ("\nA meditation-depth variant (Q1 ≤ 1 vs ≥ 2) is also at chance: "
                      f"[`docs/head_a_med_depth_smoke.md`]({NB}/docs/head_a_med_depth_smoke.md).")
    lim = ATT_LIM_COMMON
    if not is1787:
        lim += "\n- `mind_wandering` is an instructed-thinking block, not spontaneous mind-wandering."
    if not muse:
        lim += f"\n- Do not mix with Muse4 configs in one example; {sibling} has the same windows on the Muse4 proxy layout."
    return dict(
        summary=(f"{'Muse4-proxy' if muse else 'Crown8-layout'} **attention / mind-wandering** windows from OpenNeuro {ds} "
                 + ("with rare **thought-probe** labels. " if is1787 else "(breath meditation vs instructed thinking blocks). ")
                 + "Published as an **honest negative benchmark**: frozen-encoder subject-held-out scores are near chance."),
        montage=montage, shape=shape, channels=chans, labels=labels,
        subjects=f"**{nsub}** · train/val/test **{split}** (frozen val = {val}; test = {test})",
        windows=windows, scale="volts (raw), unfiltered",
        sources=[ds],
        status="Research / negative-result data (`ship_candidate: false`)",
        preprocessing=pre, label_details=label_details,
        splits=(f"Subject-level, frozen: train {split.split(' / ')[0]}, val {val}, test {test}. {ATT_SPLIT_NOTE}\n\n"
                f"`{'crown8' if muse else 'muse4'}` sibling {sibling} uses the identical split."),
        split_files="train_subjects.json val_subjects.json test_subjects.json subjects.json split_policy.json",
        file_pattern=("subXXX_ses01_windows.npz + subXXX_ses01_manifest.json" if is1787 else "subXXX_windows.npz + subXXX_manifest.json"),
        split_load='test_subjects = set(json.load(open(f"{root}/{CFG}/splits/test_subjects.json"))["subjects"])',
        subject_key="subject", allow_pickle=False, label_list="['concentration', 'mind_wandering']",
        baselines=baselines, limitations=lim,
        notebooks=(f"- {LINK_NB06}\n"
                   f"- Crown8 LOSO: [`scripts/loso_eval_head_a_crown8.py`]({NB}/scripts/loso_eval_head_a_crown8.py) · write-ups "
                   f"[`docs/loso_head_a.md`]({NB}/docs/loso_head_a.md), [`docs/crown8_attention_loso.md`]({NB}/docs/crown8_attention_loso.md), "
                   f"[`docs/reve_attention_loso.md`]({NB}/docs/reve_attention_loso.md)"),
        changes=([
            "Selected EEG around answered thought probes (ses-01); dropped ties and incomplete probes." if is1787 else
            "Selected the med1breath and think1 blocks; trimmed 30 s at block edges; capped 400 windows per block.",
            "Resampled to 256 Hz and cut into 2-s windows" + (" (hop 0.5 s)." if is1787 else " (hop 1.0 s)."),
            ("Kept 4 electrodes mapped to a Muse layout (" + ("P9/P10 stand in for TP9/TP10" if is1787 else "TP7/TP8 stand in for TP9/TP10") + ")."
             if muse else "Kept the 8 Crown-position electrodes in Crown stream order."),
            ("Derived binary labels from probe self-reports (Q1 vs Q2)." if is1787 else
             "Assigned block-level labels (meditation → `concentration`, thinking → `mind_wandering`)."),
            "Added subject-level splits and per-recording manifests.",
        ]),
    )

for ds in ("ds001787", "ds003969"):
    CONFIGS[f"muse4_attention_{ds}"] = att_cfg(ds, "muse4")
    CONFIGS[f"crown8_attention_{ds}"] = att_cfg(ds, "crown8")

CONFIGS["muse4_engagement_a_eng"] = dict(
    summary=("Muse4-proxy **low vs high mental workload / engagement** windows pooled from five open datasets. The confounds "
             "(task order, cohort, device) are documented, so this config is a **confound benchmark**: a model that scores "
             "well here may be reading task order rather than engagement."),
    montage="`muse4` **proxy**: frontal/temporal electrodes of each source mapped to AF7, AF8, TP9, TP10 (see table below)",
    shape="(N, 4, 512)", channels="AF7, AF8, TP9, TP10",
    labels="`low_engagement` (0) / `high_engagement` (1): source-specific task or rating mapping",
    subjects="**133** unique persons / 150 packs · person-wise train/val/test **93 / 20 / 20** persons (104 / 23 / 23 packs)",
    windows="**19,706** (low 9,528 · high 10,178)",
    scale="dimensionless z-scores clipped at ±15 (per channel; STEW per window)",
    sources=["ds007169", "ds007262", "ds007554", "eegmat", "stew"],
    status="Research only, not a shipping engagement head (confounded)",
    preprocessing=(
        "| Source | Packs | Device / source channels | Mapped to AF7, AF8, TP9, TP10 | Low → High | Known confound |\n"
        "|---|---:|---|---|---|---|\n"
        "| ds007169 | 18 | 19-ch mobile EEG | F7, F8, T3, T4 | 1-back → 4-back | strict L1→L4 order |\n"
        "| ds007262 | 18 | 19-ch mobile EEG (same people as ds007169) | F7, F8, T3, T4 | difficulty 0.6–1.5 → 5.1–6.9 | randomised difficulty (cleanest) |\n"
        "| ds007554 | 30 | 32-ch EEG | F7, F8, T7, T8 | passive motor → n-back/arithmetic | order not fully counterbalanced |\n"
        "| eegmat | 36 | 23-ch EEG | F7, F8, T3, T4 | rest → mental arithmetic | rest always first |\n"
        "| STEW | 48 | 14-ch Emotiv EPOC (hobbyist) | AF3, AF4, T7, T8 | rating ≤ 4 → > 4 | rest then SIMKAP |\n\n"
        "Each source: selected the two task conditions above → resampled to **256 Hz** → 2-s windows, hop 1.0 s → "
        "**z-scored per channel and clipped at ±15**. STEW comes from the processed MONSTER mirror as pre-segmented "
        "2-s windows at **128 Hz**; each window was **upsampled 128 → 256 Hz** (so content stops at 64 Hz) and z-scored per window. "
        "All stored windows are 256 Hz, 512 samples."),
    label_details=("- Labels are task/difficulty conditions (STEW: post-task self-rating) mapped to two levels. They are "
                   "**not** a validated engagement measure.\n"
                   "- `order_confound`, `label_rule`, `device_class` and `scale_note` are recorded per pack in the manifests."),
    splits=("Person-wise, frozen (`splits/splits.json`, seed 42): 93 / 20 / 20 unique persons. ds007169 and ds007262 share "
            "participants (`unique_person_id` = `barras_sub-XXX`), so both tasks of one person stay in one split. This config has "
            "one `splits.json` (keys `splits.train|val|test` → person ids; `persons` → packs) instead of `*_subjects.json`."),
    split_files="splits.json",
    file_pattern="<source>_<subject>_aeng_windows.npz + _aeng_manifest.json (source ∈ ds007169, ds007262, ds007554, eegmat, stew)",
    split_load='test_subjects = set(json.load(open(f"{root}/{CFG}/splits/splits.json"))["splits"]["test"])  # unique_person_id',
    subject_key="unique_person_id", allow_pickle=False, label_list="['low_engagement', 'high_engagement']",
    baselines=("| Encoder (frozen) | Test macro-F1 |\n|---|---:|\n| CBraMod + linear head | 0.548 |\n"
               "| REVE-base + linear head | 0.590 |\n\nBoth count as a misfit given the confounds. An EEGMAT-only stress-vs-calm smoke "
               f"is at chance (0.495): [`docs/head_stress_calm_smoke.md`]({NB}/docs/head_stress_calm_smoke.md)."),
    limitations=(
        "- **Confounded labels:** task order (ds007169, eegmat, STEW), cohort and device type all differ across sources and classes.\n"
        "- Mixed devices, including a hobbyist Emotiv headset; STEW is upsampled from 128 Hz.\n"
        "- Data is z-scored, so absolute amplitude information is gone.\n"
        "- Report per-source results, and prefer ds007262 (randomised difficulty) for any claim about engagement."),
    notebooks=(f"- Training: [`scripts/train_head_a_eng_cbramod.py`]({NB}/scripts/train_head_a_eng_cbramod.py), "
               f"[`scripts/train_head_a_eng_reve.py`]({NB}/scripts/train_head_a_eng_reve.py)\n"
               f"- Corpus build: [`scripts/expand_head_a_eng_corpus.py`]({NB}/scripts/expand_head_a_eng_corpus.py) · write-up "
               f"[`docs/head_a_eng_dual_encoder.md`]({NB}/docs/head_a_eng_dual_encoder.md)"),
    changes=[
        "Selected two task conditions per source and mapped them to low/high engagement (see table).",
        "Mapped four electrodes per source onto a Muse layout (AF7, AF8, TP9, TP10).",
        "Resampled to 256 Hz (STEW: upsampled from 128 Hz) and cut into 2-s windows (hop 1.0 s).",
        "Z-scored per channel (STEW: per window) and clipped at ±15.",
        "Added person-wise splits (shared Barras participants kept together) and per-pack manifests.",
    ],
)

NOTICES = {
    "CC0-1.0": "CC0 sources carry no attribution requirement; citations are given as good scholarly practice.",
    "ODC-By-1.0": ("ODC-By-1.0 sources: this is a derived database. Under ODC-By 1.0 any public use must keep the "
                   "attribution notices above."),
    "CC-BY-4.0": ("CC-BY-4.0 sources: the material was adapted as described under *Changes made*, and is offered under the same "
                  "upstream license terms ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)) with attribution as above. "
                  "No additional restrictions are applied."),
}


def render(cfg: str, c: dict) -> tuple[str, str]:
    srcs = [SOURCES[s] for s in c["sources"]]
    spdx = sorted({s["spdx"] for s in srcs})
    licenses_inline = " · ".join(f"[{x}]({LICENSES[x][1]})" for x in spdx)
    rows = "\n".join(f"| {s['name']} | {s['version']} | `{s['spdx']}` | [{s['host']}]({s['url']}) |" for s in srcs)
    card = CARD.substitute(
        config=cfg, summary=c["summary"], montage=c["montage"], shape=c["shape"], channels=c["channels"],
        labels=c["labels"], subjects=c["subjects"], windows=c["windows"], scale=c["scale"],
        licenses_inline=licenses_inline, status=c["status"], sources_table=rows,
        preprocessing=c["preprocessing"], label_details=c["label_details"], splits=c["splits"],
        split_files=c["split_files"], file_pattern=c["file_pattern"], split_load=c["split_load"],
        subject_key=c["subject_key"],
        allow_pickle=(", allow_pickle=True)  # stage_raw / stage_coarse are object arrays" if c["allow_pickle"] else ")"),
        shape_n=c["shape"], label_list=c["label_list"], baselines=c["baselines"],
        limitations=c["limitations"], notebooks=c["notebooks"],
    )
    blocks = []
    for s in srcs:
        lic_name, lic_url = LICENSES[s["spdx"]]
        cites = "\n".join(f"- {x}" for x in s["cite"])
        doi = f"\n- **DOI:** {s['doi']}" if s.get("doi") else ""
        blocks.append(
            f"## {s['name']}\n\n- **Version:** {s['version']}\n- **Host / landing page:** {s['url']}{doi}\n"
            f"- **License:** `{s['spdx']}` ({lic_name}, {lic_url})\n- **Used:** {s['subsets']}\n- **Cite:**\n"
            + "\n".join("  " + line for line in cites.splitlines())
        )
    changes = "\n".join(f"- {x}" for x in c["changes"])
    changes += ("\n- Removed private file-system paths from manifests and added `license_spdx` / `source_url` per recording "
                "(the window values themselves were not changed by that step).")
    notice = "\n".join(f"- {NOTICES[x]}" for x in spdx)
    attr = ATTR.substitute(config=cfg, source_blocks="\n\n".join(blocks), changes=changes, notice=notice)
    return card, attr


def main() -> None:
    for cfg, c in CONFIGS.items():
        card, attr = render(cfg, c)
        out = HERE / cfg
        out.mkdir(exist_ok=True)
        (out / "README.md").write_text(card)
        (out / "ATTRIBUTION.md").write_text(attr)
        print("wrote", cfg)


if __name__ == "__main__":
    main()
