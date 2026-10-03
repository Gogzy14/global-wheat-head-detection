# Baseline analysis — baseline-004-clean-split-3

Recorded: 2026-10-03. This is a completed baseline, ready for error analysis and
geographic evaluation. No further training or new evaluation was run while
preparing this report.

## Evidence and retained artifacts

- User-provided training log and final DetMetrics output are retained in
  `evidence/baseline-004-clean-split-3/`.
- Original run: `outputs/training/baseline-004-clean-split-3/`.
- `results.csv`: all 27 epochs; `args.yaml`: requested training settings.
- `weights/best.pt`: selected model; `weights/last.pt`: final epoch. Both exist.
- `results.png`, PR/F1 curves, confusion matrices, validation labels and predictions
  are already saved by Ultralytics in the original run directory.
- The dataset YAML snapshot retained with the evidence is the current configuration
  observed during this analysis; a separate training-time snapshot was not saved.
- Current Git commit: `b370f378a5a143ab2ae84b91ce41d3f8e8d6a522`.
  This is not independent proof of the exact code state at training time.
- Model weights are excluded from Git by `*.pt`; preserve the run folder when
  backing up the project. A Git commit alone does not back up the model.

## Configuration and split

YOLO26n pretrained, image size 640, batch 4, seed 0, workers 0, 30 requested
epochs, patience 10, close_mosaic 10. Optimizer auto selected AdamW with initial
learning rate 0.002 and momentum 0.9; the requested lr0=0.01 was ignored.

Ultralytics 8.4.152, Python 3.14.3, torch 2.14.0+cu130, NVIDIA GTX 1650 4 GB.
Although args.yaml records amp=true, the training log explicitly reports that
AMP checks failed and AMP was disabled. Use amp=False explicitly in a subsequent
training run on this setup. Keep software versions fixed during comparisons.

Current dataset root: `C:/Users/Korisnik/Desktop/Yolo test/datasets/GlobalWheat2020`.

- Train: arvalis_1, arvalis_2, arvalis_3, rres_1, inrae_1, usask_1;
  2,675 images, including 46 backgrounds, according to the training log.
- Validation: ethz_1; 747 images and 49,603 annotated wheat heads.
- Test: utokyo_1, utokyo_2, nau_1, uq_1; results not yet established here.

The configured subset names do not overlap. This does not establish the absence
of duplicate image content across folders. The README warning about the official
configuration's ethz_1 overlap does not describe this current local split.

## Measured results

Final validation of best.pt, from the supplied DetMetrics output:

| Metric | Value |
|---|---:|
| Precision | 0.9160083096249003 |
| Recall | 0.8977068272474097 |
| mAP50 | 0.9471219282386278 |
| mAP50–95 / fitness | 0.5170493032732125 |
| Best epoch | 17 |
| Completed / requested epochs | 27 / 30 |
| Training duration reported | 1.668 hours (about 100 minutes) |
| Inference time reported | 6.2469 ms/image |

The timing is the validator's measured inference stage on this GPU; it is not an
end-to-end application throughput benchmark. Precision and recall are the
validator's reported operating point, not measurements at an assumed conf=0.25.

| Epoch | mAP50 | mAP50–95 |
|---|---:|---:|
| 1 | 0.87084 | 0.39409 |
| 12 | 0.94207 | 0.50293 |
| 17 | 0.94712 | 0.51704 |
| 26 | 0.94737 | 0.49632 |
| 27 | 0.94435 | 0.48679 |

Epoch values come from results.csv; the small differences from the final
best.pt validation are retained rather than silently combining the two sources.
Epoch 26 slightly maximizes mAP50, but epoch 17 maximizes the selection metric,
mAP50–95. Early stopping correctly stopped after ten epochs without a new best.
The last model is about 3.03 percentage points below the best epoch on mAP50–95.

## Interpretation

The model detects wheat heads well under the more permissive IoU=0.50 matching
criterion on ethz_1. The lower average over IoU=0.50:0.95 suggests substantial
room to improve bounding-box localization at stricter overlap requirements.
mAP50=94.71% is not a statement that 94.71% of all heads are correctly counted.

Training box and classification losses decrease, while validation localization
loss and mAP50–95 fluctuate. After epoch 17, the run does not establish further
validation improvement. This supports stopping this run, but is not conclusive
evidence of severe overfitting or that a different schedule could never help.
Mosaic is disabled from epoch 21, explaining a change in training conditions;
the l1 loss change at that point should not alone be treated as a failure.

These metrics measure validation on one held-out subset used for model selection.
They do not yet establish generalization across the configured test regions or
accuracy of wheat-head counting. No specific visual error category has yet been
confirmed by a systematic review of predictions.

## Recommended next steps

1. Retain this run as the reference baseline and use weights/best.pt. Do not
   extend training solely to reach 30 or 100 epochs.
2. Inspect validation labels versus predictions on a fixed selection of images:
   missed heads, false detections, crowded/overlapping heads, small heads, and
   imprecise boxes. Include representative images, not only the best examples.
3. Freeze this baseline and evaluate it on split=test, both pooled and separately
   for utokyo_1, utokyo_2, nau_1, and uq_1. Record image/head counts, precision,
   recall, mAP50 and mAP50–95 for each. Keep imgsz=640, batch=4, workers=0,
   device=0 and full-precision inference, with explicit matching validation
   settings. Verify the installed 8.4.152 API before preparing evaluation code.
   A simple average of regional mAP values is not the same as pooled mAP.
4. Use the test results to report generalization. Select further hyperparameters
   on validation, not by repeatedly optimizing for the test regions. If test
   errors inform development, disclose that and reserve another untouched set
   for the final assessment.
5. After validation error analysis, a reasonable controlled follow-up is the
   same YOLO26n training setup at imgsz=800, if small-object/localization errors
   justify it. Start from the same pretrained model, keep seed=0 and the same
   split, epochs=30, patience=10 and other settings; use batch=4 if memory allows,
   or record a reduction to 2 as an additional change. Set amp=False. A gain is
   a hypothesis, not guaranteed. Avoid changing resolution, architecture and
   optimizer together. Confirm a promising gain with another seed before making
   a strong claim.

The next practical action is analysis/evaluation of the saved best model, not
another long training run. Existing result files need no manual transcription;
the experiment log and this report retain the interpretation and decisions.

## Reference

[Ultralytics validation documentation](https://docs.ultralytics.com/modes/val/)
describes split selection, reported metrics, validation arguments and the
resolution/computation tradeoff. The online documentation can change; local
8.4.152 logs and artifacts are the authority for what this experiment did.
