import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("Missing GEMINI_API_KEY in .env")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-pro")

# Few-Shot Examples
few_shot_examples = """
⚡ Important Rules:
- Include columns: User Story, Test Case ID, Test Case Scenario, Test Steps, User Roles, User Input, Expected Output, Test Result, Defect ID, Defect Severity, Defect Status, UAT Applicable Test Case, Candidate for Regression
- Test Steps must start with:
    1. Login to the Dynamics 365 application with the mentioned user roles
    2. Select Contract Management System application
    3. Navigate to Change Area
- Output only a clean Markdown table.
- No freeform text, no explanations.

---

### 📚 Example 1:
**User Story:**
Iteration 3: Conditional Field Logic for "Contract Amount Type" field under Data section in Contract Creation Form.

**Expected Test Design:**
| User Story | Test Case ID | Test Case Scenario | Test Steps | User Roles | User Input | Expected Output | Test Result | Defect ID | Defect Severity | Defect Status | UAT Applicable Test Case | Candidate for Regression |
|------------|--------------|--------------------|------------|------------|------------|----------------|-------------|-----------|----------------|---------------|---------------------------|---------------------------|
| 45602 | TC_45602_001 | Verify Revenue contract single field rule | 1. Login <br> 2. New Contract <br> 3. Contract Amount Type = Revenue <br> 4. Fill both fields <br> 5. Save as Draft | Contract & PO Originator, Contract Manager, Super Admin | Fill Revenue Description and Contract Amount | Error message: "Only one of Contract Amount or Revenue Description should be entered." | | | | | Yes | Yes |

---

### 📚 Example 2:
**User Story:**
Add "State Term Contract Number Required?" field in Commodity Code entity. Default value = No.

**Expected Test Design:**
| User Story | Test Case ID | Test Case Scenario | Test Steps | User Roles | User Input | Expected Output | Test Result | Defect ID | Defect Severity | Defect Status | UAT Applicable Test Case | Candidate for Regression |
|------------|--------------|--------------------|------------|------------|------------|----------------|-------------|-----------|----------------|---------------|---------------------------|---------------------------|
| 45422 | TC_45422_001 | Verify new field added with correct default value | 1. Login <br> 2. Navigate to Commodity Code entity <br> 3. Create new record <br> 4. Check default value of State Term Contract field | Contract Super Admin, Contract Manager | New Commodity Code creation | Field appears with default value "No" | | | | | Yes | Yes |

---

### 📚 Example 3:
**User Story:**
Contract Manager field lookup should fetch users from User and Roles entity, not old Contract Managers entity.

**Expected Test Design:**
| User Story | Test Case ID | Test Case Scenario | Test Steps | User Roles | User Input | Expected Output | Test Result | Defect ID | Defect Severity | Defect Status | UAT Applicable Test Case | Candidate for Regression |
|------------|--------------|--------------------|------------|------------|------------|----------------|-------------|-----------|----------------|---------------|---------------------------|---------------------------|
| 45494 | TC_45494_001 | Verify Contract Manager lookup source updated | 1. Login <br> 2. Navigate to Contracts <br> 3. Create new Contract <br> 4. Select Contract Manager field | Contract Super Admin, Contract Manager | Lookup Contract Manager | User list fetched from User and Roles entity | | | | | Yes | Yes |

---

⚠️ For any new user story, follow the above format exactly.
"""

# Run Gemini prompt
def run_gemini_prompt(user_story_text, correction_prompt):
    full_prompt = f"""
You are a QA Test Automation Agent.

Your task is to generate a structured test design based on a user story and requested corrections.

Here is the user story:
\"\"\"{user_story_text}\"\"\"

Correction/Fix instruction (if any):
\"\"\"{correction_prompt}\"\"\"

{few_shot_examples}
"""

    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"[ERROR] {str(e)}"





# import os
# import google.generativeai as genai
# from dotenv import load_dotenv

# load_dotenv()

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# if not GEMINI_API_KEY:
#     raise EnvironmentError("Missing GEMINI_API_KEY in .env file")

# genai.configure(api_key=GEMINI_API_KEY)

# model = genai.GenerativeModel("gemini-1.5-pro") 
# def run_gemini_prompt(user_story_text, correction_prompt):
#     full_prompt = (
#         "You are a QA automation assistant.\n\n"
#         "Here is the original user story:\n"
#         f"{user_story_text}\n\n"
#         "The user has requested the following change:\n"
#         f"{correction_prompt}\n\n"
#         "Return updated QA test case tab logic in structured text (Markdown or JSON)."
#     )
#     try:
#         response = model.generate_content(full_prompt)
#         return response.text
#     except Exception as e:
#         return f"[ERROR] {str(e)}"
