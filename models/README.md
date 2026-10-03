# Model artifacts

Store downloaded and trained weights here. Large model files such as `.pt` and
`.onnx` are ignored by Git. Record the origin and metrics of important models in
`reports/experiments.md`.

## baseline-v1

`wheat-yolo26n-baseline-v1.pt` is the preserved copy of
`outputs/training/baseline-004-clean-split-3/weights/best.pt` (epoch 17).
Use this named copy for the first interface. Its source, validation metrics,
environment and SHA-256 are recorded in `baseline-v1.manifest.json` (tracked).

The `.pt` itself is local and ignored. It is also included in
`backups/wheat-baseline-v1.zip`, which must be copied off this computer or uploaded
as a private release asset when GitHub is connected. Neither file is uploaded
by an ordinary Git push. To restore, extract the archive's `baseline-v1/` contents
into the project root, preserving subdirectories, then compare the model's
SHA-256 with the manifest.
