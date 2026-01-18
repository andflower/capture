"""
애플리케이션 전역 상수 정의 모듈

이 모듈은 애플리케이션 전반에서 사용되는 설정값과 상수를 정의합니다.
매직 넘버 사용을 방지하고 유지보수성을 높이기 위해 사용됩니다.
"""
from enum import Enum, auto


class WindowConfig:
    """
    윈도우 관련 설정 상수.

    캡처 윈도우의 크기, 테두리, 컨트롤 바 등의 설정값을 정의합니다.

    Attributes:
        BORDER_WIDTH: 테두리 두께 (픽셀)
        BOTTOM_BAR_HEIGHT: 하단 컨트롤 바 높이 (픽셀)
        MIN_WIDTH: 최소 윈도우 너비 (픽셀)
        MIN_HEIGHT: 최소 윈도우 높이 (픽셀)
        DEFAULT_WIDTH: 기본 윈도우 너비 (픽셀)
        DEFAULT_HEIGHT: 기본 윈도우 높이 (픽셀)
        RESIZE_DETECTION_ZONE: 리사이즈 감지 영역 크기 (픽셀)
    """

    BORDER_WIDTH: int = 5
    BOTTOM_BAR_HEIGHT: int = 48
    MIN_WIDTH: int = 150
    MIN_HEIGHT: int = 150
    DEFAULT_WIDTH: int = 600
    DEFAULT_HEIGHT: int = 500
    RESIZE_DETECTION_ZONE: int = 10


class InputConfig:
    """
    입력 필드 관련 설정 상수.

    Attributes:
        MIN_VALUE: 크기 입력 최소값
        MAX_VALUE: 크기 입력 최대값
        INPUT_WIDTH: 입력 필드 너비 (픽셀)
    """

    MIN_VALUE: int = 10
    MAX_VALUE: int = 9999
    INPUT_WIDTH: int = 50


class ButtonConfig:
    """
    버튼 관련 설정 상수.

    Attributes:
        MOVE_BTN_WIDTH: 이동 버튼 너비 (픽셀)
        CLOSE_BTN_WIDTH: 닫기 버튼 너비 (픽셀) - 1:1 정사각형
        BUTTON_HEIGHT: 공통 버튼 높이 (픽셀)
    """

    MOVE_BTN_WIDTH: int = 75
    CLOSE_BTN_WIDTH: int = 32
    BUTTON_HEIGHT: int = 32


class CaptureMode(Enum):
    """
    캡처 저장 모드.

    캡처된 이미지를 어디에 저장할지 결정합니다.

    Attributes:
        CLIPBOARD_ONLY: 클립보드에만 복사
        FILE_ONLY: 파일로만 저장
        BOTH: 클립보드 복사 + 파일 저장 (기본값)
    """

    CLIPBOARD_ONLY = auto()
    FILE_ONLY = auto()
    BOTH = auto()


class CaptureConfig:
    """
    캡처 관련 설정 상수.

    Attributes:
        DEFAULT_MODE: 기본 캡처 모드
        COPY_TO_CLIPBOARD: 클립보드 자동 복사 여부
        SAVE_TO_FILE: 파일 저장 여부
        SHOW_NOTIFICATION: 알림 표시 여부
        NOTIFICATION_DURATION: 알림 표시 시간 (밀리초)
    """

    DEFAULT_MODE: CaptureMode = CaptureMode.BOTH
    COPY_TO_CLIPBOARD: bool = True
    SAVE_TO_FILE: bool = True
    SHOW_NOTIFICATION: bool = True
    NOTIFICATION_DURATION: int = 2000
