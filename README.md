# Global Wheat Head Detection

Internship project for detecting wheat heads in field images using the Global
Wheat Head Dataset and Ultralytics YOLO.

## Project objectives

1. Explore the dataset and verify its annotations.
2. Train a reproducible baseline object-detection model.
3. Evaluate performance, especially across geographic domains.
4. Document experiments, results, and limitations.

## Setup

Create and activate a virtual environment in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

In VS Code, select `.venv` as both the Python interpreter and notebook kernel.

## Dataset

The dataset is intentionally not stored in Git because it is approximately
7 GB. Put a local copy under `data/GlobalWheat2020`, or let Ultralytics download
the official dataset automatically.

For a manually downloaded copy:

1. Copy `configs/dataset.example.yaml` to `configs/dataset.local.yaml`.
2. Replace the example `path` with the dataset location on your computer.
3. Do not commit `dataset.local.yaml`; it is ignored by Git.

Important: the official configuration lists `ethz_1` in both training and
validation. Treat those validation metrics as in-domain results and document
the overlap. The geographic test subsets are better suited to measuring
generalization to unseen regions.

## Typical workflow

Check a local dataset:

```powershell
python scripts/check_dataset.py --config configs/dataset.local.yaml
```

Run a short baseline experiment:

```powershell
python -m src.train --data configs/dataset.local.yaml --epochs 10
```

Evaluate a saved checkpoint:

```powershell
python -m src.evaluate --model models/best.pt --data configs/dataset.local.yaml
```

Generate predictions for an image or folder:

```powershell
python -m src.predict --model models/best.pt --source path/to/images
```

## Repository structure

```text
configs/    portable and local experiment configuration
data/       local dataset only; ignored by Git
models/     downloaded and trained weights; ignored by Git
notebooks/  numbered exploration and analysis notebooks
outputs/    compact figures, metrics, and local predictions
reports/    experiment log and internship report drafts
scripts/    command-line dataset utilities
src/        reusable training, evaluation, and prediction code
tests/      automated checks
```

## Reproducibility

For every important experiment, record the Git commit, model, image size,
epochs, batch size, random seed, dataset split, metrics, and observations in
`reports/experiments.md`.

