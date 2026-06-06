"""build tooling 向けの共通ログ設定を提供するモジュール。"""

from __future__ import annotations

import logging

_LOG_FORMAT = "%(levelname)s: %(message)s"
_CONFIGURED = False


def get_logger(name: str) -> logging.Logger:
    """共通設定を適用した Logger を返す。"""

    global _CONFIGURED

    if not _CONFIGURED:
        logging.basicConfig(level=logging.INFO, format=_LOG_FORMAT)
        _CONFIGURED = True

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
