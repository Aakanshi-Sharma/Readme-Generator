import os

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# -------------------Setting---------------------

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE-API-KEY"))

# ------------------Functions--------------------


# --------------------UI-------------------------


st.set_page_config(page_title="README  Generator")
st.header("Readme Generator")
github_link = st.text_input("Enter the github link")
