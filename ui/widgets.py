"""
커스텀 위젯 모듈

이 모듈은 애플리케이션에서 사용되는 커스텀 Qt 위젯을 정의합니다.
"""
from typing import Optional

from PyQt5.QtWidgets import QLineEdit, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QFocusEvent

from constants import InputConfig
from ui.styles import Styles


class SilentLineEdit(QLineEdit):
    """
    숫자 입력 전용 커스텀 라인 에디트 위젯.

    터미널 스타일의 투명 배경과 초록색(#00FF00) 텍스트를 제공합니다.
    포커스를 받으면 자동으로 전체 텍스트가 선택되어 바로 수정할 수 있습니다.

    Attributes:
        MIN_VALUE: 최소 허용 값
        MAX_VALUE: 최대 허용 값

    Example:
        >>> edit = SilentLineEdit()
        >>> edit.setText("500")
        >>> edit.setFixedWidth(50)
    """

    MIN_VALUE: int = InputConfig.MIN_VALUE
    MAX_VALUE: int = InputConfig.MAX_VALUE

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        SilentLineEdit 인스턴스를 초기화합니다.

        Args:
            parent: 부모 위젯 (선택사항)
        """
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기 설정을 수행합니다."""
        self.setFrame(False)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(Styles.TERMINAL_INPUT)
        self.setValidator(QIntValidator(self.MIN_VALUE, self.MAX_VALUE))

    def focusInEvent(self, event: QFocusEvent) -> None:
        """
        포커스 진입 이벤트를 처리합니다.

        포커스를 받으면 전체 텍스트를 선택하여
        사용자가 바로 새 값을 입력할 수 있도록 합니다.

        Args:
            event: 포커스 이벤트 객체
        """
        super().focusInEvent(event)
        self.selectAll()
