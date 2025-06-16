
import streamlit as st
import fitz  # PyMuPDF
from scorer import score_resume, analyze_resume_sections
from keywords import DOMAIN_KEYWORDS

st.set_page_config(page_title="Resume Scorer", layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #ffffff;
            color: #222;
        }
        .title {
            font-size: 2.2em;
            color: #1a1a1a;
            font-weight: 800;
            margin-bottom: 10px;
        }
        .section {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            border: 1px solid #ddd;
        }
        .highlight {
            color: #1a73e8;
            font-weight: bold;
        }
        .suggestion {
            color: #d00000;
            font-weight: 500;
        }
        .heading {
            font-weight: 700;
            font-size: 1.2em;
            margin-bottom: 0.5em;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>📄 AI Resume Scorer</div>", unsafe_allow_html=True)

domain = st.selectbox("📘 Select Domain", list(DOMAIN_KEYWORDS.keys()))
uploaded_file = st.file_uploader("📤 Upload Resume (PDF only)", type=["pdf"])

if uploaded_file:
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    score, breakdown, suggestions, missing_keywords = score_resume(text, domain)
    section_feedback = analyze_resume_sections(text)

    st.markdown(f"<div class='section'><div class='heading'>📊 Total Score:</div><span class='highlight'>{score} / 10</span></div>", unsafe_allow_html=True)

    st.markdown("<div class='section'><div class='heading'>🔍 Score Breakdown</div>", unsafe_allow_html=True)
    for k, v in breakdown.items():
        st.markdown(f"- **{k}**: {v}/10")
    st.markdown("</div>", unsafe_allow_html=True)

    if missing_keywords:
        st.markdown("<div class='section'><div class='heading'>🚫 Missing Keywords</div>", unsafe_allow_html=True)
        for kw in missing_keywords:
            st.markdown(f"<span class='highlight'>• {kw}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if section_feedback:
        st.markdown("<div class='section'><div class='heading'>📌 Section Feedback</div>", unsafe_allow_html=True)
        for fb in section_feedback:
            st.markdown(f"- <span class='suggestion'>{fb}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if suggestions:
        st.markdown("<div class='section'><div class='heading'>💡 Personalized Suggestions</div>", unsafe_allow_html=True)
        for s in suggestions:
            st.markdown(f"- <span class='suggestion'>{s}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section'><div class='heading'>🧠 Bonus Resume Tips</div><ul>"
                "<li>Use action verbs like <b>led</b>, <b>managed</b>, <b>executed</b>.</li>"
                "<li>Quantify results when possible (e.g., 'reduced errors by 15%').</li>"
                "<li>Ensure consistent formatting and clean alignment.</li>"
                "<li>Mention certifications relevant to the chosen domain.</li>"
                "</ul></div>", unsafe_allow_html=True)
