import time
from datetime import datetime, timedelta
import streamlit as st

st.set_page_config(page_title="Practice - uraha EffiLoop mini", page_icon="🧭", layout="centered")
st.title("Practice")
st.caption("EffiLoopミニ（10–20秒）＋ BLS（Start / Stop / Ground）")

ss = st.session_state
ss.setdefault("logs", [])
ss.setdefault("effi_running", False)
ss.setdefault("effi_start_time", None)
ss.setdefault("effi_duration_sec", 15)
ss.setdefault("effi_target", "")
ss.setdefault("effi_note", "")
ss.setdefault("bls_state", "idle")  # idle/running

st.subheader("BLS｜Start / Stop / Ground")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Start"):
        ss["bls_state"] = "running"
with col2:
    if st.button("Stop"):
        ss["bls_state"] = "idle"
with col3:
    if st.button("Ground（呼気8秒）"):
        st.write("吐く：8秒（視線はやわらかく）")
        bar = st.progress(0)
        for i in range(80):
            time.sleep(0.1)
            bar.progress(i + 1)
        st.success("OK。呼吸はそのまま自然に。")

if ss["bls_state"] == "running":
    st.info("BLS: 吸う4／吐く8を目安に。評価は保留、感覚だけ観測。")

st.markdown("---")
st.subheader("EffiLoopミニ｜10–20秒の最小ループ")
ss["effi_target"] = st.text_input("ターゲット（動詞で1行）例：押す／見る／一歩", value=ss.get("effi_target",""))
ss["effi_duration_sec"] = st.slider("ループ長（秒）", 10, 20, ss.get("effi_duration_sec",15), 1)
ss["effi_note"] = st.text_input("メモ（任意 / 体感の一言）", value=ss.get("effi_note",""))

c1, c2 = st.columns(2)
with c1:
    start_clicked = st.button("▶ Start")
with c2:
    stop_clicked = st.button("■ Stop")

now = datetime.now()

if start_clicked:
    if not ss["effi_target"].strip():
        st.warning("ターゲットを入力してください（例：押す／見る／一歩）")
    else:
        ss["effi_running"] = True
        ss["effi_start_time"] = now
        ss["effi_duration"] = timedelta(seconds=int(ss["effi_duration_sec"]))

if stop_clicked and ss["effi_running"]:
    end = now
    ss["effi_running"] = False
    ss["logs"].append({
        "start": ss["effi_start_time"].isoformat() if ss["effi_start_time"] else "",
        "end": end.isoformat(),
        "duration_sec": (end - ss["effi_start_time"]).total_seconds() if ss["effi_start_time"] else 0,
        "target": ss["effi_target"],
        "note": ss["effi_note"],
        "result": "stopped",
    })
    ss["effi_note"] = ""

if ss["effi_running"] and ss["effi_start_time"]:
    elapsed = now - ss["effi_start_time"]
    remain = ss["effi_duration"] - elapsed
    remain_sec = max(0, int(remain.total_seconds()))
    st.metric("残り", f"{remain_sec} 秒")
    st.progress(min(1.0, elapsed / ss["effi_duration"]))
    if remain.total_seconds() <= 0:
        end = now
        ss["effi_running"] = False
        ss["logs"].append({
            "start": ss["effi_start_time"].isoformat(),
            "end": end.isoformat(),
            "duration_sec": (end - ss["effi_start_time"]).total_seconds(),
            "target": ss["effi_target"],
            "note": ss["effi_note"],
            "result": "complete",
        })
        ss["effi_note"] = ""
        st.balloons()
        st.success("Complete! ログに記録しました。")
    else:
        try:
            st.rerun()
        except AttributeError:
            st.experimental_rerun()
