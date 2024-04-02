import streamlit as st
from textstat import textstat
from bs4 import BeautifulSoup
import re

# Initialize Streamlit app
st.title("SEO Optimization Tool for HTML Content")

# Function to extract text from HTML, useful for various analyses
def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    return text

# Improved keyword density calculation
def keyword_density_improved(html_content, keyword):
    text = extract_text_from_html(html_content).lower()
    keyword_matches = re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text)
    words = text.split()
    density = (len(keyword_matches) / len(words)) * 100 if words else 0
    return round(density, 2)

# Count HTML heading tags
def count_html_headings(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    headings_count = {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 4)}
    return headings_count

# Provide guidance based on analysis results
def provide_guidance(readability_score, keyword_density, headings_count):
    guidance = []
    if readability_score >= 60:
        guidance.append("✅ Readability is good. The text is easy to read.")
    else:
        guidance.append("❌ Readability could be improved. Consider simplifying the text.")

    if 1 <= keyword_density <= 2:
        guidance.append("✅ Keyword density is optimal.")
    else:
        guidance.append("❌ Keyword density could be improved. Aim for 1-2% for best SEO performance.")

    if headings_count['h1'] == 1:
        guidance.append("✅ Good use of H1 tag.")
    else:
        guidance.append("❌ Ensure there is exactly one H1 tag for the title.")

    # Add more specific guidance based on H2, H3 tags
    return "\n".join(guidance)

# User Inputs
content_type = st.radio("Content Type", ["Article/Blog", "Web Copy"], key='content_type')
keywords = st.text_input("Primary Keyword", key='keywords')
html_content = st.text_area("Paste your HTML content here", height=300, key='html_content')

# Analyze button
if st.button("Analyze HTML Content"):
    if html_content and keywords:
        # Perform the analysis
        readability_score = textstat.flesch_reading_ease(extract_text_from_html(html_content))
        kd = keyword_density_improved(html_content, keywords)
        headings_count = count_html_headings(html_content)
        
        # Display the analysis results
        st.header("SEO Analysis Results")
        st.metric(label="Readability Score", value=f"{readability_score}")
        st.metric(label="Keyword Density", value=f"{kd}%")
        for tag, count in headings_count.items():
            st.metric(label=f"{tag.upper()} Tags", value=f"{count}")
        
        # Display guidance based on the analysis
        guidance_text = provide_guidance(readability_score, kd, headings_count)
        st.subheader("Improvement Suggestions")
        st.markdown(guidance_text)
    else:
        st.error("Please ensure both primary keyword and HTML content are provided.")

# Final notes
st.markdown("""
**Note:** This tool provides initial SEO analysis focused on readability, keyword density, and use of headings. 
For comprehensive optimization, consider additional factors such as meta tags, alt text for images, and internal/external linking strategies.
""")
