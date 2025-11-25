"""Video stream helper for Raspberry Pi cameras."""

from __future__ import annotations

import logging
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
        LOGGER.info("Opening camera index %s", self.cfg.index)
        self._cap = cv2.VideoCapture(self.cfg.index)
        if not self._cap.isOpened():  # pragma: no cover - hardware failure path
            raise RuntimeError("Failed to open camera. Check wiring and permissions.")

        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cfg.width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cfg.height)
        self._cap.set(cv2.CAP_PROP_FPS, self.cfg.fps)
        LOGGER.info(
            "Camera ready at %sx%s @ %sfps",
            self.cfg.width,
            self.cfg.height,
            self.cfg.fps,
        )

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
