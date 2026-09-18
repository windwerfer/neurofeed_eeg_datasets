# Attribution — engagement_a_eng

This config is a derived, Muse4-proxy engagement corpus. It combines the following open-license sources; the combined dataset does not have one uniform upstream license.

## OpenNeuro ds007169

- Source: OpenNeuro `ds007169`, Multimodal Cognitive Workload n-back
- URL: https://openneuro.org/datasets/ds007169
- License: **CC0-1.0**
- Derived use: 1-back as low engagement; 4-back as high engagement
- Note: task order is structured (L1→L2→L3→L4); preserve this confound warning.

## OpenNeuro ds007262

- Source: OpenNeuro `ds007262`, cognitive workload arithmetic
- URL: https://openneuro.org/datasets/ds007262
- License: **CC0-1.0**
- Derived use: lower difficulty (0.6–1.5) as low engagement; higher difficulty (5.1–6.9) as high engagement
- Note: shares Barras participants with ds007169; keep shared people in one split.

## OpenNeuro ds007554

- Source: OpenNeuro `ds007554`, CMx7-MM hierarchical cognitive-motor data
- URL: https://openneuro.org/datasets/ds007554
- License: **CC0-1.0**
- Derived use: PassiveMotor/MotorImagery as low engagement; N-back/arithmetic or mental-arithmetic tasks as high engagement
- Note: task order is not fully counterbalanced.

## PhysioNet EEGMAT

- Source: PhysioNet EEG During Mental Arithmetic Tasks (`eegmat`)
- URL: https://physionet.org/content/eegmat/
- License: **ODC-By-1.0**
- Derived use: rest (`_1`) as low engagement; mental arithmetic (`_2`) as high engagement
- Note: rest precedes arithmetic; this is an order confound. Raw PhysioNet recordings are not redistributed here.

## STEW processed mirror

- Source: processed STEW mirror, `monster-monash/STEW`
- URL: https://huggingface.co/datasets/monster-monash/STEW
- License: **CC-BY-4.0** for the processed mirror used here
- Derived use: rating ≤4 as low engagement; rating >4 as high engagement
- Note: original IEEE DataPort raw access is login-walled; this config uses the processed HF mirror, with 2-second windows at 128 Hz as documented in the source expansion notes.

## Derived artifact policy

Windows are remapped to Muse4 proxy order **AF7, AF8, TP9, TP10**, resampled/windowed as documented by the export manifest. Attribute every source above, preserve source IDs and license fields in manifests, and do not imply native Muse recordings or a validated universal engagement label. This corpus is research-only and not a shipping engagement head.
