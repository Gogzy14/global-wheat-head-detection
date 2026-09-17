"""Evaluate a trained YOLO model."""

from __future__ import annotations

import argparse
from pathlib import Path

from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True, help="Trained model weights")
    parser.add_argument("--data", type=Path, required=True, help="Dataset YAML path")
    parser.add_argument("--split", choices=("val", "test"), default="test")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model = YOLO(str(args.model))
    model.val(data=str(args.data), split=args.split, project="outputs/evaluation")


if __name__ == "__main__":
    main()

