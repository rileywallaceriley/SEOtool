import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from openai import OpenAI

# Display the logo and set up the app title
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)
st.title('Competitive Edge')

# Retrieve the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=openai_api_key)

def scrape_competitor_data(url):
    """Scrape content, meta title, meta description, and keywords from a URL."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        title_tag = soup.title.text if soup.title else 'Title not found'
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_description_content = meta_description['content'] if meta_description else 'No meta description provided'
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        meta_keywords_content = meta_keywords['content'] if meta_keywords else 'No keywords provided'
        
        content_sections = [soup.find(tag).text for tag in ['main', 'article', 'section'] if soup.find(tag)]
        main_content = ' '.join(content_sections).replace('\n', ' ') if content_sections else 'Main content not found'
        
        return {
            'url': url,
            'title': title_tag,
            'meta_description': meta_description_content,
            'meta_keywords': meta_keywords_content,
            'content': main_content
        }
    except Exception as e:
        st.error(f"Failed to scrape content from {url}: {str(e)}")
        return None

def generate_seo_analysis_and_recommendations(user_data, competitor_data):
    """Generate SEO analysis and recommendations using OpenAI."""
    analysis_prompt = "Analyze the SEO strategies based on the meta information and overall content provided below. Highlight effective strategies and offer detailed, actionable recommendations for improvement.\n\n"
    
    # Example structure for including user and competitor data in the prompt
    if user_data:
        analysis_prompt += f"User's Website Meta Title: {user_data['title']}\nUser's Meta Description: {user_data['meta_description']}\nUser's Meta Keywords: {user_data['meta_keywords']}\nUser's Main Content: {user_data['content'][:500]}\n\n"
    
    for data in competitor_data:
        if data:
            analysis_prompt += f"Competitor's URL: {data['url']}\nCompetitor's Meta Title: {data['title']}\nCompetitor's Meta Description: {data['meta_description']}\nCompetitor's Meta Keywords: {data['meta_keywords']}\nCompetitor's Main Content: {data['content'][:500]}\n\n"
    
    try:
        with st.spinner('Analyzing competitors...'):
            completion = client.chat.completions.create(
                model="gpt-4",
                prompt=analysis_prompt,
                temperature=0.5,
                max_tokens=1024,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            recommendations = completion.choices[0].text.strip()
            return recommendations
    except Exception as e:
        st.error(f"An error occurred while generating recommendations: {str(e)}")
        return "An error occurred while generating recommendations."

# Streamlit UI for input fields
user_url = st.text_input('Enter your website URL:')
competitor_urls_input = st.text_area('Enter competitor URLs (comma-separated):')

# Button to trigger analysis
if st.button('Analyze Competitors'):
    if competitor_urls_input:
        competitor_urls = [url.strip() for url in competitor_urls_input.split(',')]
        competitor_data = [scrape_competitor_data(url) for url in competitor_urls if url]
        user_data = scrape_competitor_data(user_url) if user_url else None
        
        if competitor_data:
            recommendations = generate_seo_analysis_and_recommendations(user_data, competitor_data)
            st.subheader('SEO Strategy Analysis and Recommendations')
            st.markdown(recommendations)
        else:
            st.warning('Failed to retrieve data for analysis.')
    else:
        st.warning('Please enter at least one competitor URL.')