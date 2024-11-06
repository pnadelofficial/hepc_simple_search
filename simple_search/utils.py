import streamlit as st
import urllib.request
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
        os.makedirs('press_review_index', exist_ok=True)
        os.system("unzip indices/hepc_index.zip -d press_review_index")
        print(os.system("pwd"))
        print(os.system("ls -la"))
        print(os.system("ls -la press_review_index"))