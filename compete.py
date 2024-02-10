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
    # Scrape logic as previously defined, unchanged

def generate_seo_recommendations(content, ranking, url, engine='gpt-4', purpose='seo-analysis'):
    """
    Generates SEO recommendations using GPT-4 based on provided content, its ranking, and the URL.
    """
    content_preview = (content[:500] + '...') if len(content) > 500 else content
    prompt = f"Analyze the SEO strategy based on the content: '{content_preview}' from the URL: {url}. Provide detailed, actionable SEO recommendations:"

    try:
        with st.spinner('Generating SEO recommendations...'):
            completion = client.completions.create(
                model=engine,
                prompt=prompt,
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

# UI for input fields
user_url = st.text_input('Enter your website URL:')
competitor_urls_input = st.text_area('Enter competitor URLs (comma-separated):')

# Button to trigger analysis
if st.button('Analyze Competitors'):
    if competitor_urls_input:
        competitor_urls = [url.strip() for url in competitor_urls_input.split(',')]
        competitor_data = [scrape_competitor_data(url) for url in competitor_urls if url]
        user_data = scrape_competitor_data(user_url) if user_url else None
        
        # Example of using the generate_seo_recommendations function
        # Here, you would loop through competitor_data (and possibly include user_data)
        # to generate recommendations for each. Simplified for demonstration:
        if competitor_data:
            for data in competitor_data:
                if data:
                    recommendations = generate_seo_recommendations(data['content'], "example ranking", data['url'])
                    st.subheader(f"SEO Recommendations for {data['url']}:")
                    st.write(recommendations)
        if user_data:
            user_recommendations = generate_seo_recommendations(user_data['content'], "your site ranking", user_url, purpose='seo-improvement')
            st.subheader("Your Website's SEO Recommendations:")
            st.write(user_recommendations)
    else:
        st.warning('Please enter at least one competitor URL.')