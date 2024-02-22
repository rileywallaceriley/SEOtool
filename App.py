import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from openai import OpenAI

# Streamlit app title
st.image('https://i.ibb.co/VvYtGFg/REPU-11.png', width=200)
st.title('RepuSEO-Helper')

# Retrieve API keys from Streamlit secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
GOOGLE_CSE_ID = st.secrets["GOOGLE_CSE_ID"]

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def scrape_content(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    main_content = soup.find('main').text.strip() if soup.find('main') else 'Main content not found.'
    headings = [heading.text.strip() for heading in soup.find_all(['h1', 'h2', 'h3'])]
    meta_description = soup.find('meta', attrs={'name': 'description'})
    meta_description_content = meta_description['content'].strip() if meta_description else 'Meta description not found.'
    return main_content, headings, meta_description_content

def get_google_search_results(query, site_url, location):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'cx': GOOGLE_CSE_ID,
        'key': GOOGLE_API_KEY,
        'num': 10,
        'gl': location
    }
    for start_index in range(1, 51, 10):
        params['start'] = start_index
        response = requests.get(url, params=params)
        results = response.json()
        for i, item in enumerate(results.get('items', [])):
            if site_url in item.get('link'):
                return i + 1 + start_index - 1
    return "Not found within the top 50 results."

def get_recommendations(content, ranking, url, main_keyword, engine='gpt-4'):
    prompt = f"""
    Analyze the provided content, headings, and meta description for the website {url} with SEO in mind. 
    The site currently ranks {ranking} for the keyword '{main_keyword}'.
    Content (trimmed for brevity): {content[:500]}...
    Headings: {", ".join(headings)}
    Meta Description: {meta_description}

    Provide a structured analysis with sections on:
    1. What is currently working well for SEO and why.
    2. What isn't working well for SEO and why.
    3. Detailed and actionable recommendations for improving SEO ranking for '{main_keyword}'.
    4. Keyword opportunities based on the analysis.
    """
    response = client.completions.create(
        model=engine,
        prompt=prompt,
        temperature=0.5,
        max_tokens=2048,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()

# Streamlit UI for input fields
url = st.text_input('Enter your URL here:')
keyword = st.text_input('Enter your target keyword here:')
location = st.text_input('Enter your location (e.g., "New York, USA") here:')

if st.button('Analyze') and url and keyword and location:
    with st.spinner('Analyzing...'):
        ranking = get_google_search_results(keyword, url, location)
        content, headings, meta_description = scrape_content(url)
        analysis_and_recommendations = get_recommendations(content, ranking, url, keyword)
        
        # Display analysis and recommendations
        st.markdown(f'## SEO Analysis and Recommendations for {url}')
        st.write(analysis_and_recommendations)
