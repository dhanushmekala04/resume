import re
import streamlit as st
from pdfminer.high_level import extract_text
import spacy
from spacy.matcher import Matcher

# Functions from your original code
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def extract_contact_number_from_resume(text):
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_email_from_resume(text):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_skills_from_resume(text, skills_list):
    skills = [skill for skill in skills_list if re.search(rf'\b{re.escape(skill)}\b', text, re.IGNORECASE)]
    return skills

def extract_education_from_resume(text):
    pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+"
    matches = re.findall(pattern, text)
    return [match.strip() for match in matches]

def extract_name(resume_text):
    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)
    patterns = [
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]
    ]
    for pattern in patterns:
        matcher.add('NAME', patterns=[pattern])
    doc = nlp(resume_text)
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        return span.text
    return None

# Streamlit application
def main():
    st.title("Resume Information Extractor")

    # File uploader for PDF resumes
    uploaded_file = st.file_uploader("Upload a PDF resume", type=["pdf"])
    
    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        text = extract_text(uploaded_file)
        st.subheader("Extracted Text")
        st.write(text)

        # Extract and display information
        name = extract_name(text)
        if name:
            st.write("**Name:**", name)
        else:
            st.write("**Name not found**")

        contact_number = extract_contact_number_from_resume(text)
        if contact_number:
            st.write("**Contact Number:**", contact_number)
        else:
            st.write("**Contact Number not found**")

        email = extract_email_from_resume(text)
        if email:
            st.write("**Email:**", email)
        else:
            st.write("**Email not found**")

        skills_list = ['Python', 'Data Analysis', 'Machine Learning', 'Communication', 'Project Management', 'Deep Learning', 'SQL', 'Tableau']
        extracted_skills = extract_skills_from_resume(text, skills_list)
        if extracted_skills:
            st.write("**Skills:**", extracted_skills)
        else:
            st.write("**No skills found**")

        extracted_education = extract_education_from_resume(text)
        if extracted_education:
            st.write("**Education:**", extracted_education)
        else:
            st.write("**No education information found**")

if __name__ == '__main__':
    main()


