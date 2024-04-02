import streamlit as st
from textstat import textstat
from bs4 import BeautifulSoup
import spacy
import re

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def extract_text_and_elements_from_html(html_content):
    """Extract text and HTML elements using BeautifulSoup."""
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    images = soup.find_all('img')
    links = soup.find_all('a')
    return text, images, links

def analyze_keyword_density(text, keyword):
    """Calculate keyword density within text."""
    words = text.split()
    matches = sum(1 for word in words if word.lower() == keyword.lower())
    return round((matches / len(words)) * 100, 2) if words else 0

def find_sentences_for_improvement(text):
    """Identify complex and passive voice sentences using spaCy."""
    doc = nlp(text)
    complex_sentences = [sent.text for sent in doc.sents if len(sent) > 20][:3]
    passive_sentences = [sent.text for sent in doc.sents if any(tok.dep_ == "auxpass" for tok in sent)][:3]
    return complex_sentences, passive_sentences

def provide_seo_suggestions(complex_sentences, passive_sentences, images, links):
    """Generate SEO suggestions based on content analysis."""
    suggestions = []
    if complex_sentences:
        suggestions.append("Consider simplifying complex sentences for better readability.")
    if passive_sentences:
        suggestions.append("Try to use active voice instead of passive for clarity.")
    if not any(img.get('alt') for img in images):
        suggestions.append("Add 'alt' text to all images to improve SEO and accessibility.")
    if not all('http' in link.get('href', '') for link in links):
        suggestions.append("Verify all external links start with 'http'.")
    return suggestions if suggestions else ["Content looks good from an SEO perspective!"]

# Streamlit UI setup
st.title("Comprehensive SEO Analysis Tool")

# User inputs
html_content = st.text_area("Paste your HTML content here", height=300)
primary_keyword = st.text_input("Primary Keyword")
analyze_button = st.button("Analyze Content")

if analyze_button and html_content and primary_keyword:
    # Analysis
    text, images, links = extract_text_and_elements_from_html(html_content)
    readability_score = textstat.flesch_reading_ease(text)
    keyword_density = analyze_keyword_density(text, primary_keyword)
    complex_sentences, passive_sentences = find_sentences_for_improvement(text)
    seo_suggestions = provide_seo_suggestions(complex_sentences, passive_sentences, images, links)
    
    # Displaying results
    st.metric("Readability Score", readability_score)
    st.metric("Keyword Density", f"{keyword_density}%")
    st.subheader("Complex Sentences (Examples):")
    for sentence in complex_sentences:
        st.markdown(f"- *{sentence}*")
    st.subheader("Passive Voice Sentences (Examples):")
    for sentence in passive_sentences:
        st.markdown(f"- *{sentence}*")
    st.subheader("SEO Suggestions:")
    for suggestion in seo_suggestions:
        st.markdown(f"- {suggestion}")

else:
    st.error("Please ensure both primary keyword and HTML content are provided.")
