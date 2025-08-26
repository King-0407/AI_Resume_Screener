import streamlit as st
import google.generativeai as genai
import PyPDF2
import docx2txt

# Load API key from Streamlit Secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Function to extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(file):
    return docx2txt.process(file)

# Function to analyze resume
def analyze_resume(resume_text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
    You are an AI Resume Analyzer.  
    Analyze the following resume and present the results in this structured format:  

    1. Suggested Job Roles  
    2. Strengths of the Candidate  
    3. Candidate’s Areas of Interest  
    4. Resume Quality Rating (0–100)  
    5. Candidate’s Experience Level  

    Resume:  
    {resume_text}
    """
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("📄 AI Resume Analyzer (Gemini)")

uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = extract_text_from_docx(uploaded_file)

    st.subheader("✅ Resume Analysis Result")
    try:
        result = analyze_resume(resume_text)
        st.text_area("Analysis Output", result, height=400)
    except Exception as e:
        st.error(f"❌ Error during analysis: {e}")
