import pandas as pd

def generateReport(df: pd.DataFrame) -> pd.DataFrame:
    index = df['DeptGroup'] if 'DeptGroup' in df.columns else df['Department']
    pt = df.pivot_table(
        index=index,
        aggfunc='count',
        values='Employee_Id',
        margins=True,
        margins_name='Total Count'
    )
    return pt