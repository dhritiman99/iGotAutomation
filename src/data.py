import pandas as pd
import streamlit as st
import json

@st.cache_resource()
def load_deptMapping():
    with open('mapping.json','r') as f:
        dept_mapping = json.load(f)
    return dept_mapping

def getDataFrame(file: str) -> pd.DataFrame:
    data = pd.read_excel(file)
    df = pd.DataFrame(
        data=data
    )
    return df
