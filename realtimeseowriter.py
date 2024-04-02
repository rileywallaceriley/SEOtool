import streamlit as st
from textstat import textstat
from bs4 import BeautifulSoup
import re

# Initialize Streamlit app
st.title("Enhanced SEO Optimization Tool for HTML Content")

# Function definitions
def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def keyword_density_improved(html_content, keyword):
    text = extract_text_from_html(html_content).lower()
    keyword_matches = re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text)
    words = text.split()
    return round((len(keyword_matches) / len(words)) * 100, 2) if words else 0

def count_html_headings(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 4)}

def analyze_links_and_images(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')
    internal_links = [link for link in links if 'http' not in link.get('href', '')]
    external_links = [link for link in links if 'http' in link.get('href', '')]
    images = soup.find_all('img')
    images_with_alt = [img for img in images if img.has_attr('alt') and img['alt'].strip()]
    
    return len(links), len(internal_links), len(external_links), len(images), len(images_with_alt)

def provide_guidance(readability_score, keyword_density, headings_count, links, internal_links, external_links, images, images_with_alt):
    guidance = []
    # Existing guidance...
    # Add new guidance for links and images
    if external_links > 0:
        guidance.append("✅ Good job including external links.")
    else:
        guidance.append("❌ Consider adding external links to reputable sources.")
        
    if internal_links > 0:
        guidance.append("✅ Proper use of internal links.")
    else:
        guidance.append("❌ Add more internal links to improve site navigation and SEO.")
        
    if images_with_alt < images:
        missing_alt = images - images_with_alt
        guidance.append(f"❌ {missing_alt} images are missing 'alt' attributes. Add 'alt' text to improve accessibility and SEO.")
    else:
        guidance.append("✅ All images have 'alt' attributes. Great for SEO and accessibility.")
    
    return "\n".join(guidance)

# User Inputs
content_type = st.radio("Content Type", ["Article/Blog", "Web Copy"], key='content_type')
keywords = st.text_input("Primary Keyword", key='keywords')
html_content = st.text_area("Paste your HTML content here", height=300, key='html_content')

# Analyze button
if st.button("Analyze HTML Content"):
    if html_content and keywords:
        readability_score = textstat.flesch_reading_ease(extract_text_from_html(html_content))
        kd = keyword_density_improved(html_content, keywords)
        headings_count = count_html_headings(html_content)
        links, internal_links, external_links, images, images_with_alt = analyze_links_and_images(html_content)
        
        # Display analysis results
        st.header("SEO Analysis Results")
        st.metric("Readability Score", readability_score)
        st.metric("Keyword Density", f"{kd}%")
        st.metric("Links (Total/Internal/External)", f"{links}/{internal_links}/{external_links}")
        st.metric("Images (Total/With Alt Tags)", f"{images}/{images_with_alt}")
        
        # Display guidance based on the analysis
        guidance_text = provide_guidance(readability_score, kd, headings_count, links, internal_links, external_links, images, images_with_alt)
        st.subheader("Improvement Suggestions")
        st.markdown(guidance_text)
    else:
        st.error("Please ensure both primary keyword and HTML content are provided.")

# Final notes and suggestions
st.markdown("""
**Note:** This tool now provides a broader SEO analysis, including readability, keyword density, link usage, and image alt attributes. Consider adding more features like schema markup analysis, social media tags inspection, and page speed insights for a comprehensive SEO audit tool.
""")