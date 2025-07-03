
import requests
import streamlit as st
import pandas as pd

st.set_page_config(page_title="MemeSniper AI", layout="wide")
st.title("🚀 MemeSniper AI - Live Memecoin Scanner")
st.caption("Flipping SOL into gold, one meme at a time")

API_URL = 'https://public-api.birdeye.so/public/tokenlist?sort_by=volume_24h&sort_type=desc&limit=50'
HEADERS = {'x-chain': 'solana'}

@st.cache_data(show_spinner=False)
def scan():
    try:
        res = requests.get(API_URL, headers=HEADERS)
        tokens = res.json().get("data", [])
        clean = []
        for t in tokens:
            clean.append({
                "Name": t.get("name"),
                "Symbol": t.get("symbol"),
                "Price ($)": f"{float(t.get('price_usd', 0)):.4f}",
                "Volume (24h)": float(t.get("volume_24h", 0)),
                "Market Cap": float(t.get("mc", 0))
            })
        return pd.DataFrame(clean)
    except Exception as e:
        st.error(f"API Error: {e}")
        return pd.DataFrame()

if st.button("🔍 Scan Market Now"):
    with st.spinner("Scanning..."):
        df = scan()
        if not df.empty:
            st.success("Done")
            st.dataframe(df)
        else:
            st.warning("No tokens found.")
