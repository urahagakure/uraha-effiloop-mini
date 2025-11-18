# app/pages/01_Practice.py
from __future__ import annotations  # 将来アノテーション：前方参照を簡単に

import time  # 1秒待って再描画するため
from datetime import datetime  # 時刻の取得に使う

import streamlit as st  # Streamlit 本体
from config import LogRow, safe_rerun  # 仕様型と安全な再描画

# -------------------------
# 画面の基本設定・見出し
# -------------------------
st.set_page_config(
    page_title="Practice - uraha EffiLoop mini",  # タイトル
    page_icon="✅",  # アイコン
    layout="centered",  # レイアウト
)
st.title("Practice")  # 見出し
st.caption("EffiLoopミニ（10〜20秒） + BLS（Start/Stop/Ground）")  # 説明

# -------------------------
# 状態の初期化（無ければ作る）
# -------------------------
if "logs" not in st.session_state:  # ログの配列
    st.session_state["logs"] = []
if "effi_running" not in st.session_state:  # 実行中フラグ
    st.session_state["effi_running"] = False
if "effi_start_time" not in st.session_state:  # 開始時刻
    st.session_state["effi_start_time"] = None

# 既存値をデフォルトに読む（あっても上書きしない）
target_default = st.session_state.get("effi_target", "")
note_default = st.session_state.get("effi_note", "")
dur_default = int(st.session_state.get("effi_duration_sec", 10))

# -------------------------
# 入力ウィジェット（ウィジェット→状態の一方向に統一）
# ※ ここで session_state へ「手で代入しない」
# -------------------------
target = st.text_input(
    "ターゲット（瞬間で行う例：押す/見る/一歩）",  # ラベル
    value=target_default,  # 既存値
    key="effi_target",  # 状態キー
)
sec = st.slider(
    "ループ長（秒）",  # ラベル
    10,
    20,
    dur_default,
    step=1,  # 範囲と初期値
    key="effi_duration_sec",  # 状態キー（これが真実）
)
note = st.text_input(
    "メモ（任意）",  # ラベル
    value=note_default,  # 既存値
    key="effi_note",  # 状態キー
)
# --- ここは入力ウィジェット群のすぐ下に追加 --------------------------
progress_slot = st.empty()  # 仕様：進捗バーの置き場を一つ確保（毎リランで再生成OK）
# -------------------------
# ボタン（Start / Stop）
# -------------------------
col1, col2 = st.columns(2)
with col1:
    if st.button("Start", disabled=st.session_state["effi_running"]):  # Start
        st.session_state["effi_start_time"] = datetime.now()  # 開始時刻
        st.session_state["effi_running"] = True  # フラグON
        safe_rerun()  # 即時再描画

with col2:
    if st.button("Stop", disabled=not st.session_state["effi_running"]):  # Stop
        end = datetime.now()  # 終了時刻
        start = st.session_state.get("effi_start_time")  # 開始時刻
        dur = int((end - start).total_seconds()) if start else 0  # 経過秒
        st.session_state["logs"].append(  # ログ追加
            LogRow(
                start=start.isoformat() if start else "",
                end=end.isoformat(),
                duration_sec=dur,
                target=st.session_state.get("effi_target", ""),
                note=st.session_state.get("effi_note", ""),
            )
        )
        st.session_state["effi_running"] = False  # フラグOFF
        st.success("Complete! ログに記録しました。")  # 完了表示
        safe_rerun()  # 即時再描画

# -------------------------
# ------------------ 実行中の描画（ハートビート） ------------------
if st.session_state.get("effi_running", False):  # 仕様：実行中のみ進捗更新
    start = st.session_state.get("effi_start_time")  # 仕様：開始時刻を取得
    dur = int(st.session_state.get("effi_duration_sec", 10))  # 仕様：目標の総秒数
    elapsed = int((datetime.now() - start).total_seconds()) if start else 0  # 仕様：経過秒
    remain = max(dur - elapsed, 0)  # 仕様：負にならない残り秒
    pct = int(min(elapsed * 100 // max(dur, 1), 100))  # 仕様：0〜100%に正規化

    progress_slot.progress(pct)  # 仕様：プログレスバーを現在率で描画
    st.info(f"残り：{remain} 秒")  # 仕様：テキストでも残りを表示

    if remain > 0:  # 仕様：まだ残っていれば1秒待って再描画
        time.sleep(1)  # 仕様：1秒刻み
        safe_rerun()  # 仕様：即時再描画（新旧APIを吸収）
    else:  # 仕様：ちょうど完了
        st.session_state["effi_running"] = False  # 仕様：実行フラグOFF
        progress_slot.empty()  # 仕様：バーを消す
        st.success("Complete! ログに記録しました。")  # 仕様：完了メッセージ
