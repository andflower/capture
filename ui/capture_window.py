"""
메인 캡처 윈도우 모듈

이 모듈은 화면 캡처를 위한 메인 윈도우를 제공합니다.
프레임리스 오버레이 윈도우로 리사이즈 및 이동이 가능합니다.
"""
import logging
from typing import Optional, Tuple

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QSizePolicy, QShortcut
)
from PyQt5.QtCore import Qt, QRect, QPoint, QEvent
from PyQt5.QtGui import QPainter, QPen, QColor, QRegion, QMouseEvent, QKeySequence, QIcon

from constants import WindowConfig, InputConfig, ButtonConfig, CaptureMode, CaptureConfig
from ui.styles import Styles, Colors
from ui.widgets import SilentLineEdit
from ui.toast import Toast
from ui.help_dialog import HelpDialog
from ui.icons import create_move_icon, create_clipboard_icon, create_file_icon, create_both_icon
from core.capture import ScreenCapture

logger = logging.getLogger(__name__)


class FinalCaptureWindow(QWidget):
    """
    메인 캡처 윈도우 위젯.

    프레임리스 투명 오버레이 윈도우로, 화면의 특정 영역을 선택하고
    캡처할 수 있습니다. 테두리 드래그로 크기 조절, 이동 버튼으로 위치 이동,
    캡처 버튼으로 스크린샷 저장이 가능합니다.

    Attributes:
        border_width: 테두리 두께 (픽셀)
        bottom_height: 하단 컨트롤 바 높이 (픽셀)
        min_w: 최소 윈도우 너비 (픽셀)
        min_h: 최소 윈도우 높이 (픽셀)
    """

    def __init__(self) -> None:
        """FinalCaptureWindow 인스턴스를 초기화합니다."""
        super().__init__()

        # 설정 상수
        self.border_width: int = WindowConfig.BORDER_WIDTH
        self.bottom_height: int = WindowConfig.BOTTOM_BAR_HEIGHT
        self.min_w: int = WindowConfig.MIN_WIDTH
        self.min_h: int = WindowConfig.MIN_HEIGHT

        # 상태 변수 (모두 __init__에서 초기화)
        self.resize_mode: Optional[str] = None
        self.is_moving: bool = False
        self.drag_start_pos: QPoint = QPoint()
        self.move_start_pos: QPoint = QPoint()

        # 캡처 헬퍼 및 모드
        self._capturer: ScreenCapture = ScreenCapture()
        self._capture_mode: CaptureMode = CaptureConfig.DEFAULT_MODE

        # UI 위젯 참조 (initUI에서 설정)
        self.edit_width: Optional[SilentLineEdit] = None
        self.edit_height: Optional[SilentLineEdit] = None
        self._toast: Optional[Toast] = None
        self._mode_btn: Optional[QPushButton] = None

        # 윈도우 설정
        self._setup_window()
        self._init_ui()
        self._setup_shortcuts()
        self._update_mask()

    def _setup_window(self) -> None:
        """윈도우 기본 설정을 수행합니다."""
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_Hover)  # 호버 이벤트 활성화
        self.setMouseTracking(True)
        self.resize(WindowConfig.DEFAULT_WIDTH, WindowConfig.DEFAULT_HEIGHT)

    def _init_ui(self) -> None:
        """UI 컴포넌트를 초기화합니다."""
        # 메인 레이아웃
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 상단 투명 공간 (캡처 영역)
        top_spacer = QWidget()
        top_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(top_spacer)

        # 하단 컨트롤 바
        bottom_frame = self._create_bottom_frame()
        layout.addWidget(bottom_frame)

        # 토스트 알림 위젯 초기화
        self._toast = Toast(self)

        # 초기 텍스트 설정
        self._update_info_text()

    def _create_bottom_frame(self) -> QFrame:
        """
        하단 컨트롤 바를 생성합니다.

        Returns:
            QFrame: 컨트롤 바 프레임
        """
        frame = QFrame()
        frame.setStyleSheet(Styles.CONTROL_BAR)
        frame.setFixedHeight(self.bottom_height)

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 0, 8, 0)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignVCenter)  # 모든 위젯 수직 중앙 정렬

        # 크기 정보 위젯 추가
        self._add_size_info_widgets(layout)

        layout.addStretch()

        # 컨트롤 버튼 추가
        self._add_control_buttons(layout)

        return frame

    def _add_size_info_widgets(self, layout: QHBoxLayout) -> None:
        """
        크기 정보 입력 위젯들을 레이아웃에 추가합니다.

        Args:
            layout: 부모 레이아웃
        """
        # 너비 라벨
        lbl_w_prefix = QLabel("너비: ")
        lbl_w_prefix.setStyleSheet(Styles.LABEL_TERMINAL)
        layout.addWidget(lbl_w_prefix)

        # 너비 입력
        self.edit_width = SilentLineEdit()
        self.edit_width.setFixedWidth(InputConfig.INPUT_WIDTH)
        self.edit_width.editingFinished.connect(self._apply_size_from_edit)
        layout.addWidget(self.edit_width)

        # 구분자
        lbl_w_suffix = QLabel("px  x  높이: ")
        lbl_w_suffix.setStyleSheet(Styles.LABEL_TERMINAL)
        layout.addWidget(lbl_w_suffix)

        # 높이 입력
        self.edit_height = SilentLineEdit()
        self.edit_height.setFixedWidth(InputConfig.INPUT_WIDTH)
        self.edit_height.editingFinished.connect(self._apply_size_from_edit)
        layout.addWidget(self.edit_height)

        # 높이 단위
        lbl_h_suffix = QLabel("px")
        lbl_h_suffix.setStyleSheet(Styles.LABEL_TERMINAL)
        layout.addWidget(lbl_h_suffix)

    def _add_control_buttons(self, layout: QHBoxLayout) -> None:
        """
        컨트롤 버튼들을 레이아웃에 추가합니다.

        Args:
            layout: 부모 레이아웃
        """
        # 공통 버튼 높이
        btn_height = ButtonConfig.BUTTON_HEIGHT

        # 모드 전환 버튼
        self._mode_btn = QPushButton()
        self._mode_btn.setIcon(self._get_mode_icon())
        self._mode_btn.setToolTip(self._get_mode_tooltip())
        self._mode_btn.setFixedSize(btn_height, btn_height)  # 정사각형
        self._mode_btn.setStyleSheet(Styles.MODE_BUTTON)
        self._mode_btn.clicked.connect(self._cycle_capture_mode)
        layout.addWidget(self._mode_btn)

        # 이동 버튼 (아이콘 + 텍스트)
        move_btn = QPushButton("이동")
        move_btn.setIcon(create_move_icon(size=18, color=Colors.TEXT_PRIMARY))
        move_btn.setFixedSize(ButtonConfig.MOVE_BTN_WIDTH, btn_height)
        move_btn.setCursor(Qt.SizeAllCursor)
        move_btn.setStyleSheet(Styles.MOVE_BUTTON)
        move_btn.mousePressEvent = self._move_btn_press
        move_btn.mouseMoveEvent = self._move_btn_move
        layout.addWidget(move_btn)

        # 캡처 버튼
        capture_btn = QPushButton("캡쳐")
        capture_btn.setFixedHeight(btn_height)
        capture_btn.clicked.connect(self._capture_screen)
        capture_btn.setStyleSheet(Styles.CAPTURE_BUTTON)
        layout.addWidget(capture_btn)

        # 닫기 버튼 (정사각형)
        close_btn = QPushButton("X")
        close_btn.setFixedSize(btn_height, btn_height)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet(Styles.CLOSE_BUTTON)
        layout.addWidget(close_btn)

    # =========================================================================
    # 마스크 및 그리기
    # =========================================================================

    def _update_mask(self) -> None:
        """윈도우 마스크를 업데이트합니다."""
        w = self.width()
        h = self.height()
        cap_h = h - self.bottom_height
        bw = self.border_width

        # 전체 영역
        full_region = QRegion(0, 0, w, h)

        # 테두리 안쪽을 파냄 (클릭 투과 영역)
        inner_rect = QRect(bw, bw, w - 2 * bw, cap_h - 2 * bw)
        hole_region = QRegion(inner_rect)
        mask_region = full_region.subtracted(hole_region)

        # 십자선 영역 추가
        cx, cy = w // 2, cap_h // 2
        mask_region = mask_region.united(QRegion(cx, 0, 1, cap_h))
        mask_region = mask_region.united(QRegion(0, cy, w, 1))

        self.setMask(mask_region)
        self._update_info_text()

    def paintEvent(self, event) -> None:
        """
        윈도우를 그립니다.

        빨간 테두리와 십자선을 그립니다.
        """
        painter = QPainter(self)
        w = self.width()
        h = self.height()
        cap_h = h - self.bottom_height
        bw = self.border_width

        # 빨간 테두리
        border_color = QColor(Colors.CAPTURE_BORDER)
        pen = QPen(border_color, bw)
        pen.setJoinStyle(Qt.MiterJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        rect_draw = QRect(bw // 2, bw // 2, w - bw, cap_h - bw)
        painter.drawRect(rect_draw)

        # 십자선 (빨간색 1px)
        cross_pen = QPen(border_color, 1)
        painter.setPen(cross_pen)
        cx, cy = w // 2, cap_h // 2
        painter.drawLine(cx, 0, cx, cap_h)
        painter.drawLine(0, cy, w, cy)

    # =========================================================================
    # 정보창 업데이트 및 크기 적용
    # =========================================================================

    def _update_info_text(self) -> None:
        """현재 윈도우 크기를 입력창에 표시합니다."""
        if self.edit_width is None or self.edit_height is None:
            return

        current_w = self.width()
        current_cap_h = self.height() - self.bottom_height

        # 사용자가 입력 중이 아닐 때만 업데이트
        if not self.edit_width.hasFocus():
            self.edit_width.setText(str(current_w))
        if not self.edit_height.hasFocus():
            self.edit_height.setText(str(current_cap_h))

    def _apply_size_from_edit(self) -> None:
        """입력된 크기 값을 윈도우에 적용합니다."""
        if self.edit_width is None or self.edit_height is None:
            return

        try:
            new_w = int(self.edit_width.text())
            new_h = int(self.edit_height.text())

            # 최소 크기 제한
            new_w = max(self.min_w, new_w)
            new_h = max(self.min_h, new_h)

            self.resize(new_w, new_h + self.bottom_height)
            self._update_mask()

        except ValueError as e:
            logger.warning(f"유효하지 않은 크기 입력: {e}")
            # 현재 값으로 복원
            self._update_info_text()

        finally:
            # 포커스 해제
            self.edit_width.clearFocus()
            self.edit_height.clearFocus()

    # =========================================================================
    # 마우스 이벤트 (크기 조절)
    # =========================================================================

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """마우스 버튼 누름 이벤트를 처리합니다."""
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.globalPos()
            self.resize_mode = self._get_resize_mode(event.pos())

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """마우스 이동 이벤트를 처리합니다."""
        # 커서 스타일 변경
        mode = self._get_resize_mode(event.pos())
        self._update_cursor(mode)

        # 크기 조절 동작
        if self.resize_mode and event.buttons() & Qt.LeftButton:
            self._handle_resize(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """마우스 버튼 해제 이벤트를 처리합니다."""
        self.resize_mode = None

    def leaveEvent(self, event) -> None:
        """마우스가 윈도우를 벗어날 때 커서를 복원합니다."""
        self.setCursor(Qt.ArrowCursor)
        super().leaveEvent(event)

    def event(self, event: QEvent) -> bool:
        """
        일반 이벤트를 처리합니다.

        HoverMove 이벤트를 통해 마스킹된 윈도우에서도 커서 변경이 가능하도록 합니다.
        """
        if event.type() == QEvent.HoverMove:
            pos = event.pos()
            mode = self._get_resize_mode(pos)
            self._update_cursor(mode)
        return super().event(event)

    def _update_cursor(self, mode: Optional[str]) -> None:
        """
        리사이즈 모드에 따라 커서를 변경합니다.

        Args:
            mode: 리사이즈 모드 문자열
        """
        if mode is None:
            self.setCursor(Qt.ArrowCursor)
        elif mode in ('top_left', 'bottom_right'):
            self.setCursor(Qt.SizeFDiagCursor)
        elif mode in ('top_right', 'bottom_left'):
            self.setCursor(Qt.SizeBDiagCursor)
        elif 'left' in mode or 'right' in mode:
            self.setCursor(Qt.SizeHorCursor)
        elif 'top' in mode or 'bottom' in mode:
            self.setCursor(Qt.SizeVerCursor)

    def _handle_resize(self, event: QMouseEvent) -> None:
        """
        리사이즈 동작을 처리합니다.

        Args:
            event: 마우스 이벤트
        """
        global_pos = event.globalPos()
        diff = global_pos - self.drag_start_pos
        self.drag_start_pos = global_pos

        geo = self.geometry()
        new_rect = QRect(geo)

        # 가로 조절
        if self.resize_mode and 'right' in self.resize_mode:
            new_rect.setWidth(max(self.min_w, geo.width() + diff.x()))
        if self.resize_mode and 'left' in self.resize_mode:
            new_w = max(self.min_w, geo.width() - diff.x())
            if new_w != geo.width():
                new_rect.setLeft(geo.left() + diff.x())

        # 세로 조절
        if self.resize_mode and 'bottom' in self.resize_mode:
            new_rect.setHeight(
                max(self.min_h + self.bottom_height, geo.height() + diff.y())
            )
        if self.resize_mode and 'top' in self.resize_mode:
            new_h = max(self.min_h + self.bottom_height, geo.height() - diff.y())
            if new_h != geo.height():
                new_rect.setTop(geo.top() + diff.y())

        self.setGeometry(new_rect)
        self._update_mask()

    def _get_resize_mode(self, pos: QPoint) -> Optional[str]:
        """
        마우스 위치에 따른 리사이즈 모드를 반환합니다.

        Args:
            pos: 마우스 위치 (위젯 로컬 좌표)

        Returns:
            Optional[str]: 리사이즈 모드 ('top_left', 'right' 등) 또는 None
        """
        w, h = self.width(), self.height()
        x, y = pos.x(), pos.y()
        detection_zone = WindowConfig.RESIZE_DETECTION_ZONE
        cap_h = h - self.bottom_height

        # 하단 바 영역에서는 리사이즈 비활성화
        if y >= cap_h:
            return None

        mode = ""
        on_top = y < detection_zone
        on_bottom = y > cap_h - detection_zone
        on_left = x < detection_zone
        on_right = x > w - detection_zone

        if on_top:
            mode += "top"
        if on_bottom:
            mode += "bottom"
        if on_left:
            mode += "_left" if mode else "left"
        if on_right:
            mode += "_right" if mode else "right"

        return mode if mode else None

    def resizeEvent(self, event) -> None:
        """윈도우 크기 변경 이벤트를 처리합니다."""
        self._update_mask()
        super().resizeEvent(event)

    # =========================================================================
    # 이동 버튼 및 캡처
    # =========================================================================

    def _move_btn_press(self, event: QMouseEvent) -> None:
        """이동 버튼 마우스 누름 이벤트를 처리합니다."""
        if event.button() == Qt.LeftButton:
            self.is_moving = True
            self.move_start_pos = event.globalPos() - self.frameGeometry().topLeft()

    def _move_btn_move(self, event: QMouseEvent) -> None:
        """이동 버튼 마우스 이동 이벤트를 처리합니다."""
        if self.is_moving and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.move_start_pos)

    def _calculate_capture_bbox(self) -> Tuple[int, int, int, int]:
        """
        캡처할 영역의 bounding box를 계산합니다.

        Returns:
            Tuple[int, int, int, int]: (left, top, right, bottom)
        """
        bw = self.border_width
        x = self.x() + bw
        y = self.y() + bw
        w = self.width() - 2 * bw
        h = (self.height() - self.bottom_height) - 2 * bw
        return (x, y, x + w, y + h)

    def _capture_screen(self) -> None:
        """현재 캡처 모드에 따라 캡처를 수행합니다."""
        self.hide()
        QApplication.processEvents()

        # 현재 모드에 따른 옵션 설정
        copy_clipboard = self._capture_mode in (
            CaptureMode.CLIPBOARD_ONLY, CaptureMode.BOTH
        )
        save_file = self._capture_mode in (
            CaptureMode.FILE_ONLY, CaptureMode.BOTH
        )

        bbox = self._calculate_capture_bbox()
        file_path, clipboard_ok = self._capturer.capture_and_save(
            bbox,
            copy_to_clipboard=copy_clipboard,
            save_to_file=save_file
        )

        self.show()

        # 결과에 따른 토스트 알림
        if self._toast:
            if self._capture_mode == CaptureMode.BOTH:
                if file_path and clipboard_ok:
                    self._toast.show_message(
                        "캡처 완료! 클립보드 + 파일",
                        duration=2000,
                        success=True
                    )
                    logger.info(f"캡처 성공: {file_path}")
                elif clipboard_ok:
                    self._toast.show_message(
                        "클립보드에 복사됨 (파일 저장 실패)",
                        duration=2000,
                        success=True
                    )
                elif file_path:
                    self._toast.show_message(
                        f"저장됨: {file_path.name} (클립보드 실패)",
                        duration=2000,
                        success=True
                    )
                else:
                    self._toast.show_message("캡처 실패", duration=2000, success=False)
                    logger.error("캡처 실패")
            elif self._capture_mode == CaptureMode.CLIPBOARD_ONLY:
                if clipboard_ok:
                    self._toast.show_message(
                        "클립보드에 복사됨",
                        duration=2000,
                        success=True
                    )
                else:
                    self._toast.show_message("복사 실패", duration=2000, success=False)
            elif self._capture_mode == CaptureMode.FILE_ONLY:
                if file_path:
                    self._toast.show_message(
                        f"저장됨: {file_path.name}",
                        duration=2000,
                        success=True
                    )
                else:
                    self._toast.show_message("저장 실패", duration=2000, success=False)

    # =========================================================================
    # 단축키 설정
    # =========================================================================

    def _setup_shortcuts(self) -> None:
        """
        키보드 단축키를 설정합니다.

        단축키 목록:
            - Enter/Return: 캡처 실행
            - Space: 캡처 실행
            - Ctrl+C: 클립보드에만 복사 (일시 모드)
            - Ctrl+S: 파일로만 저장 (일시 모드)
            - F1: 도움말 표시
        """
        # Enter: 캡처
        QShortcut(QKeySequence(Qt.Key_Return), self, self._capture_screen)

        # Space: 캡처
        QShortcut(QKeySequence(Qt.Key_Space), self, self._capture_screen)

        # Ctrl+C: 클립보드에만 복사
        QShortcut(
            QKeySequence(Qt.CTRL + Qt.Key_C),
            self,
            self._capture_clipboard_only
        )

        # Ctrl+S: 파일로만 저장
        QShortcut(
            QKeySequence(Qt.CTRL + Qt.Key_S),
            self,
            self._capture_file_only
        )

        # F1: 도움말
        QShortcut(QKeySequence(Qt.Key_F1), self, self._show_help)

    def _capture_clipboard_only(self) -> None:
        """클립보드에만 복사하는 캡처를 실행합니다."""
        self.hide()
        QApplication.processEvents()

        bbox = self._calculate_capture_bbox()
        _, clipboard_ok = self._capturer.capture_and_save(
            bbox,
            copy_to_clipboard=True,
            save_to_file=False
        )

        self.show()

        if self._toast:
            if clipboard_ok:
                self._toast.show_message(
                    "클립보드에 복사됨",
                    duration=2000,
                    success=True
                )
            else:
                self._toast.show_message(
                    "클립보드 복사 실패",
                    duration=2000,
                    success=False
                )

    def _capture_file_only(self) -> None:
        """파일로만 저장하는 캡처를 실행합니다."""
        self.hide()
        QApplication.processEvents()

        bbox = self._calculate_capture_bbox()
        file_path, _ = self._capturer.capture_and_save(
            bbox,
            copy_to_clipboard=False,
            save_to_file=True
        )

        self.show()

        if self._toast:
            if file_path:
                self._toast.show_message(
                    f"저장됨: {file_path.name}",
                    duration=2000,
                    success=True
                )
            else:
                self._toast.show_message(
                    "파일 저장 실패",
                    duration=2000,
                    success=False
                )

    # =========================================================================
    # 캡처 모드 관리
    # =========================================================================

    def _get_mode_icon(self) -> QIcon:
        """
        현재 캡처 모드에 해당하는 아이콘을 반환합니다.

        Returns:
            QIcon: 모드 아이콘
        """
        icon_size = 18
        icon_color = Colors.TEXT_PRIMARY

        if self._capture_mode == CaptureMode.CLIPBOARD_ONLY:
            return create_clipboard_icon(icon_size, icon_color)
        elif self._capture_mode == CaptureMode.FILE_ONLY:
            return create_file_icon(icon_size, icon_color)
        else:  # BOTH
            return create_both_icon(icon_size, icon_color)

    def _get_mode_tooltip(self) -> str:
        """
        현재 캡처 모드에 대한 툴팁을 반환합니다.

        Returns:
            str: 모드 설명 문자열
        """
        mode_tooltips = {
            CaptureMode.CLIPBOARD_ONLY: "클립보드만 (클릭하여 변경)",
            CaptureMode.FILE_ONLY: "파일만 (클릭하여 변경)",
            CaptureMode.BOTH: "클립보드 + 파일 (클릭하여 변경)",
        }
        return mode_tooltips.get(self._capture_mode, "")

    def _cycle_capture_mode(self) -> None:
        """캡처 모드를 순환합니다 (BOTH → CLIPBOARD → FILE → BOTH)."""
        mode_cycle = {
            CaptureMode.BOTH: CaptureMode.CLIPBOARD_ONLY,
            CaptureMode.CLIPBOARD_ONLY: CaptureMode.FILE_ONLY,
            CaptureMode.FILE_ONLY: CaptureMode.BOTH,
        }
        self._capture_mode = mode_cycle.get(self._capture_mode, CaptureMode.BOTH)
        self._update_mode_button()

        # 토스트로 모드 변경 알림
        if self._toast:
            mode_names = {
                CaptureMode.CLIPBOARD_ONLY: "클립보드만",
                CaptureMode.FILE_ONLY: "파일만",
                CaptureMode.BOTH: "클립보드 + 파일",
            }
            self._toast.show_message(
                f"모드: {mode_names.get(self._capture_mode, '')}",
                duration=1000,
                success=True
            )

    def _update_mode_button(self) -> None:
        """모드 버튼의 아이콘과 툴팁을 업데이트합니다."""
        if self._mode_btn:
            self._mode_btn.setIcon(self._get_mode_icon())
            self._mode_btn.setToolTip(self._get_mode_tooltip())

    # =========================================================================
    # 도움말
    # =========================================================================

    def _show_help(self) -> None:
        """단축키 도움말 다이얼로그를 표시합니다."""
        dialog = HelpDialog(self)
        dialog.exec_()
