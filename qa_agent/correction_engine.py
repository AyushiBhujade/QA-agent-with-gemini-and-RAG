import pandas as pd
from io import BytesIO

# ✅ STEP 1: Parse the Gemini response (Markdown table → DataFrame)
def parse_gemini_response(gemini_output):
    try:
        lines = gemini_output.strip().split("\n")
        table_lines = [line for line in lines if line.strip().startswith("|")]

        if not table_lines or len(table_lines) < 3:
            return None

        headers = [h.strip() for h in table_lines[0].strip().split("|")[1:-1]]
        data_rows = []

        for row in table_lines[2:]:
            cells = [c.strip() for c in row.strip().split("|")[1:-1]]
            if len(cells) == len(headers):
                data_rows.append(cells)

        return pd.DataFrame(data_rows, columns=headers)

    except Exception as e:
        print(f"[ERROR] Failed to parse Gemini response: {e}")
        return None

# ✅ STEP 2: Apply parsed data to Excel writer
def apply_prompt_correction(gemini_response):
    structured_df = parse_gemini_response(gemini_response)

    if structured_df is None:
        return None  # or raise error if needed

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        structured_df.to_excel(writer, index=False, sheet_name="CorrectedTestCases")
    output.seek(0)
    return output








# import pandas as pd
# from io import BytesIO

# def apply_prompt_correction(df, gemini_response):
#     # For now assume Gemini response is parsed already as dict
#     # Real correction would parse and modify df accordingly
#     output = BytesIO()
#     with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
#         df.to_excel(writer, index=False, sheet_name="CorrectedTestCases")
#     output.seek(0)
#     return output
