# engagement_a_eng

Derived low/high engagement windows for Head A engagement experiments. This README is intended to be copied into `datasets/engagement_a_eng/` when that corpus is packaged.

## Contents

- **Sources:** ds007169, ds007262, ds007554, EEGMAT, and the processed HF STEW mirror.
- **Montage:** Muse4 proxy only; model order `AF7, AF8, TP9, TP10`.
- **Windowing:** nominally 2 s at 256 Hz for Muse4 exports. STEW retains its documented processed-source rate/window recipe; inspect its manifest before concatenation.
- **Labels:** source-specific low/high engagement mappings; see `engagement_a_eng_ATTRIBUTION.md` and the expansion record.
- **Splits:** subject-wise policy; the two Barras datasets share participants and must remain in the same split.

## Current corpus record

The expansion record reports **133 unique persons, 150 packs, and 19,706 windows**: train 93 persons, validation 20, test 20. These numbers must be rechecked against the final manifests before release.

## Caveats

Task order, device family, source cohort, and label construction are confounded. These are not clinical labels and should not be presented as a general engagement detector. The corpus is **research-only / not ship_candidate**; report honest subject-held-out metrics.

## Provenance

The source expansion and mapping are documented in `docs/head_a_eng_corpus_expansion.md` in the source repository. Full source attribution is in `engagement_a_eng_ATTRIBUTION.md`. Raw upstream recordings and private caches are not part of a derived windows release.
