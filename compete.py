import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Streamlit app title
st.title('SEO Competitive Analysis Tool')

# Download necessary NLTK datasets
@st.cache(allow_output_mutation=True)
def download_nltk_data():
    nltk.download('stopwords')
    return True

# Check if NLTK data is downloaded
if download_nltk_data():
    st.sidebar.success("NLTK Data Ready!")

# Display the logo and app title at the top
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)

# Function to extract keywords based on text frequency
def extract_keywords_from_text(text):
    text = text.lower()
    text = re.sub('[^a-zA-Z]', ' ', text)
    words = text.split()
    words = [word for word in words if word not in stopwords.words('english')]
    common_words = Counter(words).most_common(10)
    keywords = [word[0] for word in common_words]
    return ', '.join(keywords)

# Function to scrape competitor data
def scrape_competitor_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        content_sections = [soup.find(tag).text for tag in ['main', 'article', 'section'] if soup.find(tag)]
        content = ' '.join(content_sections).replace('\n', ' ') if content_sections else 'Content not found'
        
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        
        meta_description_content = meta_description['content'] if meta_description else 'No meta description provided'
        meta_keywords_content = meta_keywords['content'] if meta_keywords else extract_keywords_from_text(content)
        
        return {
            'url': url,
            'content': content,
            'meta_description': meta_description_content,
            'meta_keywords': meta_keywords_content
        }
    except Exception as e:
        return {'url': url, 'error': str(e)}

# Function to generate SEO recommendations
def generate_seo_recommendations(user_data, competitor_data):
    recommendations = []
    
    # Analysis and recommendation generation logic goes here
    # This is a placeholder for the actual logic
    
    return recommendations

# User input for URLs
user_url = st.text_input('Enter your website URL:')
competitor_urls_input = st.text_area('Enter competitor URLs (comma-separated):')

# Button to trigger analysis
if st.button('Analyze Competitors'):
    if competitor_urls_input:
        competitor_urls = [url.strip() for url in competitor_urls_input.split(',')]
        competitor_data = [scrape_competitor_data(url) for url in competitor_urls]
        user_data = scrape_competitor_data(user_url) if user_url else {}
        
        recommendations = generate_seo_recommendations(user_data, competitor_data)
        
        # Displaying recommendations
        if recommendations:
            for recommendation in recommendations:
                st.write(recommendation)
        else:
            st.write("No recommendations available.")
    else:
        st.warning('Please enter at least one competitor URL.')