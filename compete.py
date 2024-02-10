import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# Display the logo at the top of the app
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)

st.title('Competitive Edge')

# Retrieve API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=openai_api_key)

# Function to scrape content and meta from a URL
def scrape_competitor_data(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Get main content and additional sections for a comprehensive analysis
        content_sections = [soup.find(tag).text for tag in ['main', 'article', 'section'] if soup.find(tag)]
        content = ' '.join(content_sections).replace('\n', ' ') if content_sections else 'Relevant content not found'
        
        # Get meta tags (description and keywords)
        meta_description = soup.find('meta', attrs={'name': 'description'}) or ''
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'}) or ''
        
        if meta_description:
            meta_description = meta_description.get('content', '').replace('\n', ' ')
        if meta_keywords:
            meta_keywords = meta_keywords.get('content', '').replace('\n', ' ')
        
        return {
            'content': content,
            'meta_description': meta_description,
            'meta_keywords': meta_keywords
        }
    except Exception as e:
        st.error(f"Failed to scrape content: {str(e)}")
        return {
            'content': 'Exception occurred',
            'meta_description': '',
            'meta_keywords': ''
        }

# Function to generate SEO analysis and recommendations
def generate_seo_analysis_and_recommendations(user_data, competitor_data):
    analysis_prompt = "Analyze the competitors' SEO strategies and provide recommendations for improvement. Include headers and bullet points for clarity. Provide specific copy examples for recommendations.\n\n"
    
    # Append user's data to the prompt if available
    if user_data:
        analysis_prompt += f"User's Website Content: {user_data['content']}\nUser's Meta Description: {user_data['meta_description']}\nUser's Meta Keywords: {user_data['meta_keywords']}\n\n"
    
    # Append competitors' data to the prompt
    for data in competitor_data:
        analysis_prompt += f"Competitor's Website Content: {data['content']}\nCompetitor's Meta Description: {data['meta_description']}\nCompetitor's Meta Keywords: {data['meta_keywords']}\n\n"

    messages = [
        {"role": "system", "content": "You are an AI trained in advanced SEO, content optimization, and competitive analysis."},
        {"role": "user", "content": analysis_prompt}
    ]
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4",  # Specify your desired model version here
            messages=messages
        )
        recommendations = completion.choices[0].message.content
        # Format recommendations for better readability
        formatted_recommendations = recommendations.replace('\n', '<