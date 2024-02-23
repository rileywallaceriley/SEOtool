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
google_api_key = 'YOUR_GOOGLE_API_KEY'  # Use your actual API key
google_cse_id = 'YOUR_GOOGLE_CSE_ID'  # Use your actual CSE ID

# Retrieve API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("The OPENAI_API_KEY environment variable is not set.")
    st.stop()

# Create an OpenAI client instance
openai_client = OpenAI(api_key=openai_api_key)

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
             "What is currently working well for SEO and why. [Try to sum up and explain what you feel their strategy currently is, and try to be complimentary where possible.] \n"\
             "What isn't working well for SEO and why. [This section should be as detailed as possible, citing specific example thing the page to ensure eteh reader fully grasps what is holding them back.] \n"\
             "Detailed and actionable recommendations for improving SEO ranking for '{main_keyword}'. [this section should provide specific examples, whether that means pointing out specific places in the copy to insert keywords, or provide examples of rewritten header. Assume the reader isn't knowledgeable and provide a detailed explanation that shys away from simply giving jargon and demonstrates exactly what to change and adjust with direct examples using the actual copy from the website content provided.]\n"\
             "Keyword opportunities based on the analysis. [in this section provide a brief intro, and break down the suggestion, providing some context and logixc as to why you're suggesting it]"

    try:
        response = openai_client.chat.completions.create(
            model=engine,
            messages=[
                {"role": "system", "content": "You are an AI trained in advanced SEO and content optimization."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI for input fields and functionality integration
url = st.text_input('Enter your URL here:')
keyword = st.text_input('Enter your target keyword here:')
location = st.text_input('Enter your location (e.g., "Toronto, Canada") here:')

if st.button('Analyze'):
    if url and keyword and location:
        with st.spinner('Analyzing...'):
            # Assuming variables and logic for ranking and content fetching are defined above
            ranking = get_google_search_results(keyword, url, location)
            content, _, _ = scrape_content(url)
            seo_recommendations = get_recommendations(content, ranking if ranking is not None else "Not found", url, keyword)
            
            if seo_recommendations:
                st.markdown('## SEO Recommendations:')
                st.markdown(seo_recommendations)

  # Divider
        st.markdown("---")
                
                # Define a function to display each tool section with centered title and description
                def display_tool_section(header, description, button_label, button_url):
                    with st.container():
                        st.markdown(f"<h3 style='text-align: center;'>{header}</h3>", unsafe_allow_html=True)
                        st.markdown(f"<p style='text-align: center;'>{description}</p>", unsafe_allow_html=True)
                        button_html = f"""<div style="text-align: center;"><a href="{button_url}" target="_blank"><button style='margin-top: 10px; width: auto; padding: 10px 20px; border-radius: 5px; border: none; color: black; background-color: #f4a261;'>{button_label}</button></a></div>"""
                        st.markdown(button_html, unsafe_allow_html=True)
                        st.markdown("---")

               # Tool descriptions and display logic
                tools = [
                   {
        "header": "Competitive Edge",
        "description": "Analyze and apply winning SEO strategies from your competitors directly into your campaign.",
        "button_label": "Use Now - Competitive Edge",
        "button_url": "https://seotool-mfvdnqmf32f3visjegsxho.streamlit.app"
    },
    {
        "header": "Blog SEO Helper",
        "description": "Elevate your blog's visibility with targeted SEO strategies designed for maximum engagement.",
        "button_label": "Use Now - Blog SEO Helper",
        "button_url": "https://seotool-7uqzcambnfjnuuwh9pctlr.streamlit.app"
    },
                ]

                for tool in tools:
                    display_tool_section(tool['header'], tool['description'], tool['button_label'], tool['button_url'])

                # Adjusting columns for responsive image display at the bottom
                left_column, image_column, right_column = st.columns([1, 10, 1])
                with image_column:
                    st.image("https://i.ibb.co/pxcB74N/Analysis.png", use_column_width=True)
    else:
        st.warning('Please enter a URL, a keyword, and a location.')
