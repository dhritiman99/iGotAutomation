import pandas as pd
import os
import json
from src.data import getDataFrame, load_deptMapping
from src.transform import mapDepartments
from src.reporting import generateReport
import streamlit as st

st.title('IGot Report')
file = st.file_uploader(
    label='Upload Excel File',
    type='xlsx',
    max_upload_size=5
)

if file:
    deptMapping = load_deptMapping()

    df = getDataFrame(file)
    df = mapDepartments(df, deptMapping)
    #pt = generateReport(df)
    with pd.ExcelWriter(
        file, 
        engine="openpyxl", 
        mode="a", 
        if_sheet_exists="replace"
    ) as writer:

        df.to_excel(writer, index=False)
    
    #pt

    st.download_button(
        label="Get Report",
        data=file,
        mime='text/xlsx'
    )
