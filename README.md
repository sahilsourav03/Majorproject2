# Raspberry Pi Crack Detection

A lightweight Python project for Raspberry Pi that captures a live video feed from a CSI or USB camera, runs OpenCV-based image processing, and highlights minor surface cracks in real time. The processing pipeline is intentionally simple so it can run on constrained hardware while still being easy to tune.

## Features
- Works with `cv2.VideoCapture` so it supports PiCam (via Picamera2) and USB webcams.
- Configurable preprocessing (CLAHE, blur, adaptive threshold) geared toward faint cracks.
- Morphological filtering and contour heuristics to reduce noise.
- On-screen overlays showing detected crack segments with confidence scores.
- Modular architecture ready for future ML models or notification hooks.

## Requirements
- Raspberry Pi 4 (recommended) running Raspberry Pi OS Bullseye or newer.
- Camera connected via CSI ribbon or USB.
- Python 3.9+ with OpenCV (`opencv-python` or `opencv-python-headless`), NumPy, and PyYAML.

## Quick Start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.crack_detector.main --config configs/default.yaml
```

Inside the viewer window, press `q` to stop the stream. Crack detections print to the console and are outlined in red on the preview.

## Configuration
Edit `configs/default.yaml` (or supply another path via `--config`). Key options:
- `camera.index`: camera device (0 for default USB, `libcamerasrc` index for Picamera2).
- `camera.width` / `height`: capture resolution.
- `processing` block: thresholds, kernel sizes, and minimum contour sizes.
- `display` block: toggle overlays and FPS text.

## Project Layout
```
├── README.md
├── requirements.txt
├── configs/
│   └── default.yaml
└── src/
    └── crack_detector/
        ├── __init__.py
        ├── config.py
        ├── camera.py
        ├── processing.py
        └── main.py
```

## Next Steps
- Swap out `CrackDetector` with a learned model (e.g., TensorFlow Lite) if higher accuracy is needed.
- Add alerting hooks (MQTT, email) inside `main.py` when detections cross a threshold.
- Persist detections by timestamp for later review.
