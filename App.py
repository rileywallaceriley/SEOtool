import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
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
    
def generate_meta_content(content, keyword):
    # Use OpenAI's GPT model to generate meta content
    prompt = f"Write a compelling meta description for a webpage about '{keyword}', using the following content: {content}."
    try:
        completion = client.completions.create(prompt=prompt, max_tokens=60)
        return completion.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

def generate_pillar_content(content, keyword, url):
    # Use OpenAI's GPT model to generate a blog post
    prompt = f"Write a 250-word blog post optimized for SEO about '{keyword}', using the following context: {content}. Include a link to {url}."
    try:
        completion = client.completions.create(prompt=prompt, max_tokens=300)
        return completion.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

def analyze_keywords(content, keyword):
    # Placeholder for keyword analysis functionality
    # This function should integrate with an API or library to get keyword suggestions and competition data
    # Example:
    # keyword_suggestions = get_keyword_suggestions(content)
    # keyword_competition = get_keyword_competition(keyword)
    # ...
    return keyword_suggestions, keyword_competition

def get_recommendations(content, ranking, url, engine='gpt-4', purpose='general'):
    content_preview = (content[:500] + '...') if len(content) > 500 else content
    
    # Modify the prompt based on the purpose
    if purpose == 'refresh_meta':
        prompt = f"Generate an SEO-rich meta description for the following content: {content_preview}"
    elif purpose == 'refresh_main_copy':
        prompt = f"Provide SEO touch copy updates for the following content: {content_preview}"
    elif purpose == 'write_seeder_post':
        prompt = f"Compose a 300-word SEO-rich blog post meant to seed (link) into the page with the following content: {content_preview}"
    else:
        prompt = (
            f"Website URL: {url}\n"
            f"Content Preview (first 500 characters): {content_preview}\n"
            f"Current SEO Ranking: {ranking}\n\n"
            "Provide specific and actionable SEO recommendations based on the content preview and current SEO ranking. "
            "Avoid general concepts and provide direct recommendations on how to update the main copy, meta tags, and any other on-page elements to improve SEO performance, for example, show the current copy and explain exactly where to make changes. "
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
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"
        

# Streamlit UI for input fields
url = st.text_input('Enter your URL here:')
keyword = st.text_input('Enter your target keyword here:')
location = st.text_input('Enter your location (e.g., "New York, USA") here:')

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button('Analyze'):
        if url and keyword and location:
            with st.spinner('Analyzing...'):
                # Existing analyze functionality
                ranking = get_google_search_results(keyword, url, location)
                content = scrape_content(url)
                load_speed_score = get_load_speed(url)
                recommendations = get_recommendations(content, ranking, url)
                
                if ranking is not None and ranking <= 50:
                    st.write(f'Your site is ranked {ranking} for the keyword "{keyword}".')
                else:
                    st.write('Your site was not found in the top 50 results.')
                
                st.subheader('SEO Recommendations:')
                st.write(recommendations)
                
                st.subheader('Page Load Speed Score:')
                st.write(f'Load Speed Score (out of 100): {load_speed_score}')
        else:
            st.warning('Please enter a URL, a keyword, and a location.')

with col2:
    if st.button('Keywords'):
        if url and keyword:
            with st.spinner('Analyzing Keywords...'):
                content = scrape_content(url)
                keyword_suggestions, keyword_competition = analyze_keywords(content, keyword)
                st.write('Keyword Suggestions:', keyword_suggestions)
                st.write('Keyword Competition Data:', keyword_competition)
        else:
            st.warning('Please enter a URL and a keyword.')

with col3:
    if st.button('Pillar'):
        if url and keyword:
            with st.spinner('Generating Pillar Page Content...'):
                content = scrape_content(url)
                pillar_content = generate_pillar_content(content, keyword, url)
                st.text_area('Pillar Page Content:', pillar_content)
        else:
            st.warning('Please enter a URL and a keyword.')

with col4:
    if st.button('Meta'):
        if url and keyword:
            with st.spinner('Generating Meta Content...'):
                content = scrape_content(url)
                meta_content = generate_meta_content(content, keyword)
                st.text_area('Meta Description:', meta_content)
        else:
            st.warning('Please enter a URL and a keyword.')