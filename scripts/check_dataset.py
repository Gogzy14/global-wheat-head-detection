"""Perform lightweight checks on a YOLO dataset configuration."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with args.config.open(encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)

    dataset_root = Path(config["path"]).expanduser()
    print(f"Dataset root: {dataset_root}")
    print(f"Root exists: {dataset_root.exists()}")

    for split in ("train", "val", "test"):
        entries = config.get(split, [])
        if isinstance(entries, str):
            entries = [entries]
        print(f"{split}: {len(entries)} configured subset(s)")
        for entry in entries:
            path = dataset_root / entry
            print(f"  {'OK' if path.exists() else 'MISSING'}  {path}")


if __name__ == "__main__":
    main()

