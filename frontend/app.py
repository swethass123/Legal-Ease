import streamlit as st
import requests

BACKEND_URL = "https://legal-ease-h4it.vercel.app"

st.set_page_config(page_title="LegalEase")
st.title("LegalEase - AI Legal Document Helper")

option = st.selectbox("Choose", ["Simplify", "Summarize"])

text = st.text_area("Paste your Legal Document here", height=200)

if st.button("Generate"):
    if text == "":
        st.warning("Please paste text ma")
    else:
        endpoint = f"{BACKEND_URL}/{option.lower()}"
        # payload check - backend enna expect panuthu nu
        try:
            res = requests.post(endpoint, json={"text": text})
            if res.status_code == 200:
                st.success("Result ma:")
                st.write(res.json())
            else:
                st.error(f"Error: {res.text}")
        except Exception as e:
            st.error(str(e))
