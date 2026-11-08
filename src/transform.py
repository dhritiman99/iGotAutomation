import pandas as pd
import json
import streamlit as st

def mapDepartments(df: pd.DataFrame, dept_map: dict) -> pd.DataFrame:
    try:
        df = df.dropna(axis=0, how="all").dropna(axis=1, how="all")
        df['DeptGroup'] = df['Department'].map(dept_map).fillna(df['Department'])
        print(df)
        return df
    except Exception as e:
        st.error(str(e))       
        return df
            
