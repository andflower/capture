"""
단축키 도움말 다이얼로그 모듈

F1 키로 표시되는 단축키 도움말을 제공합니다.
"""
from typing import Optional

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QShortcut, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

from ui.styles import Colors, Styles


class HelpDialog(QDialog):
    """
    단축키 도움말 다이얼로그.

    F1 키로 열리며, 사용 가능한 모든 단축키를 표시합니다.

    Attributes:
        parent: 부모 위젯
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        HelpDialog 인스턴스를 초기화합니다.

        Args:
            parent: 부모 위젯
        """
        super().__init__(parent)
        self.setWindowTitle("단축키 도움말")
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowStaysOnTopHint
        )
        self.setMinimumWidth(350)
        self._setup_ui()
        self._setup_shortcuts()

    def _setup_ui(self) -> None:
        """UI를 초기화합니다."""
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {Colors.BG_DARK};
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # 제목
        title = QLabel("<h2>단축키 도움말</h2>")
        title.setStyleSheet(f"color: {Colors.PRIMARY}; font-size: 18px;")
        layout.addWidget(title)

        # 단축키 목록
        shortcuts = [
            ("F1", "도움말 표시/닫기"),
            ("Enter / Space", "캡처 실행"),
            ("Ctrl+C", "클립보드에만 복사"),
            ("Ctrl+S", "파일로만 저장"),
            ("모드 버튼", "저장 모드 변경"),
            ("테두리 드래그", "크기 조절"),
            ("이동 버튼", "윈도우 이동"),
        ]

        help_html = "<table style='font-size: 14px; line-height: 1.8;'>"
        for key, desc in shortcuts:
            help_html += f"""
                <tr>
                    <td style='padding: 6px 24px 6px 0;'>
                        <b style='color: {Colors.SECONDARY};'>{key}</b>
                    </td>
                    <td style='color: {Colors.TEXT_SECONDARY};'>{desc}</td>
                </tr>
            """
        help_html += "</table>"

        content = QLabel(help_html)
        content.setWordWrap(True)
        layout.addWidget(content)

        # 안내 문구
        hint = QLabel("F1 또는 Esc를 눌러 닫기")
        hint.setStyleSheet(f"""
            color: {Colors.TEXT_PRIMARY};
            font-size: 12px;
            padding-top: 8px;
        """)
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)

        # 닫기 버튼
        close_btn = QPushButton("닫기")
        close_btn.setStyleSheet(Styles.CAPTURE_BUTTON)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    def _setup_shortcuts(self) -> None:
        """다이얼로그 단축키를 설정합니다."""
        # F1 또는 Esc로 닫기
        QShortcut(QKeySequence(Qt.Key_F1), self, self.close)
        QShortcut(QKeySequence(Qt.Key_Escape), self, self.close)
