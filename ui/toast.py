"""
토스트 알림 위젯 모듈

캡처 완료 등의 피드백을 사용자에게 표시합니다.
"""
from typing import Optional

from PyQt5.QtWidgets import QLabel, QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont


class Toast(QLabel):
    """
    토스트 알림 위젯.

    화면 하단에 잠시 표시되었다가 사라지는 알림 메시지를 제공합니다.

    Example:
        >>> toast = Toast(parent_widget)
        >>> toast.show_message("캡처가 클립보드에 복사되었습니다!", 2000)
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Toast 인스턴스를 초기화합니다.

        Args:
            parent: 부모 위젯
        """
        super().__init__(parent)
        self._setup_ui()
        self._setup_animation()

    def _setup_ui(self) -> None:
        """UI 초기 설정을 수행합니다."""
        self.setAlignment(Qt.AlignCenter)
        self._apply_style(success=True)
        self.setFont(QFont("Segoe UI", 10))
        self.hide()

    def _apply_style(self, success: bool = True) -> None:
        """
        스타일을 적용합니다.

        Args:
            success: 성공 메시지 여부
        """
        bg_color = "rgba(16, 185, 129, 230)" if success else "rgba(239, 68, 68, 230)"
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 500;
            }}
        """)

    def _setup_animation(self) -> None:
        """애니메이션 설정을 수행합니다."""
        # 투명도 효과
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity_effect)
        self._opacity_effect.setOpacity(1.0)

        # 페이드 아웃 애니메이션
        self._fade_animation = QPropertyAnimation(self._opacity_effect, b"opacity")
        self._fade_animation.setDuration(300)
        self._fade_animation.setStartValue(1.0)
        self._fade_animation.setEndValue(0.0)
        self._fade_animation.setEasingCurve(QEasingCurve.OutQuad)
        self._fade_animation.finished.connect(self.hide)

        # 자동 숨김 타이머
        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._start_fade_out)

    def _start_fade_out(self) -> None:
        """페이드 아웃 애니메이션을 시작합니다."""
        self._fade_animation.start()

    def _position_toast(self) -> None:
        """토스트를 부모 위젯 중앙 하단에 위치시킵니다."""
        if self.parent():
            parent = self.parent()
            x = (parent.width() - self.width()) // 2
            y = parent.height() - self.height() - 60
            self.move(x, y)

    def show_message(
        self,
        message: str,
        duration: int = 2000,
        success: bool = True
    ) -> None:
        """
        토스트 메시지를 표시합니다.

        Args:
            message: 표시할 메시지
            duration: 표시 시간 (밀리초)
            success: 성공 메시지 여부 (색상 변경)
        """
        # 이전 애니메이션 중지
        self._fade_animation.stop()
        self._hide_timer.stop()

        # 스타일 및 메시지 설정
        self._apply_style(success)
        self.setText(message)
        self.adjustSize()

        # 위치 설정
        self._position_toast()

        # 표시
        self._opacity_effect.setOpacity(1.0)
        self.show()
        self.raise_()

        # 타이머 시작
        self._hide_timer.start(duration)
