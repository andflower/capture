"""
UI 스타일시트 정의 모듈

이 모듈은 애플리케이션에서 사용되는 모든 Qt 스타일시트를 정의합니다.
현대적인 다크 테마를 기반으로 합니다.
"""


class Colors:
    """
    현대적인 다크 테마 색상 팔레트.

    Material Design과 Fluent Design을 참고하여 구성했습니다.

    Attributes:
        PRIMARY: 주 강조색 (인디고)
        SECONDARY: 성공 색상 (에메랄드)
        DANGER: 위험/닫기 색상 (레드)
    """

    # 주요 색상
    PRIMARY: str = "#6366F1"
    PRIMARY_HOVER: str = "#818CF8"
    SECONDARY: str = "#10B981"
    SECONDARY_HOVER: str = "#34D399"
    DANGER: str = "#EF4444"
    DANGER_HOVER: str = "#F87171"

    # 배경 색상
    BG_DARK: str = "#1A1A2E"
    BG_SURFACE: str = "#25253A"
    BG_ELEVATED: str = "#32324A"

    # 테두리
    BORDER_SUBTLE: str = "#3D3D5C"
    BORDER_ACCENT: str = "#6366F1"

    # 텍스트
    TEXT_PRIMARY: str = "#FFFFFF"
    TEXT_SECONDARY: str = "#A0A0C0"
    TEXT_ACCENT: str = "#818CF8"

    # 캡처 영역 (빨간색 유지)
    CAPTURE_BORDER: str = "#EF4444"

    # 레거시 호환 (터미널 스타일)
    TERMINAL_GREEN: str = "#10B981"
    SELECTION_BG: str = "#065F46"


class Styles:
    """
    Qt 스타일시트 상수 클래스.

    각 위젯 유형별로 사용할 스타일시트 문자열을 정의합니다.
    """

    # 컨트롤 바
    CONTROL_BAR: str = f"""
        background-color: {Colors.BG_DARK};
        border-top: 1px solid {Colors.BORDER_SUBTLE};
    """

    # 기본 버튼
    MOVE_BUTTON: str = f"""
        QPushButton {{
            background-color: {Colors.BG_SURFACE};
            color: {Colors.TEXT_PRIMARY};
            border: 1px solid {Colors.BORDER_SUBTLE};
            border-radius: 6px;
            padding: 0px 12px;
            font-weight: 500;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {Colors.BG_ELEVATED};
            border-color: {Colors.PRIMARY};
        }}
        QPushButton:pressed {{
            background-color: {Colors.BG_DARK};
        }}
    """

    # 캡처 버튼 (주요 액션)
    CAPTURE_BUTTON: str = f"""
        QPushButton {{
            background-color: {Colors.PRIMARY};
            color: {Colors.TEXT_PRIMARY};
            border: none;
            border-radius: 6px;
            padding: 0px 20px;
            font-weight: 600;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {Colors.PRIMARY_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {Colors.PRIMARY};
        }}
    """

    # 닫기 버튼 (32x32 정사각형)
    CLOSE_BUTTON: str = f"""
        QPushButton {{
            background-color: transparent;
            color: {Colors.TEXT_SECONDARY};
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 16px;
            padding: 0px;
            margin: 0px;
        }}
        QPushButton:hover {{
            background-color: {Colors.DANGER};
            color: {Colors.TEXT_PRIMARY};
        }}
    """

    # 입력 필드 (터미널 스타일 유지하되 현대화)
    TERMINAL_INPUT: str = f"""
        QLineEdit {{
            background-color: {Colors.BG_SURFACE};
            color: {Colors.TERMINAL_GREEN};
            border: 1px solid {Colors.BORDER_SUBTLE};
            border-radius: 4px;
            padding: 4px 8px;
            font-weight: bold;
            font-size: 14px;
            min-height: 20px;
            selection-background-color: {Colors.SELECTION_BG};
        }}
        QLineEdit:focus {{
            border-color: {Colors.SECONDARY};
        }}
    """

    # 라벨 (터미널 스타일)
    LABEL_TERMINAL: str = (
        f"color: {Colors.TEXT_SECONDARY}; "
        f"font-weight: 500; "
        f"font-size: 14px; "
        f"border: none;"
    )

    # 강조 라벨 (크기 표시용)
    LABEL_ACCENT: str = (
        f"color: {Colors.TERMINAL_GREEN}; "
        f"font-weight: bold; "
        f"font-size: 14px; "
        f"border: none;"
    )

    # 모드 버튼 (토글 스타일)
    MODE_BUTTON: str = f"""
        QPushButton {{
            background-color: {Colors.BG_SURFACE};
            color: {Colors.TEXT_SECONDARY};
            border: 1px solid {Colors.BORDER_SUBTLE};
            border-radius: 6px;
            padding: 0px 12px;
            font-size: 16px;
        }}
        QPushButton:hover {{
            background-color: {Colors.BG_ELEVATED};
            border-color: {Colors.SECONDARY};
            color: {Colors.TEXT_PRIMARY};
        }}
        QPushButton:pressed {{
            background-color: {Colors.BG_DARK};
        }}
    """
