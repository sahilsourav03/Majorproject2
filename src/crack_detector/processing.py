"""Image processing pipeline for crack detection."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, List, Sequence, Tuple

import cv2
import numpy as np

from .config import AnalysisConfig, ProcessingConfig


@dataclass
class Detection:
    bbox: Tuple[int, int, int, int]
    area: float
    confidence: float


class CrackDetector:
    """Detects minor surface cracks using classical OpenCV ops."""

    def __init__(self, proc_cfg: ProcessingConfig, analysis_cfg: AnalysisConfig):
        self.cfg = proc_cfg
        self.analysis_cfg = analysis_cfg
        self.clahe = cv2.createCLAHE(
            clipLimit=self.cfg.clahe_clip_limit,
            tileGridSize=(self.cfg.clahe_grid_size, self.cfg.clahe_grid_size),
        )
        self.history: Deque[int] = deque(maxlen=self.analysis_cfg.history_size)

    def _preprocess(self, frame: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        enhanced = self.clahe.apply(gray)
        blurred = cv2.GaussianBlur(
            enhanced, (self.cfg.gaussian_kernel, self.cfg.gaussian_kernel), 0
        )
        edges = cv2.Canny(
            blurred, self.cfg.canny_threshold1, self.cfg.canny_threshold2
        )
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=self.cfg.dilate_iterations)
        morphed = cv2.erode(dilated, kernel, iterations=self.cfg.erode_iterations)
        return morphed

    def _score(self, area: float, aspect_ratio: float) -> float:
        ar_score = min(1.0, aspect_ratio / self.cfg.min_aspect_ratio)
        area_score = min(1.0, area / (self.cfg.min_contour_area * 4))
        return 0.6 * ar_score + 0.4 * area_score

    def detect(self, frame: np.ndarray) -> List[Detection]:
        mask = self._preprocess(frame)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detections: List[Detection] = []

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < self.cfg.min_contour_area:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            aspect = max(w, h) / max(1, min(w, h))
            if not (self.cfg.min_aspect_ratio <= aspect <= self.cfg.max_aspect_ratio):
                continue
            confidence = self._score(area, aspect)
            if confidence < self.cfg.min_confidence:
                continue
            detections.append(Detection((x, y, w, h), area, confidence))

        self.history.append(len(detections))
        return detections

    def stable_detection(self) -> bool:
        if not self.history:
            return False
        positives = sum(1 for count in self.history if count > 0)
        return positives / len(self.history) >= self.analysis_cfg.trigger_ratio

    def annotate(self, frame: np.ndarray, detections: Sequence[Detection], fps: float) -> np.ndarray:
        annotated = frame.copy()
        for det in detections:
            x, y, w, h = det.bbox
            cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(
                annotated,
                f"crack {det.confidence:.2f}",
                (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                1,
                cv2.LINE_AA,
            )
        if fps > 0:
            cv2.putText(
                annotated,
                f"FPS: {fps:.1f}",
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
        status = "STABLE" if self.stable_detection() else "SCANNING"
        cv2.putText(
            annotated,
            status,
            (10, 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0) if status == "SCANNING" else (0, 165, 255),
            2,
            cv2.LINE_AA,
        )
        return annotated
