"""
UI Helper functions for IntelliDocs
"""

import streamlit as st

def load_custom_css():
    """Load custom CSS for better UI"""
    st.markdown("""
    <style>
    .doc-preview {
        background-color: #f8f9fa;
        color: #212529;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
        font-family: monospace;
        font-size: 12px;
        max-height: 300px;
        overflow-y: auto;
        white-space: pre-wrap;
        line-height: 1.4;
    }
    .summary-box {
        background-color: #e8f4f8;
        color: #1a1a1a;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        white-space: pre-wrap;
        line-height: 1.5;
        border: 1px solid #b8daeb;
    }
    .comparison-box {
        background-color: #f0f8f0;
        color: #1a1a1a;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        white-space: pre-wrap;
        line-height: 1.5;
        border: 1px solid #c3e6c3;
    }
    .metric-card {
        background-color: #ffffff;
        color: #333333;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        border-left: 4px solid #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)