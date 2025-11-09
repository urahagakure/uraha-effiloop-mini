import streamlit as st
st.set_page_config(page_title="uraha EffiLoop mini", page_icon="✅", layout="centered")

st.title("uraha EffiLoop mini")
st.caption("FEPセルフケア最小ループ｜保存なし・匿名・CSVのみ")

st.markdown("""
**できること**
- 10–20秒の最小ループ（EffiLoopミニ）
- BLS（Start / Stop / Ground）
- セッション内ログをCSVで保存（サーバ保存なし）

**注意**：医療・診断目的ではありません。危機時は専門機関へ。
""")

st.write("左のサイドバーから **Practice / Logs** を開いてください。（pages/ 配下は自動表示されます）")
st.info("バージョン: 0.1.0 / ライセンス: MIT")
