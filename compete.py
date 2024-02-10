import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from openai import OpenAI

# Display the logo and set the app title
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)
st.title('Competitive Edge')

# Retrieve the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=openai_api_key)

# Function to scrape content, meta description, and keywords from a URL
def scrape_competitor_data(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        content_sections = [soup.find(tag).text for tag in ['main', 'article', 'section'] if soup.find(tag)]
        content = ' '.join(content_sections).replace('\n', ' ') if content_sections else 'Content not found'
        
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        
        meta_description_content = meta_description['content'] if meta_description else 'No meta description provided'
        meta_keywords_content = meta_keywords['content'] if meta_keywords else 'No keywords provided'
        
        return {
            'url': url,
            'content': content,
            'meta_description': meta_description_content,
            'meta_keywords': meta_keywords_content
        }
    except Exception as e:
        st.error(f"Failed to scrape content: {str(e)}")
        return None

# Function to generate SEO analysis and recommendations using OpenAI
def generate_seo_analysis_and_recommendations(user_data, competitor_data):
    analysis_prompt = "Analyze the competitors' SEO strategies and provide recommendations for improvement. Include headers and bullet points for clarity. Provide specific copy examples for recommendations.\n\n"
    
    if user_data:
        analysis_prompt += f"User's Website Content: {user_data['content']}\nUser's Meta Description: {user_data['meta_description']}\nUser's Meta Keywords: {user_data['meta_keywords']}\n\n"
    
    for data in competitor_data:
        if data:
            analysis_prompt += f"Competitor's Website Content: {data['content']}\nCompetitor's Meta Description: {data['meta_description']}\nCompetitor's Meta Keywords: {data['meta_keywords']}\n\n"

    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI trained in advanced SEO, content optimization, and competitive analysis."},
                {"role": "user", "content": analysis_prompt}
            ]
        )
        recommendations = completion.choices[0].message.content
        return recommendations
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "An error occurred while generating recommendations."

# UI for input fields
user_url = st.text_input('Enter your website URL:')
competitor_urls_input = st.text_area('Enter competitor URLs (comma-separated):')

# Button to trigger analysis
if st.button('Analyze Competitors'):
    if competitor_urls_input:
        competitor_urls = [url.strip() for url in competitor_urls_input.split(',')]
        competitor_data = [scrape_competitor_data(url) for url in competitor_urls]
        user_data = scrape_competitor_data(user_url) if user_url else None
        
        recommendations = generate_seo_analysis_and_recommendations(user_data, competitor_data)
        
        st.subheader('Recommendations based on Competitor Analysis:')
        st.markdown(recommendations, unsafe_allow_html=True)
    else:
        st.warning('Please enter at least one competitor URL.')