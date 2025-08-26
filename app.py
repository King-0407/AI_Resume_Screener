import os
import docx2txt
import PyPDF2
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ✅ Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# ---------- Utility Functions ----------
# Extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Extract text from DOCX
def extract_text_from_docx(file):
    return docx2txt.process(file)

# Analyze resume with Gemini
def analyze_resume(resume_text):
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    You are an AI Resume Analyzer.  
    Analyze the following resume and present the results in STRICTLY this structured format:  

    1️⃣ Suggested Job Roles:  
    - Role 1  
    - Role 2  
    - Role 3  

    2️⃣ Strengths of the Candidate:  
    - Skill 1 - %  
    - Skill 2 - %  
    - Skill 3 - %  

    3️⃣ Candidate’s Areas of Interest:  
    - Area 1  
    - Area 2  
    - Area 3  
    
    4️⃣ Resume Quality Rating:  
           - Provide a score from 0 to 100 based on the resume’s structure, grammar, keyword richness, and overall readability.  
           - Include a brief explanation of the score.  

    5️⃣ Candidate’s Experience Level:  
        - Total years of professional experience  
        - Seniority level (Entry-level, Mid-level, Senior)  
        - Relevant industry experience (e.g., IT, Healthcare, Finance)  

    🔹 Very Important:  
    - Do NOT use ** ** for highlighting.  
    - Use simple dash (-) or arrow (➡) for points.  
    - Keep it concise and pointwise only, no long paragraphs.  

    Resume:  
    {resume_text}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error during analysis: {str(e)}"

# ---------- Streamlit UI ----------
st.set_page_config(page_title="AI Resume Analyzer", page_icon="🤖", layout="centered")

st.title("📄 AI Resume Analyzer (Gemini)")
st.write("Upload your *resume (PDF or DOCX)* and let AI analyze it.")

uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx"])

if uploaded_file is not None:
    with st.spinner("Extracting text..."):
        if uploaded_file.name.endswith(".pdf"):
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            text = extract_text_from_docx(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload PDF or DOCX.")
            text = None

    if text:
        with st.spinner("Analyzing with Gemini..."):
            result = analyze_resume(text)

        st.subheader("✅ Resume Analysis Result")
        st.write(result)