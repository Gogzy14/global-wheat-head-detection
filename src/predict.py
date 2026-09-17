"""Run wheat-head detection on an image, directory, or video."""

from __future__ import annotations

import argparse
from pathlib import Path

from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True, help="Trained model weights")
    parser.add_argument("--source", required=True, help="Image, directory, or video source")
    parser.add_argument("--confidence", type=float, default=0.25)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model = YOLO(str(args.model))
    model.predict(
        source=args.source,
        conf=args.confidence,
        save=True,
        project="outputs/predictions",
    )


if __name__ == "__main__":
    main()

