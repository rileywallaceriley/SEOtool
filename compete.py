import os
import re
import requests
from bs4 import BeautifulSoup
from collections import Counter
import streamlit as st

# Define a basic list of stopwords
stopwords = set([
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
    "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers",
    "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are",
    # Add more stopwords as needed
])

# Function to extract keywords from text
def extract_keywords_from_text(text):
    text = text.lower()
    words = re.findall(r'\b[a-z]+\b', text)
    filtered_words = [word for word in words if word not in stopwords]
    word_counts = Counter(filtered_words)
    common_words = word_counts.most_common(10)
    keywords = [word[0] for word in common_words]
    return ', '.join(keywords)

# Function to scrape content, meta description, and keywords from a URL
def scrape_competitor_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        content_sections = [soup.find(tag).text for tag in ['main', 'article', 'section'] if soup.find(tag)]
        content = ' '.join(content_sections).replace('\n', ' ') if content_sections else 'Content not found'
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_description_content = meta_description['content'] if meta_description else 'No meta description provided'
        meta_keywords_content = extract_keywords_from_text(content)
        
        return {
            'url': url,
            'meta_description': meta_description_content,
            'meta_keywords': meta_keywords_content
        }
    except Exception as e:
        return {'url': url, 'error': str(e)}

# Streamlit UI with structured output
st.title('SEO Competitive Analysis Tool')
user_url = st.text_input('Enter your website URL:')
competitor_urls_input = st.text_area('Enter competitor URLs (comma-separated):')

if st.button('Analyze Competitors'):
    if competitor_urls_input:
        competitor_urls = [url.strip() for url in competitor_urls_input.split(',')]
        competitor_data = [scrape_competitor_data(url) for url in competitor_urls]
        user_data = scrape_competitor_data(user_url) if user_url else {}

        # Displaying the analysis in a structured format
        if user_data:
            st.subheader('Your Website Analysis')
            st.write(f"**URL:** {user_url}")
            st.write(f"**Meta Description:** {user_data.get('meta_description', 'Not found')}")
            st.write(f"**Extracted Keywords:** {user_data.get('meta_keywords', 'Not found')}")
        
        st.subheader('Competitor Analysis')
        for data in competitor_data:
            st.markdown(f"**URL:** {data.get('url')}")
            st.markdown(f"**Meta Description:** {data.get('meta_description', 'Not found')}")
            st.markdown(f"**Extracted Keywords:** {data.get('meta_keywords', 'Not found')}")
            st.markdown("---")

        # Placeholder for SEO Recommendations based on analysis
        st.subheader('SEO Recommendations')
        st.markdown("""
        - **Enhance Your Meta Descriptions**: Ensure they are compelling and contain relevant keywords.
        - **Review Your Content**: Incorporate keywords that are frequently used by your competitors but are missing from your content.
        - **Monitor Your Competitors**: Regularly check their SEO strategies and adapt your approach accordingly.
        """)
    else:
        st.warning('Please enter at least one competitor URL.')