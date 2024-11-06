import streamlit as st
import urllib.request
from zipfile import ZipFile
import os

def reset_pages():
    st.session_state['page_count'] = 0

def get_data():
    os.makedirs('data', exist_ok=True)
    os.makedirs('indices', exist_ok=True)

    if not os.listdir('data'):
        urllib.request.urlretrieve("https://tufts.box.com/shared/static/t9cpmf2e57cwz0rtkbjew4usnopg78rd.csv", "data/chunked_press_review.csv")

    if not os.listdir('indices'):
        urllib.request.urlretrieve("https://tufts.box.com/shared/static/16rzcw8kmjlfyrhtkvbypqt4fh5ye8na.zip", "indices/hepc_index.zip")
        with ZipFile('indices/hepc_index.zip', 'r') as zip_ref:
            zip_ref.extractall('indices')