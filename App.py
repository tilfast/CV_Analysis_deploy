#!/usr/bin/env python
# coding: utf-8

# ## App
# 
# This is a test App for deployment on streamlit server
# 
# It just analyzes a CV through OpenAI
# 
# Here is the **actual logic** of the App:
# 
#     - load a CV
#     - Analyze the CV with OpenAI
# 
# creation date: 25/08/2025

# In[5]:


import streamlit as st
from auth_utils import check_password
from datetime import date

# ✅ Set page config FIRST
st.set_page_config(page_title="CV Analyzer", layout="wide")

# 🔐 Auth check
check_password(secret=st.secrets["auth"]["password"])

# 📅 Daily tracking
if "openai_daily" not in st.session_state:
    st.session_state["openai_daily"] = {"date": date.today(), "count": 0}

if st.session_state["openai_daily"]["date"] != date.today():
    st.session_state["openai_daily"] = {"date": date.today(), "count": 0}

MAX_CALLS_PER_DAY = 5

if st.session_state["openai_daily"]["count"] >= MAX_CALLS_PER_DAY:
    st.warning("You've reached the daily limit for OpenAI calls.")
    st.stop()

st.session_state["openai_daily"]["count"] += 1
#st.success(f"OpenAI call #{st.session_state['openai_daily']['count']} today.")

# 🧠 App title
st.title("📄 CV Analyzer with OpenAI")

import json
from PyPDF2 import PdfReader
from openai_utils import analyze_cv    # safe after set_page_config
from html_utils import json_to_html


# ------------ Session state init ------------
for key, default in {
    "result_text": None,   # raw string from OpenAI
    "result_json": None,   # parsed dict if valid JSON
    "show_html": False,    # toggle for HTML report
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ------------ Sidebar controls (optional) ------------
with st.sidebar:
    st.header("Controls")
    # Always show HTML toggle; disable until we have a result
    st.checkbox(
        "🧾 Show HTML Report",
        key="show_html",
        disabled=(st.session_state["result_json"] is None),
        help="Enable after running analysis."
    )

    # Clear results
    if st.button("Clear results"):
        st.session_state["result_text"] = None
        st.session_state["result_json"] = None
        st.rerun()

# ------------ File upload ------------ 
uploaded_file = st.file_uploader("Upload a PDF CV", type=["pdf"])

if uploaded_file is not None and "raw_text" not in st.session_state:
    try:
        reader = PdfReader(uploaded_file)
        raw_text = "\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception as e:
        raw_text = ""
        st.warning(f"Could not read PDF text directly ({e}).")

    preview = (raw_text[:2000] + "...") if raw_text and len(raw_text) > 2000 else (raw_text or "[no text extracted]")
    st.text_area("📝 Extracted Text (preview)", preview, height=200)
    st.session_state["raw_text"] = raw_text

# ------------ Analyze Button (always visible if raw_text exists) ------------ 
if st.session_state.get("raw_text"):
    if st.button("🔍 Analyze with OpenAI"):
        with st.spinner("Analyzing..."):
            try:
                result = analyze_cv(st.session_state["raw_text"])
                st.session_state["result_text"] = result
                try:
                    st.session_state["result_json"] = json.loads(result)
                except Exception:
                    st.session_state["result_json"] = None
            except Exception as e:
                st.error(f"OpenAI analysis failed: {e}")        


view_raw = st.checkbox("Show raw JSON string")

if view_raw and st.session_state["result_text"]:
    st.subheader("📋 Raw JSON Output")
    st.code(st.session_state["result_text"], language="json")
elif st.session_state["result_json"]:
    st.subheader("✅ Parsed Summary")
    st.write(st.session_state["result_json"])

if st.session_state["show_html"] and st.session_state["result_json"] and 0:
        st.subheader("🧾 HTML Report")
        st.markdown(json_to_html(st.session_state["result_json"]), unsafe_allow_html=True)            


# In[ ]:




