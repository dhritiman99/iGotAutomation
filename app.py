import pandas as pd
import os
import json
from src.data import getDataFrame, load_deptMapping
from src.transform import mapDepartments
from src.reporting import generateReport, write_file
import streamlit as st
from datetime import datetime

def columnNameSelector(df: pd.DataFrame) -> pd.DataFrame:
    columns = list(df.columns)
    roles = {
        "Department": "Department column",
        "Status": "Status column",
        "Employee_Id": "Employee ID column",
    }

    if len(columns) < len(roles) or len(set(columns)) != len(columns):
        st.error("The uploaded file must have at least three columns with unique names.")
        st.stop()

    selected = {}
    used_columns = set()

    for canonical_name, label in roles.items():
        default_column = (
            canonical_name
            if canonical_name in columns and canonical_name not in used_columns
            else next(column for column in columns if column not in used_columns)
        )

        source_column = st.selectbox(
            label,
            options=columns,
            index=columns.index(default_column),
            key=f"column_{canonical_name}",
        )

        selected[canonical_name] = source_column
        used_columns.add(source_column)


    if len(set(selected.values())) != len(roles):

        st.error("Select a different input column for each field.")
        st.stop()


    # Avoid duplicate canonical headers if an existing one wasn't selected.

    columns_to_drop = [
        name for name in roles

        if name in df.columns and name not in selected.values()

    ]
    df = df.drop(columns=columns_to_drop)


    rename_map = {

        source_column: canonical_name

        for canonical_name, source_column in selected.items()

    }
    return df.rename(columns=rename_map)


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
        df = columnNameSelector(df)
        df = mapDepartments(df, deptMapping)
        pt = generateReport(df)
        write_file(file,df, pt)
        now = datetime.now()
        st.download_button(
            label="Get Report",
            data=file,
            file_name= f'report_{now.strftime("%Y-%m-%d_%H:%M:%S")}.xlsx',
            mime='text/xlsx'
        )

    except (ValueError, KeyError) as error:
        st.error(str(error))