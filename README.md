# Image Processing Studio

A professional Python project for image processing using Pillow, OpenCV, and NumPy.

## Features

- Load and save images
- Resize and rotate
- Convert to grayscale
- Brightness and contrast adjustment
- Blur and sharpening filters
- Edge detection
- Binary thresholding
- Optional Streamlit web interface
- Command-line processing

## Project structure

```text
image-processing-python/
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── output/
├── src/
│   └── image_processor/
│       ├── __init__.py
│       └── core.py
└── sample_images/
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the desktop CLI

```bash
python main.py --input sample_images/example.jpg --grayscale --resize-width 800 --contrast 1.5 --output-dir output
```

## Run the web interface

```bash
streamlit run app.py
```

## Example operations

- `--grayscale`
- `--resize-width 1024`
- `--resize-height 768`
- `--rotate 90`
- `--brightness 1.4`
- `--contrast 1.8`
- `--blur 2.5`
- `--sharpen`
- `--edge`
- `--threshold 120`

## Technologies used

- Python 3.10+
- Pillow
- OpenCV
- NumPy
- Streamlit

## License

MIT
