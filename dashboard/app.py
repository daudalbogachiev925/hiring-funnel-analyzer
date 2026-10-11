import os
import streamlit as st
import pandas as pd
import plotly.express as px
import requests

API = os.getenv("API_URL", "http://api:8000")

st.set_page_config(page_title="Hiring Funnel", layout="wide")
st.title("Hiring Funnel Analyzer")

@st.cache_data(ttl=30)
def fetch(path):
    return requests.get(f"{API}{path}").json()

funnel = pd.DataFrame(fetch("/api/stages/funnel"))
sources = pd.DataFrame(fetch("/api/stages/sources"))
cands = pd.DataFrame(fetch("/api/candidates?limit=1000"))

col1, col2, col3 = st.columns(3)
col1.metric("Кандидатов", len(cands))
col2.metric("Офферов", int(cands.offered.sum()) if len(cands) else 0)
col3.metric("Наймов", int(cands.hired.sum()) if len(cands) else 0)

st.subheader("Воронка")
st.plotly_chart(px.funnel(funnel, x="count", y="stage"))

st.subheader("Источники")
st.plotly_chart(px.bar(sources, x="source", y="count"))

st.subheader("Кандидаты")
st.dataframe(cands.head(200))
