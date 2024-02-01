import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# Display the logo at the top of the app
logo_url = 'https://i.ibb.co/JHrXTjz/REPU-03.png'
st.image(logo_url, width=200)  # Adjust the width as needed

st.title('RepuSEO-Helper')

# Retrieve API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=openai_api_key)

google_api_key = 'your_google_api_key'  # Replace with your actual Google API key
google_cse_id = 'your_custom_search_engine_id'  # Replace with your actual Custom Search Engine ID

# ... [rest of your existing code for functions get_google_search_results, scrape_content, get_load_speed] ...

def get_recommendations(content, ranking, url, engine='gpt-3.5-turbo', purpose='general'):
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

# Streamlit UI
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
            if st.button('Refresh Meta'):
                with st.spinner('Refreshing meta description...'):
                    meta_description = get_recommendations(content, ranking, url, purpose='refresh_meta')
                    st.write('Refreshed Meta Description:')
                    st.write(meta_description)

        with col2:
            if st.button('Refresh Main Copy'):
                with st.spinner('Refreshing main copy...'):
                    main_copy_updates = get_recommendations(content, ranking, url, purpose='refresh_main_copy')
                    st.write('Refreshed Main Copy Updates:')
                    st.write(main_copy_updates)

        with col3:
            if st.button('Write Seeder Post'):
                with st.spinner('Generating seeder post...'):
                    seeder_post = get_recommendations(content, ranking, url, purpose='write_seeder_post')
                    st.write('Seeder Post (300 words):')
                    st.write(seeder_post)
    else:
        st.warning('Please enter a URL, a keyword, and a location.')
