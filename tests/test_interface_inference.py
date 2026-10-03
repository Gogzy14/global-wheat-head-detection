"""Check the local checkpoint and confidence boundaries without loading weights."""

import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from PIL import Image

from src.interface_inference import WheatDetector


def test_missing_checkpoint_never_constructs_yolo(tmp_path, monkeypatch) -> None:
    yolo = Mock()
    monkeypatch.setitem(sys.modules, "ultralytics", SimpleNamespace(YOLO=yolo))

    with pytest.raises(FileNotFoundError, match="wheat-yolo26n-baseline-v1.pt"):
        WheatDetector(tmp_path / "wheat-yolo26n-baseline-v1.pt")

    yolo.assert_not_called()


@pytest.fixture
def detector_with_model(tmp_path, monkeypatch):
    checkpoint = tmp_path / "wheat-yolo26n-baseline-v1.pt"
    checkpoint.write_bytes(b"checkpoint placeholder; YOLO is mocked")
    model = Mock()
    yolo = Mock(return_value=model)
    monkeypatch.setitem(sys.modules, "ultralytics", SimpleNamespace(YOLO=yolo))
    return WheatDetector(checkpoint), model


@pytest.mark.parametrize("confidence", [0.0, 0.37, 1.0])
def test_selected_confidence_is_forwarded_exactly(detector_with_model, confidence) -> None:
    detector, model = detector_with_model
    cpu_result = object()
    model.predict.return_value = [SimpleNamespace(cpu=lambda: cpu_result)]

    result = detector.predict(Image.new("RGB", (16, 16)), confidence)

    assert model.predict.call_args.kwargs["conf"] == confidence
    assert result is cpu_result


@pytest.mark.parametrize("confidence", [-0.01, 1.01, float("nan"), float("inf")])
def test_invalid_confidence_does_not_run_inference(detector_with_model, confidence) -> None:
    detector, model = detector_with_model

    with pytest.raises(ValueError, match="Confidence must be between"):
        detector.predict(Image.new("RGB", (16, 16)), confidence)

    model.predict.assert_not_called()
