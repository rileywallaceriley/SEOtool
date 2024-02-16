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
    # You should integrate with an API or library to get keyword suggestions and competition data
    # Example:
    # keyword_suggestions = get_keyword_suggestions(content)
    # keyword_competition = get_keyword_competition(keyword)

    # Temporary code to avoid the error, remove or replace with actual logic
    keyword_suggestions = ['suggestion1', 'suggestion2']  # Replace with actual logic
    keyword_competition = {'suggestion1': 'low', 'suggestion2': 'high'}  # Replace with actual logic

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

if st.button('Analyze'):
    if url and keyword and location:
        with st.spinner('Analyzing...'):
            # Existing analyze functionality
            ranking = get_google_search_results(keyword, url, location)
            content = scrape_content(url)
            recommendations = get_recommendations(content, ranking, url)
            
            if ranking is not None and ranking <= 50:
                st.write(f'Your site is ranked {ranking} for the keyword "{keyword}".')
            else:
                st.write('Your site was not found in the top 50 results.')
            
            st.subheader('SEO Recommendations:')
            st.write(recommendations)

        # Define a function to display each tool section with centered title and description
        def display_tool_section(header, description, button_label, button_url):
            with st.container():
                # Use HTML to center the header and description
                st.markdown(f"<h3 style='text-align: center;'>{header}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center;'>{description}</p>", unsafe_allow_html=True)
                
                # Centered button with HTML
                button_html = f"""<div style="text-align: center;"><a href="{button_url}" target="_blank"><button style='margin-top: 10px; width: auto; padding: 10px 20px; border-radius: 5px; border: none; color: black; background-color: #f4a261;'>{button_label}</button></a></div>"""
                st.markdown(button_html, unsafe_allow_html=True)
                
                # Divider
                st.markdown("---")

        # Display the additional SEO tools and resources immediately after defining the function
        st.markdown("---")
        tools = [
            # Tool descriptions as provided
        ]

        # Displaying the tool sections
        for tool in tools:
            display_tool_section(tool['header'], tool['description'], tool['button_label'], tool['button_url'])

        # Responsive image display at the bottom
        left_column, image_column, right_column = st.columns([1, 10, 1])
        with image_column:
            st.image("https://i.ibb.co/pxcB74N/Analysis.png", use_column_width=True)
    else:
        st.warning('Please enter a URL, a keyword, and a location.')
