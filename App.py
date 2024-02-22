import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
from openai import OpenAI

# Display the logo at the top of the app
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)

st.title('RepuSEO-Helper')

# Retrieve API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=openai_api_key)

# Define your Google API key and CSE ID here
google_api_key = 'YOUR_GOOGLE_API_KEY'
google_cse_id = 'YOUR_GOOGLE_CSE_ID'

def get_google_search_results(query, site_url, location):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'cx': google_cse_id,
        'key': google_api_key,
        'num': 10,  # Number of results per page
        'gl': location  # Location parameter
    }
    ranking = None
    for start_index in range(1, 51, 10):  # Look through the first 50 results
        params['start'] = start_index
        response = requests.get(url, params=params)
        results = response.json()

        for i, item in enumerate(results.get('items', [])):
            if site_url in item.get('link'):
                ranking = i + 1 + start_index - 1  # Adjusting ranking based on the page
                return ranking
    return None

def scrape_content(url):
    # Ensure the URL starts with http:// or https://
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.find('main').text if soup.find('main') else 'Main content not found'
    return content
# Continuing from the previous part...

KEYWORDS_EVERYWHERE_API_KEY = os.getenv("KEYWORDS_EVERYWHERE_API_KEY")
if not KEYWORDS_EVERYWHERE_API_KEY:
    raise ValueError("The KEYWORDS_EVERYWHERE_API_KEY environment variable is not set.")

def suggest_new_keywords(content, keyword):
    prompt = f"Based on the content related to '{keyword}', suggest additional keywords that could help improve SEO and drive traffic."
    try:
        completion = client.completions.create(prompt=prompt, max_tokens=60, n=5, stop=["\n"])
        keywords = [choice['text'].strip() for choice in completion.choices]
        return keywords
    except Exception as e:
        return f"An error occurred while generating keyword suggestions: {str(e)}"

def fetch_keyword_volumes(keywords):
    url = "https://api.keywordseverywhere.com/v1/get_keyword_data"
    headers = {'Authorization': f'Bearer {KEYWORDS_EVERYWHERE_API_KEY}'}
    payload = {
        'country': 'CA',
        'currency': 'CAD',
        'dataSource': 'gkp',
        'kw[]': keywords
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        st.error("Failed to fetch keyword volume data.")
        return []

# Streamlit UI for input fields and functionality integration
url = st.text_input('Enter your URL here:')
keyword = st.text_input('Enter your target keyword here:')
location = st.text_input('Enter your location (e.g., "Toronto, Canada") here:')

if st.button('Analyze'):
    if url and keyword and location:
        with st.spinner('Analyzing...'):
            ranking = get_google_search_results(keyword, url, location)
            content = scrape_content(url)
            
            if ranking is not None:
                st.write(f'Your site is ranked {ranking} for the keyword "{keyword}" in {location}.')
                suggested_keywords = suggest_new_keywords(content, keyword)
                if suggested_keywords:
                    keyword_volume_data = fetch_keyword_volumes(suggested_keywords)
                    st.subheader('Suggested Keywords and Their Search Volumes:')
                    for data in keyword_volume_data:
                        st.write(f"Keyword: {data['keyword']}, Volume: {data['vol']}, CPC: {data['cpc']['value']}, Competition: {data['competition']}")
                else:
                    st.write("No new keyword suggestions were generated.")
            else:
                st.write('Your site was not found in the top 50 results.')
    else:
        st.warning('Please enter a URL, a keyword, and a location.')
