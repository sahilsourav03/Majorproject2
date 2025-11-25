"""Configuration helpers for the crack detection pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

import yaml


@dataclass
class CameraConfig:
    index: int = 0
    width: int = 1280
    height: int = 720
    fps: int = 30


@dataclass
class ProcessingConfig:
    clahe_clip_limit: float = 2.0
    clahe_grid_size: int = 8
    gaussian_kernel: int = 5
    canny_threshold1: int = 40
    canny_threshold2: int = 100
    dilate_iterations: int = 1
    erode_iterations: int = 1
    min_contour_area: int = 50
    min_aspect_ratio: float = 2.5
    max_aspect_ratio: float = 50.0
    min_confidence: float = 0.35


@dataclass
class AnalysisConfig:
    history_size: int = 15
    trigger_ratio: float = 0.3


@dataclass
class DisplayConfig:
    show_window: bool = True
    annotate: bool = True
    show_fps: bool = True


@dataclass
class AppConfig:
    camera: CameraConfig = field(default_factory=CameraConfig)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    analysis: AnalysisConfig = field(default_factory=AnalysisConfig)
    display: DisplayConfig = field(default_factory=DisplayConfig)

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "AppConfig":
        def build(section: str, model):
            data = raw.get(section, {})
            return model(**data)

        return cls(
            camera=build("camera", CameraConfig),
            processing=build("processing", ProcessingConfig),
            analysis=build("analysis", AnalysisConfig),
            display=build("display", DisplayConfig),
        )

    @classmethod
    def from_yaml(cls, path: Path | str) -> "AppConfig":
        path = Path(path)
        with path.open("r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh) or {}
        return cls.from_dict(raw)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "camera": self.camera.__dict__,
            "processing": self.processing.__dict__,
            "analysis": self.analysis.__dict__,
            "display": self.display.__dict__,
        }
