import streamlit as st
from textstat import textstat
from bs4 import BeautifulSoup
import re

# Improved keyword density calculation that focuses on whole word matches
def keyword_density_improved(html_content, keyword):
    text = extract_text_from_html(html_content).lower()
    # Regex to find whole word matches only, respecting keyword boundaries
    keyword_matches = re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text)
    words = text.split()
    density = (len(keyword_matches) / len(words)) * 100 if words else 0
    return round(density, 2)

# Including guidance and benchmarks in the analysis results
def provide_guidance(readability_score, keyword_density, headings_count):
    guidance = []
    if readability_score >= 60:
        guidance.append("Readability is good. The text is easy to read.")
    else:
        guidance.append("Readability could be improved. Consider simplifying the text.")

    if 1 <= keyword_density <= 2:
        guidance.append("Keyword density is optimal.")
    else:
        guidance.append("Keyword density could be improved. Aim for 1-2% for best SEO performance.")

    if headings_count['h1'] == 1:
        guidance.append("Good use of H1 tag.")
    else:
        guidance.append("Ensure there is exactly one H1 tag for the title.")

    if headings_count['h2'] >= 2:
        guidance.append("Good use of H2 tags to structure content.")
    else:
        guidance.append("Consider using more H2 tags to structure your content into sections.")

    # Additional guidance based on H3 usage and other checks can be added similarly
    return "\n".join(guidance)

# Update the section where analysis results are displayed to include guidance
if st.button("Analyze HTML Content"):
    if html_content:
        readability_score = textstat.flesch_reading_ease(extract_text_from_html(html_content))
        kd = keyword_density_improved(html_content, keywords)
        headings_count = count_html_headings(html_content)
        
        st.header("SEO Analysis Results")
        st.metric(label="Readability Score", value=f"{readability_score}")
        st.metric(label="Keyword Density", value=f"{kd}%")
        for tag, count in headings_count.items():
            st.metric(label=f"{tag.upper()} Tags", value=f"{count}")
        
        # Display guidance based on the analysis
        guidance_text = provide_guidance(readability_score, kd, headings_count)
        st.subheader("Improvement Suggestions")
        st.write(guidance_text)
    else:
        st.error("Please paste HTML content to analyze.")
