# Suggested Hugging Face dataset-card frontmatter

The exact license metadata should be finalized after the export manifest and upstream terms are reviewed. This dataset combines sources with different licenses, so do not label the whole repository as a single permissive license.

```yaml
---
pretty_name: Neurofeed EEG Windows
name: windwerfer/neurofeed-eeg-windows
license: other
license_name: Multiple upstream licenses; see README and attribution documents
license_link: docs/PUBLISH_PLAN.md
task_categories:
  - time-series-classification
tags:
  - eeg
  - electroencephalography
  - neuroscience
  - time-series
  - muse
  - crown
  - sleep-staging
  - attention
  - engagement
size_categories:
  - unknown
configs:
  - config_name: muse4_vigilance_sleep_edf
  - config_name: muse4_attention_ds001787
  - config_name: muse4_attention_ds003969
  - config_name: crown8_attention_ds001787
  - config_name: crown8_attention_ds003969
  - config_name: muse4_engagement_a_eng
---
```

Replace `size_categories: unknown` with the HF size bucket after the final parquet export is measured. Keep per-source license and attribution details in the card body.
