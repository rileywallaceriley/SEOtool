import streamlit as st
import nltk
from bs4 import BeautifulSoup
from textstat.textstat import textstat
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

def analyze_text(content):
    """Analyzes the text for basic insights."""
    tokens = word_tokenize(content)
    tagged_tokens = nltk.pos_tag(tokens)
    
    # Calculate the number of nouns, verbs, and adjectives as an example analysis
    pos_counts = {
        "Nouns": sum(1 for word, pos in tagged_tokens if pos.startswith('NN')),
        "Verbs": sum(1 for word, pos in tagged_tokens if pos.startswith('VB')),
        "Adjectives": sum(1 for word, pos in tagged_tokens if pos.startswith('JJ'))
    }
    
    # Remove stopwords for keyword density analysis
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    total_words = len(filtered_tokens)
    
    return {
        "total_words": total_words,
        "pos_counts": pos_counts,
        "readability_score": textstat.flesch_reading_ease(content),
    }

def extract_text_from_html(html_content):
    """Extracts clean text from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    return text

# Streamlit UI
st.title("SEO Analysis Tool Using NLTK")

html_content = st.text_area("Paste your HTML content here:", height=200)
if st.button("Analyze"):
    if html_content:
        text_content = extract_text_from_html(html_content)
        analysis_results = analyze_text(text_content)
        
        st.write("Readability Score:", analysis_results["readability_score"])
        st.write("Word Count (excluding common stopwords):", analysis_results["total_words"])
        st.write("Part-of-Speech Counts:", analysis_results["pos_counts"])
    else:
        st.error("Please input some HTML content to analyze.")