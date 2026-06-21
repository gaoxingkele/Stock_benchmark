# Universe, Splits, And Labels

This benchmark uses reusable universe, split, and label definitions before paper-specific model code.

## Current Smoke Universe

```text
configs/universes/csi300_smoke.json
```

It points to:

```text
data/processed/cn_a_share/csi300_by_date_smoke/instruments/csi300.txt
data/processed/cn_a_share/csi300_by_date_smoke/calendars/day.txt
```

The current smoke universe contains 300 CSI300 symbols over 7 trading dates from 2024-01-02 to 2024-01-10.

## Current Smoke Split

```text
configs/splits/csi300_by_date_smoke.json
```

```text
train: 2024-01-02 to 2024-01-05
test:  2024-01-08 to 2024-01-10
```

This split is only for code-path validation. Formal benchmark splits still need long-history data and a validation segment.

## Label Generation

Generate one-day forward returns:

```bash
python Stock_benchmark/scripts/generate_forward_return_labels.py \
  --panel Stock_benchmark/data/processed/cn_a_share/csi300_by_date_smoke/panel.csv \
  --horizon 1 \
  --out Stock_benchmark/data/processed/cn_a_share/csi300_by_date_smoke/labels_h1.csv
```

Generate five-day forward returns on long-history data by changing `--horizon 5`.

## Validation

```bash
python Stock_benchmark/scripts/validate_smoke_protocol.py
```

Verified output:

```text
instruments={'count': '300', 'start_date': '2024-01-02', 'end_date': '2024-01-10'}
calendar_dates=7 split_calendar_coverage={'train': 4, 'test': 3}
panel_rows_by_split={'train': 1200, 'test': 900}
labels_h1=1800 labels_h5=600
```

Generated label files:

```text
data/processed/cn_a_share/csi300_by_date_smoke/labels_h1.csv
data/processed/cn_a_share/csi300_by_date_smoke/labels_h5.csv
```
