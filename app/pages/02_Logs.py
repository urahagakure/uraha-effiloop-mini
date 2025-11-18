from __future__ import annotations

from typing import List, cast

import pandas as pd
import streamlit as st
from config import LogRow

# ここで取り出して型を確定
logs: List[LogRow] = cast(List[LogRow], st.session_state.get("logs", []))

if not logs:
    st.info("まだログがありません。Practiceでループを実行してください。")
    st.stop()

df = pd.DataFrame(logs)
st.dataframe(df)
# CSVダウンロード等は今まで通り
