from docx import Document
import pdfplumber

def extract_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        return "\n".join([page.extract_text() or "" for page in pdf.pages])

def extract_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    return "\n".join([p.text for p in doc.paragraphs])
