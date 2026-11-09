import pandas as pd
import os
import json
from src.data import getDataFrame, load_deptMapping
from src.transform import mapDepartments
from src.reporting import generateReport, write_file
import streamlit as st
from datetime import datetime



st.title('IGot Report')
file = st.file_uploader(
    label='Upload Excel File',
    type='xlsx',
    max_upload_size=5
)

if file:
    try:
        deptMapping = load_deptMapping()
        if not deptMapping:
            st.error("Department Column Does not exist..")
            st.stop()
        df = getDataFrame(file)
        if df.empty:
            st.error("Error Getting Data")
            st.stop()
        df = mapDepartments(df, deptMapping)
        pt = generateReport(df)
        write_file(df, pt)
        now = datetime.now()
        st.download_button(
            label="Get Report",
            data=file,
            file_name= f'report_{now.strftime("%Y-%m-%d_%H:%M:%S")}.xlsx',
            mime='text/xlsx'
        )
    except (ValueError, KeyError) as error:
        st.error(str(error))