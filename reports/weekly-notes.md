# Weekly notes

## Week 1

### Completed

- Created the project structure.

### Findings

- Add concise technical observations here.

### Problems and decisions

- Record failed attempts and explain important choices.

### Next steps

- Validate the local dataset structure.
- Explore images and bounding-box annotations.
- Train a short baseline run.

## 2026-10-03 — Completed clean-split baseline

- Analyzed baseline-004-clean-split-3 and recorded it in experiments.md.
- Requested 30 epochs; early stopping ended at 27, with best.pt from epoch 17.
- Final validation on ethz_1: precision 0.916008, recall 0.897707,
  mAP50 0.947122, mAP50–95 0.517049.
- Actual setup: YOLO26n, 640, batch 4, seed 0, AdamW lr=0.002; AMP disabled
  automatically on GTX 1650. Runtime approximately 100 minutes.
- Decision: preserve best.pt as the reference baseline; analyze validation
  errors and evaluate geographic test subsets before planning more training.
- Test evaluation and regional comparisons remain pending. Use validation for
  subsequent hyperparameter selection.
- Detailed evidence and recommendations: [baseline analysis](baseline-004-clean-split-3.md).
