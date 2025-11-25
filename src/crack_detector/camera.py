"""Video stream helper for Raspberry Pi cameras."""

from __future__ import annotations

import logging
import platform
import time
from typing import Optional, Tuple

import cv2

from .config import CameraConfig

LOGGER = logging.getLogger(__name__)


class VideoStream:
    """Simple wrapper around cv2.VideoCapture with context-manager support."""

    def __init__(self, cfg: CameraConfig):
        self.cfg = cfg
        self._cap: Optional[cv2.VideoCapture] = None
        self._last_ts = time.time()
        self._fps = 0.0

    def open(self) -> None:
        # Detect OS and handle camera access accordingly
        system = platform.system()
        is_linux = system == "Linux"

        if is_linux:
            # On Linux/Raspberry Pi: convert index to device path
            try:
                idx = int(self.cfg.index)
                device = f"/dev/video{idx}"
            except Exception:
                device = str(self.cfg.index)

            LOGGER.info("Opening camera device %s using V4L2 backend...", device)

            # Open with explicit V4L2 backend (Linux/Raspberry Pi)
            self._cap = cv2.VideoCapture(device, cv2.CAP_V4L2)
            if not self._cap.isOpened():
                LOGGER.error("Failed opening camera with V4L2. Retrying with ANY backend...")
                self._cap = cv2.VideoCapture(device)
        else:
            # On macOS/Windows: use index directly
            device = self.cfg.index
            LOGGER.info("Opening camera index %s...", device)
            self._cap = cv2.VideoCapture(device)

        if not self._cap.isOpened():
            raise RuntimeError("Failed to open camera. Check wiring, USB port, permissions.")

        # Apply working resolution + fps
        width = getattr(self.cfg, "width", 1280)
        height = getattr(self.cfg, "height", 720)
        fps = getattr(self.cfg, "fps", 15)

        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self._cap.set(cv2.CAP_PROP_FPS, fps)

        # Warm up camera
        time.sleep(0.5)

        # Verify first frame
        ok = False
        for _ in range(5):
            ret, frame = self._cap.read()
            if ret and frame is not None:
                ok = True
                break
            time.sleep(0.1)

        if not ok:
            LOGGER.error("Camera opened but no frames could be read.")
            self._cap.release()
            self._cap = None
            raise RuntimeError("Camera failed to deliver frames after open()")

        LOGGER.info("Camera ready at %sx%s @ %sfps", width, height, fps)

    def read(self) -> Tuple[bool, Optional[cv2.Mat]]:
        if self._cap is None:
            raise RuntimeError("Camera not opened. Call open() first.")

        ok, frame = self._cap.read()
        now = time.time()
        delta = now - self._last_ts
        if delta > 0:
            self._fps = 0.9 * self._fps + 0.1 * (1.0 / delta)
        self._last_ts = now
        return ok, frame

    def release(self) -> None:
        if self._cap is not None:
            LOGGER.info("Releasing camera")
            self._cap.release()
            self._cap = None

    def get_fps(self) -> float:
        return self._fps

    def __enter__(self) -> "VideoStream":
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.release()
