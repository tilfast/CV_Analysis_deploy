#!/usr/bin/env python
# coding: utf-8

# # Authentification
# 
# Usage gate

# In[2]:


# auth_utils.py
import streamlit as st

import os

password = os.environ.get("APP_PASSWORD")


def check_password(secret="your_secret"):
    def password_entered():
        if password == secret:
            st.session_state["authenticated"] = True
        else:
            st.session_state["authenticated"] = False

    if "authenticated" not in st.session_state:
        st.text_input("Enter password", type="password", on_change=password_entered, key="password")
        st.stop()

    if not st.session_state["authenticated"]:
        st.text_input("Enter password", type="password", on_change=password_entered, key="password")
        st.error("Incorrect password")
        st.stop()



# In[ ]:




