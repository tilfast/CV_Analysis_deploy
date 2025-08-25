#!/usr/bin/env python
# coding: utf-8

# ## OpenAI utility
# 
# This is a test App for deployment on streamlit server
# 
# It just analyzes a CV through OpenAI
# 
# This is the **connection to Open AI**
# 
# creation date: 25/08/2025

# In[ ]:


# openai_utils.py
from openai import OpenAI
import os

try:
    import streamlit as st
except Exception:
    st = None


    
    
def _get_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    print("openai.api_key:", os.getenv("OPENAI_API_KEY"))
    if key:
        return key
    if st is not None:
        try:
            return st.secrets["openai"]["api_key"]   # accessed only when called
        except Exception:
            pass
    raise RuntimeError("OpenAI API key not found.")


def _get_client() -> OpenAI:
    return OpenAI(api_key=_get_api_key())

def analyze_cv(text: str) -> str:
    client = _get_client()  # create client at call time, not import time

    prompt = f"""
You are a professional recruiter. Reply ONLY with valid JSON with keys:
"Full Name","Summary","Top 3 Skills","Last 3 Positions","Education Summary","Fit Score".
CV:
{text}
"""
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )

    return resp.choices[0].message.content


# In[ ]:




