"""
아이콘 리소스 모듈

유니코드 이모지 및 심볼을 사용하여 아이콘을 관리합니다.
QPainter를 사용한 커스텀 아이콘도 제공합니다.
"""
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint


def create_move_icon(size: int = 24, color: str = "#FFFFFF") -> QIcon:
    """
    이동 버튼용 외부 링크 스타일 아이콘을 생성합니다.

    사각형과 대각선 화살표로 구성된 아이콘입니다.

    Args:
        size: 아이콘 크기 (픽셀)
        color: 아이콘 색상 (hex)

    Returns:
        QIcon: 생성된 아이콘
    """
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    pen = QPen(QColor(color))
    pen.setWidth(2)
    painter.setPen(pen)

    # 여백
    margin = 4
    box_size = size - margin * 2

    # 사각형 (왼쪽 하단 부분만 - ㄴ 모양)
    # 왼쪽 세로선
    painter.drawLine(margin, margin + 4, margin, margin + box_size)
    # 아래쪽 가로선
    painter.drawLine(margin, margin + box_size, margin + box_size - 4, margin + box_size)

    # 대각선 화살표 (오른쪽 위로)
    arrow_start_x = margin + 6
    arrow_start_y = margin + box_size - 6
    arrow_end_x = margin + box_size
    arrow_end_y = margin

    # 화살표 본체 (대각선)
    painter.drawLine(arrow_start_x, arrow_start_y, arrow_end_x, arrow_end_y)

    # 화살표 머리
    arrow_head_size = 5
    painter.drawLine(arrow_end_x, arrow_end_y, arrow_end_x - arrow_head_size, arrow_end_y)
    painter.drawLine(arrow_end_x, arrow_end_y, arrow_end_x, arrow_end_y + arrow_head_size)

    painter.end()

    return QIcon(pixmap)


def create_clipboard_icon(size: int = 24, color: str = "#FFFFFF") -> QIcon:
    """
    클립보드 아이콘을 생성합니다.

    Args:
        size: 아이콘 크기 (픽셀)
        color: 아이콘 색상 (hex)

    Returns:
        QIcon: 생성된 아이콘
    """
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    pen = QPen(QColor(color))
    pen.setWidth(2)
    painter.setPen(pen)

    margin = 3
    w = size - margin * 2
    h = size - margin * 2

    # 클립보드 본체 (사각형)
    painter.drawRect(margin, margin + 4, w, h - 4)

    # 클립 부분 (위쪽 작은 사각형)
    clip_width = w // 2
    clip_x = margin + (w - clip_width) // 2
    painter.drawRect(clip_x, margin, clip_width, 6)

    painter.end()

    return QIcon(pixmap)


def create_file_icon(size: int = 24, color: str = "#FFFFFF") -> QIcon:
    """
    파일/폴더 아이콘을 생성합니다.

    Args:
        size: 아이콘 크기 (픽셀)
        color: 아이콘 색상 (hex)

    Returns:
        QIcon: 생성된 아이콘
    """
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    pen = QPen(QColor(color))
    pen.setWidth(2)
    painter.setPen(pen)

    margin = 3
    w = size - margin * 2
    h = size - margin * 2

    # 폴더 본체
    painter.drawRect(margin, margin + 4, w, h - 4)

    # 폴더 탭 (위쪽)
    tab_width = w // 3
    painter.drawLine(margin, margin + 4, margin + tab_width, margin + 4)
    painter.drawLine(margin + tab_width, margin + 4, margin + tab_width + 3, margin)
    painter.drawLine(margin + tab_width + 3, margin, margin + tab_width + 6, margin)

    painter.end()

    return QIcon(pixmap)


def create_both_icon(size: int = 24, color: str = "#FFFFFF") -> QIcon:
    """
    클립보드+파일 결합 아이콘을 생성합니다.

    Args:
        size: 아이콘 크기 (픽셀)
        color: 아이콘 색상 (hex)

    Returns:
        QIcon: 생성된 아이콘
    """
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    pen = QPen(QColor(color))
    pen.setWidth(1)
    painter.setPen(pen)

    # 왼쪽: 클립보드 (작게)
    margin = 2
    half = size // 2 - 1

    # 클립보드 본체
    painter.drawRect(margin, margin + 3, half - 2, half + 4)
    # 클립
    clip_w = (half - 2) // 2
    clip_x = margin + ((half - 2) - clip_w) // 2
    painter.drawRect(clip_x, margin, clip_w, 4)

    # 오른쪽: 파일 (작게)
    right_x = half + 2
    painter.drawRect(right_x, margin + 3, half - 2, half + 4)
    # 폴더 탭
    tab_w = (half - 2) // 3
    painter.drawLine(right_x, margin + 3, right_x + tab_w, margin + 3)
    painter.drawLine(right_x + tab_w, margin + 3, right_x + tab_w + 2, margin)

    painter.end()

    return QIcon(pixmap)


class Icons:
    """
    애플리케이션 아이콘 상수.

    유니코드 문자를 사용하여 아이콘을 표시합니다.

    Attributes:
        CAPTURE: 캡처 아이콘
        COPY: 복사 아이콘
        SAVE: 저장 아이콘
        CLOSE: 닫기 아이콘
        MOVE: 이동 아이콘
    """

    # 액션 아이콘
    CAPTURE: str = "📷"
    COPY: str = "📋"
    SAVE: str = "💾"
    CLOSE: str = "✕"
    MOVE: str = "✥"
    SETTINGS: str = "⚙"

    # 상태 아이콘
    SUCCESS: str = "✓"
    ERROR: str = "✗"
    INFO: str = "ℹ"
    WARNING: str = "⚠"

    # 모드 아이콘
    CLIPBOARD: str = "📋"
    FILE: str = "📁"
    BOTH: str = "📋📁"

    # 크기 조절 아이콘
    RESIZE_H: str = "↔"
    RESIZE_V: str = "↕"
    RESIZE_DIAG: str = "⤡"
