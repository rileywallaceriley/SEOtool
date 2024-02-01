import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# Retrieve API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=openai_api_key)

google_api_key = 'AIzaSyC0qDb3rdkRKxFrMaFyyDPMqBMYtOrrC4c'
google_cse_id = '34200d9d3c6084a1f'

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

def get_load_speed(url):
    pagespeed_url = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={google_api_key}'
    response = requests.get(pagespeed_url)
    result = response.json()
    
    # Parse the result as needed, for example:
    speed_score = result.get('lighthouseResult', {}).get('categories', {}).get('performance', {}).get('score')
    if speed_score:
        speed_score = speed_score * 100  # Convert to percentage
    else:
        speed_score = 'Load speed score not available'
    return speed_score

def get_recommendations(content, ranking, url, engine='gpt-3.5-turbo'):
    content_preview = (content[:500] + '...') if len(content) > 500 else content
    prompt = (
        f"Website URL: {url}\n"
        f"Content Preview (first 500 characters): {content_preview}\n"
        f"Current SEO Ranking: {ranking}\n\n"
        "Provide specific and actionable SEO recommendations based on the content preview and current SEO ranking. "
        "Avoid general concepts and provide direct recommendations on how to update the main copy, meta tags, and any other on-page elements to improve SEO performance. "
        "Also, include page speed recommendations if appropriate.\n\n"
        "Note: The main keyword should be strategically included in the content, but avoid recommendations that merely state to include the main keyword."
    )
    
    messages = [
        {"role": "system", "content": "You are an AI trained in advanced SEO and content optimization."},
        {"role": "user", "content": prompt}
    ]
    
    try:
        completion = client.chat.completions.create(
            model=engine,
            messages=messages
        )
        return completion['choices'][0]['message']['content']
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI
st.title('SEO Analysis Tool')

url = st.text_input('Enter your URL here:')
keyword = st.text_input('Enter your target keyword here:')
location = st.text_input('Enter your location (e.g., "New York, USA") here:')

if st.button('Analyze'):
    if url and keyword and location:
        ranking = get_google_search_results(keyword, url, location)
        content = scrape_content(url)
        load_speed_score = get_load_speed(url)
        recommendations = get_recommendations(content, ranking, url)
        
        if ranking is not None and ranking <= 50:
            st.write(f'Your site is ranked {ranking} for the keyword "{keyword}".')
        elif ranking is None:
            st.write('Your site was not found in the top 50 results.')
        
        # Display the SEO recommendations
        st.subheader('SEO Recommendations:')
        st.write(recommend
