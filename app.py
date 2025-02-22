import os

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from github import Github

# -------------------Setting---------------------

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE-API-KEY"))

ghub = Github(os.getenv("GITHUB_TOKEN"))


# ------------------Functions--------------------

def get_genai_response(prompt, text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt, text])
    return response.text


def get_content_from_github(link):
    link = link.replace("https://github.com/", "")
    final_content = ""
    if verify_link(link):
        repo = ghub.get_repo(link)
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                try:
                    # print(file_content.decoded_content.decode('utf-8'))
                    final_content += " " + file_content.decoded_content.decode('utf-8')
                except Exception as e:
                    print(f"Could not read {file_content.path}: {e}")

        return final_content
    return None


def verify_link(link):
    if len(link.split("/")) == 2:
        return True
    return False


# ---------------------Prompt-------------------
input_prompt = """
You are Github repo content expert with great knowledge about the code. 
Generate a good and interesting README with proper functionality and working.
Also try to add subheader project link and add project link which may be present in README.md.
The extracted content from github repo is :
"""

# --------------------UI-------------------------


st.set_page_config(page_title="README Generator")
st.header("README Generator")
github_link = st.text_input("Enter the github link")
submit_button = st.button("Extract")
if submit_button:
    with st.spinner("Loading"):
        content = get_content_from_github(github_link)
        if content is not None:
            result = get_genai_response(input_prompt, content)
            st.write(result)
