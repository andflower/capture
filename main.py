"""
스크린 캡처 도구 - 메인 엔트리 포인트

PyQt5 기반의 프레임리스 스크린 캡처 도구입니다.
Qt 플랫폼 초기화 문제(SessionStart:startup hook error)를 방지하기 위한
환경 설정을 수행한 후 애플리케이션을 시작합니다.
"""
import os
import sys
import logging

# 로깅 설정 (가장 먼저 설정하여 모든 로그 캡처)
_log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'capture.log')
_file_handler = logging.FileHandler(_log_file, mode='w', encoding='utf-8')
_file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
_file_handler.setLevel(logging.DEBUG)
logging.root.addHandler(_file_handler)
logging.root.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.info('로깅 초기화 완료')

# Qt 환경 초기화 (PyQt5 import 전에 수행해야 함)
from qt_env_setup import initialize_qt_environment  # noqa: E402

initialize_qt_environment(opengl_mode='angle')
logger.info('Qt 환경 초기화 완료')

from PyQt5.QtWidgets import QApplication  # noqa: E402
from ui.capture_window import FinalCaptureWindow  # noqa: E402

logger.info('모든 모듈 import 완료')


def main() -> int:
    """
    애플리케이션 메인 함수.

    QApplication을 생성하고 메인 윈도우를 표시합니다.

    Returns:
        int: 애플리케이션 종료 코드
    """
    logger.info('QApplication 생성 시작')
    app = QApplication(sys.argv)

    logger.info('FinalCaptureWindow 생성 시작')
    window = FinalCaptureWindow()

    logger.info('윈도우 표시')
    window.show()

    logger.info('이벤트 루프 시작')
    exit_code = app.exec_()

    logger.info(f'애플리케이션 정상 종료 (exit_code={exit_code})')
    return exit_code


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        logger.exception(f'애플리케이션 크래시: {e}')
        raise
