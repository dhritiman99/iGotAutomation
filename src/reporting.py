import pandas as pd
import streamlit as st

def generateReport(df: pd.DataFrame) -> pd.DataFrame:
    index = "DeptGroup" if 'DeptGroup' in df.columns else "Department"
    pt = df.pivot_table(
        index=index,                 # Department Name
        columns='Status',            # Pending / Completed
        values='Employee_Id',        # Count Employee IDs
        aggfunc='count',
        margins=True,
        margins_name='Total Count',
        fill_value=0
    )
    return pt

def write_file(file: st.file_uploader,df: pd.DataFrame, pt: pd.DataFrame) -> None:
    with pd.ExcelWriter(
            file,
            engine="openpyxl",
            mode="a",
            if_sheet_exists="replace"
        ) as writer:


            df.to_excel(
                writer,
                sheet_name="Master_Data",
                index=False
            )


            pt.to_excel(
                writer,
                sheet_name="Report"
            )
