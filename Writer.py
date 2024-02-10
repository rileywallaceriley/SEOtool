import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# Display the logo at the top of the app
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)  # Adjust the width as needed

st.title('Blog Writer')

# Initialize session states for button presses
if 'meta_pressed' not in st.session_state:
    st.session_state['meta_pressed'] = False
if 'main_copy_pressed' not in st.session_state:
    st.session_state['main_copy_pressed'] = False
if 'seeder_pressed' not in st.session_state:
    st.session_state['seeder_pressed'] = False

# Retrieve API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=openai_api_key)

google_api_key = 'AIzaSyC0qDb3rdkRKxFrMaFyyDPMqBMYtOrrC4c'
google_cse_id = '34200d9d3c6084a1f'

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
            "Create a 350 word blog post. "
            "Use the keywords as overarching topics to create the blog post. use seo rich H2 and H3 tags to organize the content"
            "Note: The main keyword should be strategically included in the content"
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

if st.button('Analyze'):
    if url and keyword and location:
        with st.spinner('Analyzing...'):
            ranking = get_google_search_results(keyword, url, location)
            content = scrape_content(url)
            load_speed_score = get_load_speed(url)
            recommendations = get_recommendations(content, ranking, url)
        
        if ranking is not None and ranking <= 50:
            st.write(f'Your site is ranked {ranking} for the keyword "{keyword}".')
        elif ranking is None:
            st.write('Your site was not found in the top 50 results.')
        
        # Display the SEO recommendations and load speed
        st.subheader('SEO Recommendations:')
        st.write(recommendations)
        
        st.subheader('Page Load Speed Score:')
        st.write(f'Load Speed Score (out of 100): {load_speed_score}')
        
        # Action buttons for further SEO enhancements
        col1, col2, col3 = st.columns(3)
        with col1:
            if not st.session_state['meta_pressed']:
                if st.button('Refresh Meta'):
                    st.session_state['meta_pressed'] = True
                    with st.spinner('Refreshing meta description...'):
                        meta_description = get_recommendations(content, ranking, url, purpose='refresh_meta')
                        st.write('Refreshed Meta Description:')
                        st.write(meta_description)

        with col2:
            if not st.session_state['main_copy_pressed']:
                if st.button('Refresh Main Copy'):
                    st.session_state['main_copy_pressed'] = True
                    with st.spinner('Refreshing main copy...'):
                        main_copy_updates = get_recommendations(content, ranking, url, purpose='refresh_main_copy')
                        st.write('Refreshed Main Copy Updates:')
                        st.write(main_copy_updates)

        with col3:
            if not st.session_state['seeder_pressed']:
                if st.button('Write Seeder Post'):
                    st.session_state['seeder_pressed'] = True
                    with st.spinner('Generating seeder post...'):
                        seeder_post = get_recommendations(content, ranking, url, purpose='write_seeder_post')
                        st.write('Seeder Post (300 words):')
                        st.write(seeder_post)
    else:
        st.warning('Please enter a URL, a keyword, and a location.')
