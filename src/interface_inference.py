"""Local, reusable model inference for the Streamlit image interface."""

from __future__ import annotations

from pathlib import Path
from threading import Lock
from typing import TYPE_CHECKING

from PIL import Image

if TYPE_CHECKING:
    from ultralytics.engine.results import Results


class WheatDetector:
    """Load one local checkpoint and safely share it across Streamlit sessions."""

    def __init__(self, checkpoint: Path) -> None:
        checkpoint = Path(checkpoint).resolve()
        if not checkpoint.is_file():
            raise FileNotFoundError(
                f"The wheat detection model was not found at {checkpoint}. "
                "Restore models/wheat-yolo26n-baseline-v1.pt and restart the app."
            )

        # Check the local file first so a missing checkpoint cannot trigger
        # Ultralytics' automatic model-download behavior.
        from ultralytics import YOLO

        self._model = YOLO(str(checkpoint))
        self._lock = Lock()

    def predict(self, image: Image.Image, confidence: float) -> Results:
        """Detect one RGB image at the selected threshold and return CPU results."""
        confidence = float(confidence)
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0.")
        if image.mode != "RGB":
            raise ValueError("The input image must be converted to RGB before detection.")

        # YOLO updates predictor arguments on each call. Lock the entire call
        # because Streamlit's resource cache shares this instance across sessions.
        with self._lock:
            results = self._model.predict(
                source=image,
                conf=confidence,
                imgsz=640,
                half=False,
                save=False,
                verbose=False,
                stream=False,
            )
            return results[0].cpu()
