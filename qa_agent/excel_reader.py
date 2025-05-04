
import pandas as pd
from typing import List

def read_excel_tabs(file, expected_sheets: List[str] = None) -> dict:
    """
    Reads specific sheets from an Excel file and returns them as a dictionary of DataFrames.
    If expected_sheets is None, all sheets will be read.
    """
    try:
        xls = pd.ExcelFile(file)
        sheets = expected_sheets if expected_sheets else xls.sheet_names
        return {sheet: xls.parse(sheet) for sheet in sheets}
    except Exception as e:
        return {"error": str(e)}
