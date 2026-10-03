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

## Local Streamlit interface

The dark interface shows the uploaded image and annotated result side by side.
Choose a confidence threshold, use the label and confidence display options,
then click **Detect wheat heads** to run
`models/wheat-yolo26n-baseline-v1.pt` locally at image size 640 with FP32
inference.

The detection count is a model estimate; counting accuracy has not been
validated separately. Changing the uploaded image or confidence threshold
clears the previous result until detection is run again. Result downloads
will be added in the next step.

Design and integration references:
[Ultralytics YOLO26 demo](https://huggingface.co/spaces/Ultralytics/YOLO26) and
[Ultralytics Streamlit guide](https://docs.ultralytics.com/guides/streamlit-live-inference#live-inference-with-streamlit-application-using-ultralytics-yolo26).

Run these commands in PowerShell from the project folder, using the existing
baseline `.venv` environment. Install the interface dependency if needed:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-interface.txt
```

The interface requirements pin Streamlit and use the saved baseline versions
as constraints so that installing the interface does not upgrade those packages.

Start the local interface:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.headless true --browser.gatherUsageStats false
```

Open [http://127.0.0.1:8501](http://127.0.0.1:8501) in your browser. The app runs
on this computer only. Leave the terminal running while using the page, then
press `Ctrl+C` in that terminal to stop it.

## Dataset

The dataset is intentionally not stored in Git because it is approximately
7 GB. Put a local copy under `data/GlobalWheat2020`, or let Ultralytics download
the official dataset automatically.

For a manually downloaded copy:

1. Copy `configs/dataset.example.yaml` to `configs/dataset.local.yaml`.
2. Replace the example `path` with the dataset location on your computer.
3. Do not commit `dataset.local.yaml`; it is ignored by Git.

The local baseline and example configuration reserve `ethz_1` for validation;
it is excluded from training. Earlier runs used an overlapping configuration
and are not directly comparable. The geographic test subsets measure
generalization to additional unseen regions.

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

The `baseline-v1` checkpoint is documented in
[`reports/baseline-v1-preservation.md`](reports/baseline-v1-preservation.md).
It preserves the completed model before interface development. Exact installed
package versions are in `requirements-baseline-v1.freeze.txt`; this Windows/CUDA
environment inventory is not a portable deployment lockfile. Model weights and
local backup archives are excluded from Git and must be transferred separately.
