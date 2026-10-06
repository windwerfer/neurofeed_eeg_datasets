# Per-config cards (source of the Hugging Face config READMEs)

`TEMPLATE.md` and `ATTRIBUTION_TEMPLATE.md` are the single templates. `build_cards.py` holds per-config facts and
per-source citations, and renders `<config>/README.md` + `<config>/ATTRIBUTION.md`:

```bash
uv run python docs/hf/cards/build_cards.py
```

The rendered files are uploaded to the Hub as `<config>/README.md` and `<config>/ATTRIBUTION.md`. Relative links
inside them (`../schemas/…`, `../cross_config/…`) follow the **Hub** layout, not this repo's layout. The root Hub card
is [`../DATASET_CARD.md`](../DATASET_CARD.md) and the license summary is [`../LICENSES.md`](../LICENSES.md).
