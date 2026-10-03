# baseline-v1 — checkpoint before interface development

Prepared on 2026-10-03 at the user's request. Further training and geographic
test evaluation are deferred; the next phase is a simple interface using the
current saved model. No interface code or deployment is part of this checkpoint.

## Preserved model and results

- Source: `outputs/training/baseline-004-clean-split-3/weights/best.pt`.
- Named copy: `models/wheat-yolo26n-baseline-v1.pt`.
- Best epoch: 17; completed epochs: 27 of 30; patience: 10.
- Validation: ethz_1, 747 images, 49,603 heads.
- Precision 0.9160083096249003; recall 0.8977068272474097;
  mAP50 0.9471219282386278; mAP50–95 0.5170493032732125.
- `models/baseline-v1.manifest.json` records SHA-256 and exact model provenance.
- Source logs, per-epoch results, arguments and plots are retained in the
  experiment folders and included in the baseline commit.
- `reports/baseline-004-clean-split-3.md` contains the analysis. Its proposed
  model improvements are deferred, not prerequisites for the interface.

## Environment and configuration

- Python 3.14.3, Ultralytics 8.4.152, torch 2.14.0+cu130,
  torchvision 0.29.0+cu130; Windows, GTX 1650 4 GB.
- `requirements.txt` pins direct project dependencies.
- `requirements-baseline-v1.freeze.txt` is the full `pip freeze --all` inventory
  from the project environment, captured before adding any interface libraries.
- The inventory is machine-specific, not a verified installation recipe for
  another OS or hosting service. The CUDA-tagged torch wheels require an
  appropriate PyTorch package source; a plain PyPI install is not assumed to
  reproduce them. No fresh-environment recreation was performed.
- `configs/dataset.example.yaml` now represents the actual clean subset split,
  using a placeholder dataset root. Set that root locally before training.
- Original raw evidence retains the original local paths for provenance.
- AMP was automatically disabled during training; use full-precision inference
  initially. The interface should start at image size 640 and report detected
  head count as a model estimate, not an established counting accuracy.

## Backup and Git scope

The local archive `backups/wheat-baseline-v1.zip` contains the named best model,
the manifest, environment inventory, portable dataset configuration, reports,
raw logs, run arguments, per-epoch metrics and main result plots. It is a
preservation package, not a complete standalone application or a dataset backup.
The full source history is retained separately by Git and the `baseline-v1` tag.

The archive and model are excluded from Git. Their presence on the same disk is
not protection from disk loss; an off-device copy remains part of the GitHub/
backup step. Keep the original training folder as well. `last.pt` remains there;
the archive prioritizes the selected `best.pt` needed by the interface.

The unrelated untracked internship Word document is left untouched and excluded
from this commit. Earlier files already in Git remain in its history.

## GitHub handoff

Create an empty private repository without initializing a README, .gitignore or
license. Connect its URL as `origin`, then push the current branch and the
`baseline-v1` tag. Upload the ZIP separately as a private release asset for that
tag, or retain an equivalent off-device backup. Do not upload the dataset or
virtual environment. Repository creation, network push and release upload are
not performed by this local preservation step.
