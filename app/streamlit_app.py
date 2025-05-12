import streamlit as st
from zla.data import load_processed   # your helper
from zla.viz import timeline_bar, network

st.set_page_config(page_title="Zelda Lore Analytics", layout="wide")

st.title("🗡️ Zelda Lore Analytics")
theme = st.selectbox("Choose a motif", ["Triforce", "Resurrection"])
df = load_processed()

st.plotly_chart(timeline_bar(df, theme), use_container_width=True)

if st.checkbox("Show network graph"):
    st.plotly_chart(network(df, theme), use_container_width=True)
