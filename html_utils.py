#!/usr/bin/env python
# coding: utf-8

# ## HTML utils
# 
# This is a test App for deployment on streamlit server
# 
# It just analyzes a CV through OpenAI
# 
# Here is the utility to build a **HTML Report**
# 
# creation date: 25/08/2025

# In[1]:


import json
from pathlib import Path

def json_to_html(json_string: str) -> str:
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError:
        return "<p>Invalid JSON format returned by API.</p>"

    html = f"""
    <h2>Candidate Report</h2>
    <p><strong>Name:</strong> {data.get('Full Name')}</p>
    <p><strong>Summary:</strong> {data.get('Summary')}</p>
    <p><strong>Top Skills:</strong> {', '.join(data.get('Top 3 Skills', []))}</p>
    <h3>Recent Positions</h3>
    <ul>
    {''.join(f'<li>{pos}</li>' for pos in data.get('Last 3 Positions', []))}
    </ul>
    <p><strong>Education:</strong> {data.get('Education Summary')}</p>
    <p><strong>Fit Score:</strong> <span style="font-size: 24px;">{data.get('Fit Score')}</span></p>
    """
    return html


# In[ ]:




