import streamlit as st
import nltk
from bs4 import BeautifulSoup
from textstat.textstat import textstat
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

def calculate_keyword_density(text, keyword):
    """Calculate keyword density in the given text."""
    words = word_tokenize(text.lower())
    keyword_count = sum(word == keyword.lower() for word in words)
    total_words = len(words)
    return (keyword_count / total_words) * 100 if total_words > 0 else 0

def analyze_text(content, primary_keyword):
    """Analyzes the text for basic insights including keyword density."""
    tokens = word_tokenize(content)
    tagged_tokens = nltk.pos_tag(tokens)
    
    # Basic Part-of-Speech counts
    pos_counts = {
        "Nouns": sum(1 for word, pos in tagged_tokens if pos.startswith('NN')),
        "Verbs": sum(1 for word, pos in tagged_tokens if pos.startswith('VB')),
        "Adjectives": sum(1 for word, pos in tagged_tokens if pos.startswith('JJ')),
    }
    
    # Readability and keyword density
    readability_score = textstat.flesch_reading_ease(content)
    keyword_density = calculate_keyword_density(content, primary_keyword)
    
    return {
        "pos_counts": pos_counts,
        "readability_score": readability_score,
        "keyword_density": keyword_density,
    }

def extract_text_from_html(html_content):
    """Extracts clean text from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    return text

# Streamlit UI for SEO Analysis Tool
st.title("SEO Analysis Tool Using NLTK")

# User inputs for HTML content and primary keyword
html_content = st.text_area("Paste your HTML content here:", height=200)
primary_keyword = st.text_input("Primary Keyword")
if st.button("Analyze"):
    if html_content and primary_keyword:
        text_content = extract_text_from_html(html_content)
        analysis_results = analyze_text(text_content, primary_keyword)
        
        # Display the analysis results
        st.write("Readability Score:", analysis_results["readability_score"])
        st.write("Keyword Density (%):", analysis_results["keyword_density"])
        st.write("Part-of-Speech Counts:", analysis_results["pos_counts"])
    else:
        st.error("Please input both HTML content and a primary keyword to analyze.")