import streamlit as st
import spacy
from bs4 import BeautifulSoup
from textstat.textstat import textstat

# Attempt to load the spaCy model, with a fallback to download if not found
try:
    nlp = spacy.load("en_core_web_sm")
except IOError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def analyze_text(content):
    """Analyzes the text for SEO insights."""
    doc = nlp(content)
    # Basic analysis for demonstration
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return {
        "entities": entities,
        "readability_score": textstat.flesch_reading_ease(content),
    }

def extract_text_from_html(html_content):
    """Extracts clean text from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    return text

# Streamlit UI
st.title("SEO Analysis Tool")

html_content = st.text_area("Paste your HTML content here:", height=200)
if st.button("Analyze"):
    if html_content:
        text_content = extract_text_from_html(html_content)
        analysis_results = analyze_text(text_content)
        
        st.write("Readability Score:", analysis_results["readability_score"])
        st.write("Detected Entities:", analysis_results["entities"])
    else:
        st.error("Please input some HTML content to analyze.")