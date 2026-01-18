"""
스크린 캡처 로직 모듈

이 모듈은 화면 캡처 기능을 제공합니다.
UI 로직과 분리되어 독립적으로 사용할 수 있습니다.
MSS를 사용하여 멀티 모니터 환경을 지원합니다.
"""
import datetime
import logging
from io import BytesIO
from pathlib import Path
from typing import Tuple, Optional

import mss
from PIL import Image as PILImage
from PIL.Image import Image
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage

logger = logging.getLogger(__name__)


class ScreenCapture:
    """
    스크린 캡처 기능을 제공하는 클래스.

    지정된 화면 영역을 캡처하고 파일로 저장하는 기능을 제공합니다.

    Attributes:
        DEFAULT_FORMAT: 기본 파일명 형식
        TIMESTAMP_FORMAT: 타임스탬프 형식

    Example:
        >>> capturer = ScreenCapture()
        >>> result = capturer.capture_and_save((0, 0, 800, 600))
        >>> print(result)
        capture_20260118_143022.png
    """

    DEFAULT_FORMAT: str = "capture_{timestamp}.png"
    TIMESTAMP_FORMAT: str = "%Y%m%d_%H%M%S"

    def __init__(self, output_dir: Optional[Path] = None) -> None:
        """
        ScreenCapture 인스턴스를 초기화합니다.

        Args:
            output_dir: 캡처 이미지 저장 디렉토리 (None이면 현재 디렉토리)
        """
        self.output_dir: Path = output_dir or Path.cwd()

    def capture_region(
        self,
        bbox: Tuple[int, int, int, int]
    ) -> Optional[Image]:
        """
        지정된 영역을 캡처합니다.

        MSS 라이브러리를 사용하여 멀티 모니터 환경에서도
        음수 좌표를 정확히 처리합니다.

        Args:
            bbox: 캡처 영역 (left, top, right, bottom)

        Returns:
            Optional[Image]: 캡처된 이미지 또는 None (실패 시)
        """
        try:
            left, top, right, bottom = bbox
            region = {
                'left': left,
                'top': top,
                'width': right - left,
                'height': bottom - top
            }

            with mss.mss() as sct:
                screenshot = sct.grab(region)
                # BGRA → RGB 변환
                img = PILImage.frombytes(
                    'RGB',
                    screenshot.size,
                    screenshot.bgra,
                    'raw',
                    'BGRX'
                )

            logger.debug(f"캡처 성공: bbox={bbox}")
            return img
        except Exception as e:
            logger.error(f"캡처 실패: {e}")
            return None

    def save_capture(self, image: Image) -> Optional[Path]:
        """
        캡처된 이미지를 파일로 저장합니다.

        Args:
            image: 저장할 이미지

        Returns:
            Optional[Path]: 저장된 파일 경로 또는 None (실패 시)
        """
        timestamp = datetime.datetime.now().strftime(self.TIMESTAMP_FORMAT)
        filename = self.DEFAULT_FORMAT.format(timestamp=timestamp)
        filepath = self.output_dir / filename

        try:
            image.save(str(filepath))
            logger.info(f"캡처 저장 완료: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"저장 실패: {e}")
            return None

    def copy_to_clipboard(self, image: Image) -> bool:
        """
        PIL 이미지를 클립보드에 복사합니다.

        Args:
            image: 복사할 PIL Image 객체

        Returns:
            bool: 복사 성공 여부
        """
        try:
            # PIL Image → PNG 바이트로 변환
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            buffer.seek(0)

            # 바이트 → QImage 변환
            qimage = QImage()
            qimage.loadFromData(buffer.getvalue())

            # 클립보드에 복사
            clipboard = QApplication.clipboard()
            clipboard.setImage(qimage)

            logger.info("클립보드에 이미지 복사 완료")
            return True
        except Exception as e:
            logger.error(f"클립보드 복사 실패: {e}")
            return False

    def capture_and_save(
        self,
        bbox: Tuple[int, int, int, int],
        copy_to_clipboard: bool = True,
        save_to_file: bool = True
    ) -> Tuple[Optional[Path], bool]:
        """
        영역을 캡처하고 파일 저장 및 클립보드 복사를 수행합니다.

        Args:
            bbox: 캡처 영역 (left, top, right, bottom)
            copy_to_clipboard: 클립보드에 복사 여부
            save_to_file: 파일로 저장 여부

        Returns:
            Tuple[Optional[Path], bool]: (저장된 파일 경로, 클립보드 복사 성공 여부)
        """
        image = self.capture_region(bbox)
        if image is None:
            return (None, False)

        file_path: Optional[Path] = None
        clipboard_ok: bool = False

        # 클립보드 복사
        if copy_to_clipboard:
            clipboard_ok = self.copy_to_clipboard(image)

        # 파일 저장
        if save_to_file:
            file_path = self.save_capture(image)

        return (file_path, clipboard_ok)
