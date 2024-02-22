import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from openai import OpenAI

# Display the logo and set up the Streamlit UI
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)
st.title('RepuSEO-Helper')

# Define your Google API key and CSE ID here
google_api_key = 'AIzaSyC0qDb3rdkRKxFrMaFyyDPMqBMYtOrrC4c'
google_cse_id = '34200d9d3c6084a1f'

# Retrieve API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=openai_api_key)

def get_google_search_results(query, site_url, location):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'cx': google_cse_id,
        'key': google_api_key,
        'num': 10,
        'gl': location
    }
    ranking = None
    for start_index in range(1, 51, 10):
        params['start'] = start_index
        response = requests.get(url, params=params)
        results = response.json()

        for i, item in enumerate(results.get('items', [])):
            if site_url in item.get('link'):
                ranking = i + 1 + start_index - 1
                return ranking
    return None

def scrape_content(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.find('main').text if soup.find('main') else 'Main content not found'
    headings = [h.text for h in soup.find_all(['h1', 'h2', 'h3'])]
    meta_description = soup.find('meta', attrs={'name': 'description'})
    meta_description_content = meta_description['content'] if meta_description else 'Meta description not found'
    return content, headings, meta_description_content

def get_recommendations(content, ranking, url, main_keyword, engine='gpt-4', purpose='general'):
    content_preview = (content[:500] + '...') if len(content) > 500 else content
    headings, meta_description = scrape_content(url)[1:]
    prompt = f"Analyze the provided content, headings, and meta description for the website {url} with SEO in mind. "\
             f"The site currently ranks {ranking} for the keyword '{main_keyword}'. "\
             f"Content (trimmed for brevity): {content_preview}\n"\
             f"Headings: {', '.join(headings)}\n"\
             f"Meta Description: {meta_description}\n\n"\
             "Provide a structured analysis with sections on:\n"\
             "1. What is currently working well for SEO and why.\n"\
             "2. What isn't working well for SEO and why.\n"\
             "3. Detailed and actionable recommendations for improving SEO ranking for '{main_keyword}'.\n"\
             "4. Keyword opportunities based on the analysis."

    try:
        response = client.chat.completions.create(
            model=engine,
            messages=[
                {"role": "system", "content": "You are an AI trained in advanced SEO and content optimization."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# UI for input fields
url = st.text_input('Enter your URL here:')
keyword = st.text_input('Enter your target keyword here:')
location = st.text_input('Enter your location (e.g., "New York, USA") here:')

if st.button('Analyze'):
    if url and keyword and location:
        with st.spinner('Analyzing...'):
            ranking = get_google_search_results(keyword, url, location)
            content, _, _ = scrape_content(url)  # Only content is needed here
            recommendations = get_recommendations(content, ranking, url, keyword)  # Pass keyword as main_keyword
            
            if ranking is not None and ranking <= 50:
                st.write(f'Your site is ranked {ranking} for the keyword "{keyword}".')
            else:
                st.write('Your site was not found in the top 50 results.')
            
            st.subheader('SEO Recommendations:')
            st.write(recommendations)
    else:
        st.warning('Please enter a URL, a keyword, and a location.')
