import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from openai import OpenAI

# Initialize the OpenAI client with your API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("The OPENAI_API_KEY environment variable is not set.")
    st.stop()
client = OpenAI(api_key=openai_api_key)

# Display the logo and app title at the top of the UI
st.image('https://i.ibb.co/VvYtGFg/REPU-11.png', width=200)
st.title('Competitive Edge')

def scrape_competitor_data(url):
    """Scrape the title and meta description from a given URL."""
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return {'url': url, 'error': 'Failed to fetch content'}
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.text if soup.title else 'No title found'
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_description_content = meta_description['content'] if meta_description else 'No meta description provided'
        return {
            'url': url,
            'title': title,
            'meta_description': meta_description_content,
        }
    except Exception as e:
        return {'url': url, 'error': str(e)}

def generate_seo_recommendations(engine='gpt-4', prompt='Analyze the following SEO strategy:'):
    """Generate SEO recommendations using GPT-4 based on a given prompt."""
    try:
        with st.spinner('Generating SEO recommendations...'):
            response = client.completions.create(
                model=engine,
                prompt=prompt,
                temperature=0.5,
                max_tokens=1024,
            )
            return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred while generating recommendations: {str(e)}"

# Streamlit UI for collecting user and competitor URLs
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
                prompt = f"URL: {data['url']}\nTitle: {data['title']}\nMeta Description: {data['meta_description']}\n\nProvide SEO recommendations:"
                recommendations = generate_seo_recommendations(prompt=prompt)
                analysis_results.append((data['url'], recommendations))
            else:
                analysis_results.append((url, "Failed to analyze this URL."))

        for url, recommendations in analysis_results:
            st.subheader(f"SEO Recommendations for {url}:")
            st.write(recommendations)