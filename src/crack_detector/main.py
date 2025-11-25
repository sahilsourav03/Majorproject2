"""Entry point for running the crack detector."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Optional

import cv2

from .camera import VideoStream
from .config import AppConfig
from .processing import CrackDetector

LOGGER = logging.getLogger("crack_detector")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Realtime crack detection")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/default.yaml"),
        help="Path to YAML config file",
    )
    parser.add_argument(
        "--no-window",
        action="store_true",
        help="Disable the OpenCV preview window",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Python logging level (default: INFO)",
    )
    return parser


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def run(config_path: Path, no_window: bool) -> None:
    cfg = AppConfig.from_yaml(config_path)
    if no_window:
        cfg.display.show_window = False

    detector = CrackDetector(cfg.processing, cfg.analysis)

    with VideoStream(cfg.camera) as stream:
        try:
            while True:
                ok, frame = stream.read()
                if not ok:
                    LOGGER.warning("Camera frame read failed; retrying...")
                    continue

                detections = detector.detect(frame)
                if detections:
                    for det in detections:
                        LOGGER.info(
                            "Crack detected area=%.1f confidence=%.2f bbox=%s",
                            det.area,
                            det.confidence,
                            det.bbox,
                        )

                output = frame
                if cfg.display.annotate:
                    output = detector.annotate(frame, detections, stream.get_fps())

                if cfg.display.show_window:
                    cv2.imshow("Crack Monitor", output)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        LOGGER.info("Exit requested by user")
                        break
        except KeyboardInterrupt:
            LOGGER.info("Stopping due to keyboard interrupt")
        finally:
            if cfg.display.show_window:
                cv2.destroyAllWindows()


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    setup_logging(args.log_level)
    run(args.config, args.no_window)


if __name__ == "__main__":  # pragma: no cover
    main()
