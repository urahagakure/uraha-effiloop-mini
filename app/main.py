# app/main.py
import streamlit as st

# 長いURLの定数（折れないので行末だけ E501 を抑制）
DOC_URL = "https://example.com/very/long/path/that/you/cannot/break"  # noqa: E501
APP_URL = "https://example.com/app"  # noqa: E501

st.set_page_config(
    page_title="uraha EffiLoop mini",
    page_icon="✅",
    layout="centered",
)

st.title("uraha EffiLoop mini")
st.caption("FEPセルフケア最小ループ（保存なし・匿名・CSVのみ）")

# 複数行の文章は“隣接リテラルの自動連結”で折る
st.write("左のサイドバーから **Practice / Logs** を開いてください。(pages/配下は自動表示されます)")

# （必要なら）リンク表示
st.markdown(f"[使い方ガイドはこちら]({DOC_URL})")
# st.markdown(f"[公開アプリはこちら]({APP_URL})")

st.markdown("""
**できること**
- 10–20秒の最小ループ（EffiLoopミニ）
- BLS（Start / Stop / Ground）
- セッション内ログをCSVで保存（サーバ保存なし）

**注意**：医療・診断目的ではありません。危機時は専門機関へ。
""")
