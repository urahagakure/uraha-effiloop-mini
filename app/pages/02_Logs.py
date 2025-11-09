import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Logs - uraha EffiLoop mini", page_icon="📄", layout="centered")
st.title("Logs")
st.caption("セッション内ログのみ。サーバ保存は行いません。")

logs = st.session_state.get("logs", [])
if not logs:
    st.info("まだログがありません。Practiceでループを実行してください。")
else:
    df = pd.DataFrame(logs)
    st.dataframe(df)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("CSVをダウンロード", data=csv, file_name="effiloop_logs.csv", mime="text/csv")
    if st.button("セッションクリア（このタブだけ）"):
        st.session_state["logs"] = []
        st.success("クリアしました。")
        try:
            st.rerun()
        except AttributeError:
            st.experimental_rerun()
