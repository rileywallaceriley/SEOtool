import streamlit as st
from textstat import textstat
from bs4 import BeautifulSoup

# Updated functions to handle HTML content
def extract_text_from_html(html_content):
    """Extracts and returns all text from the HTML content."""
    soup = BeautifulSoup(html_content, 'lxml')  # 'html.parser' as an alternative
    text = soup.get_text(separator=' ', strip=True)
    return text

def count_html_headings(html_content):
    """Counts HTML heading tags (H1, H2, H3) in the provided HTML content."""
    soup = BeautifulSoup(html_content, 'lxml')
    headings_count = {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 4)}
    return headings_count

def keyword_density_in_html(html_content, keyword):
    """Calculate the keyword density within HTML content."""
    text = extract_text_from_html(html_content)
    words = text.lower().split()
    keyword_count = sum(1 for word in words if keyword.lower() == word)
    density = (keyword_count / len(words)) * 100 if words else 0
    return round(density, 2)

# Streamlit UI
st.title("SEO Optimization Tool - HTML Content Analysis")

content_type = st.radio("Content Type", ["Article/Blog", "Web Copy"], key='content_type')
keywords = st.text_input("Primary Keyword", key='keywords')
html_content = st.text_area("Paste your HTML content here", height=300, key='html_content')

if st.button("Analyze HTML Content"):
    if html_content:
        # Perform the analysis
        readability_score = textstat.flesch_reading_ease(extract_text_from_html(html_content))
        kd = keyword_density_in_html(html_content, keywords)
        headings_count = count_html_headings(html_content)
        
        # Display the analysis results
        st.header("SEO Analysis Results")
        st.metric(label="Readability Score", value=f"{readability_score}")
        st.metric(label="Keyword Density", value=f"{kd}%")
        
        st.subheader("Headings Usage")
        for tag, count in headings_count.items():
            st.metric(label=f"{tag.upper()} Tags", value=f"{count}")

        # Add more analyses as needed
    else:
        st.error("Please paste HTML content to analyze.")
