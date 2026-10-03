# Experiment log

Record one row for every experiment worth comparing. Use the Git commit column
to connect the result to the exact version of the code.

| ID | Date | Git commit | Model | Image size | Epochs | Batch | Seed | Split | mAP50 | mAP50–95 | Notes |
|---|---|---|---|---:|---:|---:|---:|---|---:|---:|---|
| baseline-004-clean-split-3 | 2026-10-03 | `b370f37`* | YOLO26n | 640 | 27/30; best 17 | 4 | 0 | val: ethz_1 | 0.947122 | 0.517049 | patience=10; P=0.916008; R=0.897707; 1.668 h; AMP automatically disabled; AdamW lr=0.002 |

*Commit observed when documenting the run; the training-time commit was not
recorded independently. Metrics above are from the final validation of `best.pt`,
not the last epoch. The previous baseline-001 row was an unmeasured template,
not an experimental result.

See [analysis and next steps](baseline-004-clean-split-3.md) for evidence,
limitations, the dataset split, and the evaluation plan. Test metrics are pending.
