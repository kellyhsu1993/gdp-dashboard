# -*- coding: utf-8 -*-
"""Hackathon_UI.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/junyizhou0304/deloitte_hackathon/blob/master/Hackathon_UI.ipynb
"""

import streamlit as st
import openai
import faiss
import json
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF

# Load preprocessed knowledge data (FAISS embeddings & metadata)
def load_data():
    return "FAISS index loaded"

# Function to retrieve relevant content
def retrieve_answer(question):
    return {
        "answer": "BCIT partnered with Indigenous Communities for Renewable Energy projects.",
        "sources": ["BCIT Strategic Plan 2023"],
        "metadata": {"institution": "BCIT", "document_type": "Strategic Plan", "year": 2023},
    }

# Function to generate a downloadable PDF report
def generate_pdf(query, result):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Deloitte AI Research Assistant Report", ln=True, align='C')

    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Query: {query}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, "AI-Generated Answer:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, result["answer"])

    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, "Source Documents:", ln=True)
    pdf.set_font("Arial", size=12)
    for src in result["sources"]:
        pdf.cell(200, 10, f"- {src}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, "Metadata:", ln=True)
    pdf.set_font("Arial", size=12)
    for key, value in result["metadata"].items():
        pdf.cell(200, 10, f"{key.capitalize()}: {value}", ln=True)

    # Convert PDF to downloadable format
    pdf_output = BytesIO()
    pdf.output(pdf_output, 'F')
    return pdf_output.getvalue()

# Streamlit UI
st.set_page_config(page_title="Deloitte AI Research Assistant", layout="wide")

st.title("📊 Deloitte’s AI Research Assistant")
st.write("Ask questions about BC post-secondary institutions, and get AI-powered insights.")

# User input
query = st.text_input("🔍 Ask a question (e.g., 'Which colleges offer AI-related diplomas?')")

if query:
    result = retrieve_answer(query)
    st.subheader("💡 AI-Generated Answer")
    st.write(result["answer"])

    # Display citations
    st.subheader("📄 Source Documents")
    for src in result["sources"]:
        st.write(f"- {src}")

    # Feedback mechanism
    st.subheader("📢 Feedback")
    col1, col2 = st.columns(2)
    with col1:
        st.button("👍 Helpful")
    with col2:
        st.button("👎 Needs Improvement")

    # Download Report
    st.subheader("📥 Download Report")
    pdf_data = generate_pdf(query, result)
    st.download_button(label="📄 Download as PDF", data=pdf_data, file_name="AI_Research_Report.pdf", mime="application/pdf")

# Sidebar Filters
st.sidebar.header("🔎 Filter Results")
institution = st.sidebar.selectbox("Institution", ["All", "BCIT", "UBC", "SFU", "UVic"])
doc_type = st.sidebar.selectbox("Document Type", ["All", "Strategic Plan", "Financial Statement", "Mandate Letter"])

st.sidebar.markdown("💡 AI-driven research insights tailored for Deloitte consultants.")

# Visual Analytics Dashboard
st.sidebar.header("📊 Analytics Dashboard")

# Example Data for Visualization
analytics_data = pd.DataFrame({
    "Institution": ["BCIT", "UBC", "SFU", "UVic", "Capilano"],
    "Mentions": [35, 42, 30, 25, 20]
})

st.sidebar.subheader("Institution Mentions")
fig, ax = plt.subplots()
ax.bar(analytics_data["Institution"], analytics_data["Mentions"], color=['blue', 'red', 'green', 'purple', 'orange'])
ax.set_ylabel("Mentions")
ax.set_xlabel("Institution")
st.sidebar.pyplot(fig)

# Trend Graph (Example Data)
st.sidebar.subheader("Document Type Distribution")
doc_data = pd.DataFrame({
    "Document Type": ["Strategic Plan", "Financial Statement", "Mandate Letter"],
    "Count": [45, 30, 25]
})

fig2, ax2 = plt.subplots()
ax2.pie(doc_data["Count"], labels=doc_data["Document Type"], autopct="%1.1f%%", colors=['cyan', 'magenta', 'yellow'])
st.sidebar.pyplot(fig2)

st.sidebar.markdown("📌 Use analytics to track institution trends & document insights.")
