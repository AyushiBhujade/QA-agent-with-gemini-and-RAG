
import pandas as pd
from io import BytesIO

def create_test_design_excel(test_cases):
    df = pd.DataFrame(test_cases)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="TestCases")
    output.seek(0)
    return output
