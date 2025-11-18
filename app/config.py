from __future__ import annotations  # ← 最上段

from typing import Callable, Optional, TypedDict, cast  # 型ヒント

import streamlit as st  # Streamlit 本体

# どうしても折れない長いURLは行末でだけ E501 を無視
APP_URL = "https://example.com/very/long/path/that/you/cannot/break"  # noqa: E501


# ログ1行の型
class LogRow(TypedDict):
    start: str
    end: str
    duration_sec: int
    target: str
    note: str


# これ1つだけ残す（旧 safe_rerun は削除）
def safe_rerun() -> None:
    """Streamlitの rerun/experimental_rerun を型安全に呼び分ける。"""
    fn_opt: Optional[Callable[[], None]] = cast(
        Optional[Callable[[], None]], getattr(st, "rerun", None)
    )
    if fn_opt is not None:
        fn_opt()
    else:
        st.experimental_rerun()
