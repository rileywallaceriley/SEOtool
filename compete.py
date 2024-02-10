import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Ensure NLTK resources are available
nltk.download('stopwords', quiet=True)

# Display the logo and app title at the top
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)
st.title('Competitive Edge')

# Retrieve API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=openai_api_key)

def extract_keywords_from_text(text):
    """Extract keywords from text based on frequency, excluding common stopwords."""
    text = text.lower()
    text = re.sub('[^a-zA-Z]', ' ', text)
    words = text.split()
    words = [word for word in words if word not in stopwords.words('english')]
    common_words = Counter(words).most_common(10)
    keywords = [word[0] for word in common_words]
    return ', '.join(keywords)

def scrape_competitor_data(url):
    """Scrape content, meta description, and keywords from a URL, extracting keywords from content if necessary."""
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        content_sections = [soup.find(tag).text for tag in ['main', 'article', 'section'] if soup.find(tag)]
        content = ' '.join(content_sections).replace('\n', ' ') if content_sections else 'Relevant content not found'
        
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        
        meta_description_content = meta_description.get('content', '').replace('\n', ' ') if meta_description else 'No meta description provided.'
        meta_keywords_content = meta_keywords.get('content', '').replace('\n', ' ') if meta_keywords else extract_keywords_from_text(content) if content != 'Relevant content not found' else 'No keywords identified in content.'
        
        return {
            'url': url,
            'content': content,
            'meta_description': meta_description_content,
            'meta_keywords': meta_keywords_content
        }
    except Exception as e:
        st.error(f"Failed to scrape content from {url}: {str(e)}")
        return None

def generate_seo_recommendations(user_data, competitor_data):
    """Generate SEO recommendations based on the user's and competitors' data."""
    recommendations = []
    
    if user_data:
        user_keywords = set(user_data['meta_keywords'].split(', '))
        all_competitor_keywords = set()
        
        for data in competitor_data:
            competitor_keywords = set(data['meta_keywords'].split(', '))
            all_competitor_keywords.update(competitor_keywords)
        
        missing_keywords = all_competitor_keywords.difference(user_keywords)
        if missing_keywords:
            recommendations.append(f"Consider incorporating these high-frequency keywords from your competitors into your content or meta tags: {', '.join(missing_keywords)}.")
        
        if not user_data['meta_description']:
            recommendations.append("Add a meta description to improve your site's SEO and click-through rate from search engine results pages.")
        
    else:
        recommendations.append("Providing your website's URL would allow for a more detailed analysis and tailored recommendations.")
    
    if not recommendations:
        recommendations.append("Your SEO practices are on par with your competitors'. Consider exploring advanced optimization techniques or focusing on content quality and user engagement.")
    
    return recommendations

# Streamlit UI for input fields
user_url = st.text_input('Enter your website URL:')
competitor_urls_input = st.text_area('Enter competitor URLs (comma-separated):')

if st.button('Analyze Competitors'):
    if competitor_urls_input:
        competitor_urls = [url.strip() for url in competitor_urls_input.split(',')]
        competitor_data = [scrape_competitor_data(url) for url in competitor_urls if url]
        user_data = scrape_competitor_data(user_url) if user_url else None

        recommendations = generate_seo_recommendations(user_data, competitor_data)
        
        st.subheader('SEO Recommendations:')
        for recommendation in recommendations:
            st.markdown(f"- {recommendation}")
    else:
        st.warning('Please enter at least one competitor URL.')