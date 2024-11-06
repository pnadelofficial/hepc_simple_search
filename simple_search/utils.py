import streamlit as st
import subprocess
import os

def reset_pages():
    st.session_state['page_count'] = 0

def get_data():
    os.makedirs('data', exist_ok=True)
    os.makedirs('indices', exist_ok=True)

    if not os.listdir('data'):
        subprocess.run(["wget", "https://tufts.box.com/shared/static/t9cpmf2e57cwz0rtkbjew4usnopg78rd.csv", "-O", "data/chunked_press_review.csv"])

    if not os.listdir('indices'):
        subprocess.run(["wget", "https://tufts.box.com/shared/static/16rzcw8kmjlfyrhtkvbypqt4fh5ye8na.zip", "-O", "indices/hepc_index.zip"])
        subprocess.run(["unzip", "indices/hepc_index.zip", "-d", "press_review_index"])
