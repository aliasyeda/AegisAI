import streamlit as st

def setup_theme():
    """Configure Streamlit theme and custom CSS"""
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .threat-card {
        background-color: #2e2e2e;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin: 10px 0;
    }
    .metric-card {
        background-color: #1e1e1e;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)