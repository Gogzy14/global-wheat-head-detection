"""Local image inference with the preserved wheat-head detection model."""

from __future__ import annotations

import logging
from pathlib import Path

import streamlit as st
from PIL import Image, ImageOps, UnidentifiedImageError

from src.interface_inference import WheatDetector


PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_ROOT / "models" / "wheat-yolo26n-baseline-v1.pt"
LOGGER = logging.getLogger(__name__)


@st.cache_resource(show_spinner=False)
def get_detector(checkpoint: str) -> WheatDetector:
    """Keep the saved model in memory between button clicks."""
    return WheatDetector(Path(checkpoint))


def clear_detection() -> None:
    """An old prediction must never appear under new input settings."""
    st.session_state.pop("detection", None)


def empty_image(message: str, detail: str) -> None:
    # Only app-owned text is passed here, never an uploaded filename.
    st.html(
        f'<div class="empty-image"><div class="image-symbol">▧</div>'
        f'<strong>{message}</strong><span>{detail}</span></div>'
    )


def main() -> None:
    st.set_page_config(
        page_title="Global Wheat Head Detection",
        page_icon="🌾",
        layout="wide",
    )

    st.html(f"<style>{(PROJECT_ROOT / 'interface.css').read_text(encoding='utf-8')}</style>")
    st.html(
        '<header class="wheat-header">'
        '<div class="eyebrow">GLOBAL WHEAT HEAD DATASET</div>'
        '<h1>Wheat Head <span>Detection</span></h1>'
        '<p>Find and count wheat heads in your field images.</p>'
        '<div class="model-badges"><span>YOLO26n</span><span>baseline-v1</span>'
        '<span class="local-badge">Local inference</span></div>'
        '</header>'
    )

    with st.tabs(["Image"])[0]:
        input_column, result_column = st.columns(2, gap="medium")

        with input_column:
            preview = None
            with st.container(border=True, key="upload_panel"):
                st.markdown("**Upload image**")
                image_area = st.empty()
                uploaded_image = st.file_uploader(
                    "Upload an image",
                    type=["jpg", "jpeg", "png", "webp"],
                    label_visibility="collapsed",
                    key="uploaded_image",
                    on_change=clear_detection,
                    help="Choose one JPG, PNG, or WebP image, up to 20 MB.",
                )
                with image_area.container():
                    if uploaded_image is not None:
                        try:
                            with Image.open(uploaded_image) as source:
                                preview = ImageOps.exif_transpose(source).convert("RGB")
                            st.image(preview, width="stretch", alt="Uploaded field image")
                        except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
                            clear_detection()
                            st.error("This image could not be opened. Please choose another file.")
                    else:
                        clear_detection()
                        empty_image("Upload a field image", "JPG, PNG or WebP · Up to 20 MB")

            with st.container(border=True, key="settings_panel"):
                confidence = st.slider(
                    "Confidence threshold",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.25,
                    step=0.01,
                    key="confidence_threshold",
                    on_change=clear_detection,
                    help="A higher threshold keeps only predictions with higher confidence.",
                )
                label_column, confidence_column = st.columns(2)
                show_labels = label_column.checkbox("Show labels", value=True)
                show_confidence = confidence_column.checkbox(
                    "Show confidence", value=True,
                    help="Display a confidence value on each detected box.",
                )
                st.caption("Model: wheat-yolo26n-baseline-v1 · Image size: 640")

            detect_clicked = st.button(
                "Detect wheat heads", type="primary", disabled=preview is None, width="stretch"
            )
            if detect_clicked and preview is not None:
                clear_detection()
                try:
                    with st.spinner("Detecting wheat heads…"):
                        detector = get_detector(str(MODEL_PATH))
                        st.session_state.detection = detector.predict(preview, confidence)
                except FileNotFoundError:
                    st.error("The saved model is missing. Restore models/wheat-yolo26n-baseline-v1.pt.")
                except Exception:
                    LOGGER.exception("Wheat-head inference failed")
                    st.error("Detection failed. Try another image or restart the local app.")

        with result_column:
            detection = st.session_state.get("detection")
            with st.container(border=True, key="result_panel"):
                st.markdown("**Result**")
                if detection is None:
                    empty_image("Your result will appear here", "Upload an image, then select Detect wheat heads")
                else:
                    st.image(
                        detection.plot(labels=show_labels, conf=show_confidence, line_width=2),
                        channels="BGR",
                        width="stretch",
                        alt="Field image with detected wheat heads marked by bounding boxes",
                    )
                st.caption("Bounding boxes mark the wheat heads detected by the model.")

            with st.container(border=True, key="summary_panel"):
                count_column, threshold_column = st.columns(2)
                count = len(detection.boxes) if detection is not None else None
                count_column.metric("Wheat heads detected", count if count is not None else "—")
                threshold_column.metric("Confidence threshold", f"{confidence:.2f}")
                if count == 0:
                    st.info("No wheat heads found at this threshold. Try lowering it.")
                st.caption("The count is a model estimate and may include missed or incorrect detections.")

    st.caption("Global Wheat Head Detection · Powered by Ultralytics YOLO and Streamlit")


if __name__ == "__main__":
    main()
