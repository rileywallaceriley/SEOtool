import streamlit as st
import textstat
import nltk

# Ensure NLTK resources are downloaded (needed if you expand the script to use NLTK for further analysis)
nltk.download('punkt')

# SEO Analysis Functions
def calculate_flesch_reading_ease(text):
    """Calculate the Flesch Reading Ease score for the input text."""
    return textstat.flesch_reading_ease(text)

def keyword_density(text, keyword):
    """Calculate the keyword density percentage for the input text."""
    words = text.lower().split()
    keyword_count = sum(1 for word in words if keyword.lower() == word)
    density = (keyword_count / len(words)) * 100
    return round(density, 2)

def headings_analysis(text):
    """Simple markdown heading analysis for SEO."""
    h1_count = text.count('# ')
    h2_count = text.count('## ')
    h3_count = text.count('### ')
    return h1_count, h2_count, h3_count

# Streamlit App UI
st.title("SEO Optimization Tool")

# User Inputs
content_type = st.radio("Content Type", ["Article/Blog", "Web Copy"], key='content_type')
keywords = st.text_input("Primary Keyword", key='keywords')

# Content Input
with st.form("content_form"):
    main_copy = st.text_area("Main Content", key='main_copy', height=300)
    analyze_button = st.form_submit_button("Analyze")

# Analysis and Results Display
if analyze_button and main_copy:
    readability_score = calculate_flesch_reading_ease(main_copy)
    kd = keyword_density(main_copy, keywords)
    h1, h2, h3 = headings_analysis(main_copy)
    
    st.header("SEO Analysis Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Readability Score", value=f"{readability_score}")
    with col2:
        st.metric(label="Keyword Density", value=f"{kd}%")
    with col3:
        st.metric(label="H1 Tags", value=f"{h1}")
    
    st.subheader("Headings Usage")
    st.markdown(f"""
    - **H2 Tags**: {h2}
    - **H3 Tags**: {h3}
    """)
    
    # Tips for Improvement
    with st.expander("Tips for Improvement"):
        st.markdown("""
        - **Readability Score**: Aim for a score above 60 for general audiences. The higher the score, the easier it is to read.
        - **Keyword Density**: Keep your keyword density between 1% and 2% to avoid keyword stuffing. Consider variations and synonyms for better results.
        - **Headings**: Use headings to structure your content logically. An H1 tag for the title, followed by H2 for main sections, and H3 for subsections, enhances readability and SEO.
        """)
