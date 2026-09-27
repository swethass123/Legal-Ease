import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
import streamlit as st
from dotenv import load_dotenv
from io import BytesIO
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# ------------------------------------------------
# FUNCTIONS - ITHU THAN MAIN FIX DA
# ------------------------------------------------
def format_docx(text):
    doc = Document()
    for line in text.split('\n'):
        doc.add_paragraph(line)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()

def format_pdf(text):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    y = 750
    c.setFont("Helvetica", 11)
    for line in text.split('\n'):
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = 750
        # Long line ah cut pannu
        c.drawString(40, y, line[:95])
        y -= 15
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

def format_html_preview(text): 
    return text.replace('\n', '<br>')

# ------------------------------------------------
# ENVIRONMENT
# ------------------------------------------------
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="LegalEase - Legal Document Generator",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ LegalEase - AI Legal Document Generator")
st.markdown("Simple-a legal document generate pannalam ma!")

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------
st.sidebar.header("Settings")
doc_type = st.sidebar.selectbox(
    "Document Type",
    ["Rental Agreement", "Employment Contract", "NDA", "Service Agreement", "Partnership Deed"]
)

# ------------------------------------------------
# FORM
# ------------------------------------------------
with st.form("legal_form"):
    st.subheader("Details Fill pannunga ma")
    col1, col2 = st.columns(2)
    with col1:
        party1 = st.text_input("Party 1 Name")
        address1 = st.text_area("Party 1 Address")
    with col2:
        party2 = st.text_input("Party 2 Name")
        address2 = st.text_area("Party 2 Address")
    purpose = st.text_area("Purpose / Terms", placeholder="Ex: Rent amount, duration, conditions...")
    submitted = st.form_submit_button("Generate Document")

# ------------------------------------------------
# GENERATE
# ------------------------------------------------
if submitted:
    if not party1 or not party2 or not purpose:
        st.error("Ellam fill pannunga ma!")
    else:
        with st.spinner("Document generate aaguthu ma..."):
            try:
                payload = {
                    "doc_type": doc_type,
                    "party1_name": party1,
                    "party1_address": address1,
                    "party2_name": party2,
                    "party2_address": address2,
                    "terms": purpose,
                    "purpose": purpose
                }
                
                response = requests.post(f"{BACKEND_URL}/generate", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    document_text = data.get("document", "")
                    st.success("Document Ready ma!")
                    
                    st.subheader("Preview")
                    html_preview = format_html_preview(document_text)
                    st.markdown(html_preview, unsafe_allow_html=True)
                    
                    st.subheader("Download")
                    col1, col2 = st.columns(2)
                    with col1:
                        docx_file = format_docx(document_text)
                        st.download_button(
                            "Download as DOCX",
                            data=docx_file,
                            file_name=f"{doc_type}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    with col2:
                        pdf_file = format_pdf(document_text)
                        st.download_button(
                            "Download as PDF",
                            data=pdf_file,
                            file_name=f"{doc_type}.pdf",
                            mime="application/pdf"
                        )
                else:
                    st.error(f"Error: {response.text}")
            
            except Exception as e:
                st.error(f"Backend connect aagala ma: {e}")
