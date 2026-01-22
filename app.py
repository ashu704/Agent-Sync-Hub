import streamlit as st
import subprocess
import os
import time
import threading
import signal

st.set_page_config(
    page_title="Agent-Sync Context Hub",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp {
        background: #fafafa;
    }
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
    header, footer, .stDeployButton {
        display: none !important;
    }
    iframe {
        border: none;
    }
</style>
""", unsafe_allow_html=True)

def start_server():
    subprocess.Popen(
        ["npx", "tsx", "server/index.ts"],
        cwd=os.getcwd(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def start_vite():
    subprocess.Popen(
        ["npx", "vite", "--port", "5173", "--host", "0.0.0.0"],
        cwd=os.getcwd(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

if 'servers_started' not in st.session_state:
    start_server()
    time.sleep(1)
    start_vite()
    time.sleep(2)
    st.session_state.servers_started = True

st.markdown("""
<iframe src="http://localhost:5173" width="100%" height="900" style="border:none;"></iframe>
""", unsafe_allow_html=True)
