from pathlib import Path

import streamlit as st
from PIL import Image

from src.image_processor.core import ImageProcessor, ProcessingOptions


st.set_page_config(page_title="Image Processing Studio", page_icon="🖼️", layout="wide")

st.title("Image Processing Studio")
st.caption("Professional image processing tool built with Python")

processor = ImageProcessor(output_dir="output")

with st.sidebar:
    st.header("Controls")
    grayscale = st.checkbox("Convert to grayscale")
    resize_width = st.number_input("Resize width", min_value=1, max_value=5000, value=0)
    resize_height = st.number_input("Resize height", min_value=1, max_value=5000, value=0)
    rotate = st.slider("Rotate", min_value=-180, max_value=180, value=0)
    brightness = st.slider("Brightness", min_value=0.1, max_value=3.0, value=1.0, step=0.1)
    contrast = st.slider("Contrast", min_value=0.1, max_value=3.0, value=1.0, step=0.1)
    blur = st.slider("Blur", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
    sharpen = st.checkbox("Sharpen")
    edge = st.checkbox("Edge detection")
    threshold = st.slider("Threshold", min_value=0, max_value=255, value=0, step=1)

uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "bmp", "webp"])

if uploaded_image is not None:
    input_path = Path("temp_upload.png")
    input_path.write_bytes(uploaded_image.getvalue())
    original_image = Image.open(input_path)
    st.image(original_image, caption="Original Image", use_column_width=True)

    options = ProcessingOptions(
        grayscale=grayscale,
        resize_width=None if resize_width == 0 else int(resize_width),
        resize_height=None if resize_height == 0 else int(resize_height),
        rotate=int(rotate),
        brightness=float(brightness),
        contrast=float(contrast),
        blur=float(blur),
        sharpen=sharpen,
        edge=edge,
        threshold=None if threshold == 0 else int(threshold),
    )

    processed = processor.process(original_image, options)

    st.image(processed, caption="Processed Image", use_column_width=True)

    output_name = "processed_output.png"
    output_path = processor.save_image(processed, output_name)

    with open(output_path, "rb") as file:
        btn = st.download_button(
            label="Download processed image",
            data=file,
            file_name=output_name,
            mime="image/png",
        )

    st.success(f"Output saved to: {output_path}")
else:
    st.info("Please upload an image to begin processing.")
