import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import json
import os

# Streamlit app title and setup
st.image('https://i.ibb.co/VvYtGFg/REPU-11.png', width=200)
st.title('RepuSEO-Helper')

# Environment variables for API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
KEYWORDS_EVERYWHERE_API_KEY = os.getenv("KEYWORDS_EVERYWHERE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY

def scrape_content(url):
    """Scrapes the main content from a given URL."""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        content = soup.find('main').text if soup.find('main') else 'Main content not found'
        return content.strip()
    except Exception as e:
        return f"Error scraping content: {e}"

def get_google_search_results(query, site_url, location="CA"):
    """Fetches the site's ranking for a given keyword in Google search."""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'cx': GOOGLE_CSE_ID,
        'key': GOOGLE_API_KEY,
        'num': 10,
        'gl': location
    }
    try:
        response = requests.get(url, params=params).json()
        for index, item in enumerate(response.get("items", []), start=1):
            if site_url in item["link"]:
                return index
        return "Not found in top 10"
    except Exception as e:
        return f"Error fetching search results: {e}"
def generate_seo_recommendations(keyword, content):
    """Generate SEO recommendations using OpenAI's GPT model based on the site's content and target keyword."""
    try:
        prompt = f"Given the website content related to '{keyword}', provide SEO recommendations for improving search engine rankings."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error generating SEO recommendations: {e}"

def suggest_new_keywords(content):
    """Suggest new keywords based on the site's content using OpenAI's GPT model."""
    try:
        prompt = f"Based on the following content, suggest new keywords for SEO optimization: {content[:500]}..."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=60,
            n=5  # Adjust based on how many suggestions you want
        )
        keywords = [choice.text.strip() for choice in response.choices]
        return keywords
    except Exception as e:
        return f"Error suggesting new keywords: {e}"

def fetch_keyword_volumes(keywords):
    """Fetch search volumes for a list of keywords using the Keywords Everywhere API."""
    headers = {
        'Authorization': f'Bearer {KEYWORDS_EVERYWHERE_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'country': 'CA',
        'currency': 'USD',
        'dataSource': 'gkp',
        'kw[]': keywords
    }
    try:
        response = requests.post('https://api.keywordseverywhere.com/v1/get_keyword_data', headers=headers, json=data)
        if response.status_code == 200:
            return response.json().get('data', [])
        else:
            return f"Error fetching keyword volumes: Status code {response.status_code}"
    except Exception as e:
        return f"Error fetching keyword volumes: {e}"
# Streamlit UI components for input
url = st.text_input("Enter your URL:")
keyword = st.text_input("Enter your target keyword:")
location = st.text_input("Enter your location (e.g., 'CA' for Canada):", value='CA')

if st.button("Analyze SEO"):
    if url and keyword:
        content = scrape_content(url)
        ranking = get_google_search_results(keyword, url, location)
        recommendations = generate_seo_recommendations(keyword, content)

        st.subheader("SEO Ranking")
        st.write(f"Your site's ranking for '{keyword}': {ranking}")

        st.subheader("SEO Recommendations")
        st.write(recommendations)

        keywords = suggest_new_keywords(content)
        st.subheader("Suggested Keywords")
        st.write(", ".join(keywords))

        volumes = fetch_keyword_volumes(keywords)
        st.subheader("Keyword Search Volumes")
        for keyword_data in volumes:
            st.write(f"{keyword_data['keyword']}: {keyword_data['vol']} searches/month")
    else:
        st.error("Please enter both a URL and a target keyword.")
