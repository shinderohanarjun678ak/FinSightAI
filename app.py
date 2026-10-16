import streamlit as st
from src.views.login_view import render_login_page

st.set_page_config(
    page_title="FinSight AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

render_login_page()
