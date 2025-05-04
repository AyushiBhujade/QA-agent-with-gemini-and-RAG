
import streamlit as st
from io import BytesIO
import json
from qa_agent.parser import extract_text_from_txt, extract_text_from_docx
from qa_agent.llm_engine import run_gemini_prompt
from qa_agent.correction_engine import apply_prompt_correction

st.set_page_config(page_title="QA Agent with Gemini", layout="wide")
st.title("🧪 QA Agent 🤖 — ✨ LLM-Powered Test Design with Gemini 🚀")

# Initialize session state
if "current_test_design" not in st.session_state:
    st.session_state.current_test_design = None

if "user_story_text" not in st.session_state:
    st.session_state.user_story_text = None

if "upload_completed" not in st.session_state:
    st.session_state.upload_completed = False

def parse_gemini_response(response_text):
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return None

# Upload Section
with st.expander("📂 Upload User Story", expanded=not st.session_state.upload_completed):
    uploaded_file = st.file_uploader("Choose a file (.txt, .docx, .png)", type=["txt", "docx", "png"])

    if uploaded_file and not st.session_state.upload_completed:
        st.success(f"Uploaded: {uploaded_file.name}")
        file_contents = uploaded_file.read()

        if uploaded_file.name.endswith(".txt"):
            user_story_text = extract_text_from_txt(file_contents)
        elif uploaded_file.name.endswith(".docx"):
            user_story_text = extract_text_from_docx(uploaded_file)
        else:
            user_story_text = file_contents.decode("utf-8", errors="ignore")

        st.session_state.user_story_text = user_story_text
        st.text_area("📄 Extracted User Story Content", user_story_text, height=250)

        with st.spinner("💡 Generating initial Test Design with Gemini..."):
            initial_response = run_gemini_prompt(user_story_text, "Generate the initial Test Design.")

        st.markdown("### 📄 Initial Test Design from Gemini")
        st.code(initial_response)

        st.session_state.current_test_design = initial_response
        st.session_state.upload_completed = True

        structured_data = apply_prompt_correction(initial_response)

        if structured_data:
            st.download_button("⬇️ Download Initial Test Design", structured_data, file_name="Test_Design.xlsx")
        else:
            st.error("Gemini response could not be parsed.")

# Correction Section
if st.session_state.current_test_design is not None:
    st.markdown("---")
    st.markdown("## ✍️ Apply Corrections to Existing Test Design")

    prompt = st.text_area("What would you like to fix, change, or add?", height=150)

    if prompt:
        with st.spinner("💡 Gemini is applying your correction..."):
            combined_input = f"""
You are maintaining an evolving Test Design document.

Below is the CURRENT Test Design after previous corrections:

{st.session_state.current_test_design}

Now, apply the following NEW correction carefully:
'{prompt}'

⚠️ Important Instructions:
- Do NOT recreate the Test Design from scratch.
- Do NOT revert any previous corrections.
- Only apply this new correction on the current Test Design exactly as instructed.
- Return the fully corrected and updated Test Design, ready for next corrections.

Provide the full updated Test Design only.
"""
            updated_response = run_gemini_prompt(combined_input, "")

        st.markdown("### 🤖 Updated Test Design After Correction")
        st.code(updated_response)

        st.session_state.current_test_design = updated_response

        structured_data = apply_prompt_correction(updated_response)

        if structured_data:
            st.download_button("⬇️ Download Corrected Test Design", structured_data, file_name="Corrected_Test_Design.xlsx")
        else:
            st.error("Gemini updated response could not be parsed.")
