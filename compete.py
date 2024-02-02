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
        
        # Get main content
        content = soup.find('main').text if soup.find('main') else 'Main content not found'
        
        # Get meta tags (description and keywords)
        meta_description = soup.find('meta', attrs={'name': 'description'}) or ''
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'}) or ''
        
        if meta_description:
            meta_description = meta_description.get('content')
        if meta_keywords:
            meta_keywords = meta_keywords.get('content')
        
        return {
            'content': content.replace('\n', ' '),
            'meta_description': meta_description.replace('\n', ' '),
            'meta_keywords': meta_keywords.replace('\n', ' ')
        }
    except Exception as e:
        return {
            'content': 'Failed to scrape content',
            'meta_description': '',
            'meta_keywords': ''
        }

# Function to generate recommendations based on competitors' data
def generate_recommendations(competitor_data):
    # Consolidate competitor content and meta data
    all_content = ' '.join([data['content'] for data in competitor_data])
    all_meta_descriptions = ' '.join([data['meta_description'] for data in competitor_data])
    all_meta_keywords = ', '.join([data['meta_keywords'] for data in competitor_data])
    
    # Use OpenAI's GPT model to generate recommendations based on the consolidated data
    prompt = (
        f"Generate new meta and main copy blurbs based on the following content: {all_content}, "
        f"meta descriptions: {all_meta_descriptions}, and meta keywords: {all_meta_keywords}."
    )
    messages = [
        {"role": "system", "content": "You are an AI trained in advanced SEO and content optimization."},
        {"role": "user", "content": prompt}
    ]
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4",  # Specify your desired model version here
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI for input fields
competitor_urls = st.text_input('Enter up to three competitor URLs separated by commas:')

if st.button('Analyze Competitors'):
    if competitor_urls:
        competitor_urls = [url.strip() for url in competitor_urls.split(',')]
        with st.spinner('Analyzing Competitors...'):
            competitor_data = [scrape_competitor_data(url) for url in competitor_urls]
            recommendations = generate_recommendations(competitor_data)
            st.subheader('Recommendations based on Competitor Analysis:')
            st.write(recommendations)
    else:
        st.warning('Please enter at least one competitor URL.')
