import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
import openai

# Ensure you have the latest version of the OpenAI library
# pip install --upgrade openai

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("The OPENAI_API_KEY environment variable is not set.")
    st.stop()
openai.api_key = openai_api_key

st.image('https://i.ibb.co/VvYtGFg/REPU-11.png', width=200)
st.title('Competitive Edge')

def scrape_competitor_data(url):
    """Scrape the title and meta description from a given URL."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.text if soup.title else 'No title found'
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_description_content = meta_description['content'] if meta_description else 'No meta description provided'
        return {'url': url, 'title': title, 'meta_description': meta_description_content}
    except Exception as e:
        return {'url': url, 'error': str(e)}

def generate_seo_recommendations(content, url, engine='gpt-4'):
    """Generate SEO recommendations using GPT-4 based on provided content and URL."""
    prompt = f"Based on the following content from {url}, provide detailed SEO recommendations:\nContent: {content[:500]}..."
    try:
        with st.spinner('Generating SEO recommendations...'):
            response = openai.Completion.create(
                model=engine,
                prompt=prompt,
                temperature=0.7,
                max_tokens=1024,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred while generating recommendations: {str(e)}"

user_url = st.text_input('Enter your website URL:')
competitor_urls_input = st.text_area('Enter competitor URLs (comma-separated):')

if st.button('Analyze Competitors'):
    if not competitor_urls_input:
        st.warning('Please enter at least one competitor URL.')
    else:
        competitor_urls = [url.strip() for url in competitor_urls_input.split(',')]
        analysis_results = []
        for url in competitor_urls:
            data = scrape_competitor_data(url)
            if 'error' not in data:
                recommendations = generate_seo_recommendations(data['meta_description'], data['url'], engine='gpt-4')
                analysis_results.append((data['url'], recommendations))
            else:
                analysis_results.append((url, "Failed to analyze this URL."))

        for url, recommendations in analysis_results:
            st.subheader(f"SEO Recommendations for {url}:")
            st.write(recommendations)