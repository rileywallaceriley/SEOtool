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
    # Continue from the previous part...

# Keywords Everywhere API Key
keywords_everywhere_api_key = os.getenv("KEYWORDS_EVERYWHERE_API_KEY")
if not keywords_everywhere_api_key:
    st.error("The KEYWORDS_EVERYWHERE_API_KEY environment variable is not set.")
    st.stop()

def get_enhanced_recommendations(content, ranking, url, main_keyword, keyword_volume_data, engine='gpt-4'):
    # Prepare the content preview and SEO data
    content_preview = (content[:500] + '...') if len(content) > 500 else content
    headings, meta_description = scrape_content(url)[1:]
    
    # Prepare keyword insights
    keyword_insights = ". ".join([f"The keyword '{data['keyword']}' has a search volume of {data['vol']}, a CPC of {data['cpc']['value']}, and a competition level of {data['competition']}" for data in keyword_volume_data])
    
    # Generate the prompt with more specific instructions for actionable advice and examples
    prompt = f"Analyze the provided content, headings, meta description, and keyword insights for the website {url} with SEO in mind. The site currently ranks {ranking} for the keyword '{main_keyword}'. Content (trimmed for brevity): {content_preview}. Headings: {', '.join(headings)}. Meta Description: {meta_description}. Keyword Insights: {keyword_insights}. Provide a structured analysis with sections on: 1. What is currently working well for SEO and why. 2. What isn't working well for SEO and why. 3. Detailed and actionable recommendations for improving SEO ranking for '{main_keyword}', including specific examples of better copy. 4. Keyword opportunities based on the analysis."

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

def suggest_new_keywords(content, keyword):
    prompt = f"Based on the content related to '{keyword}', suggest additional keywords that could help improve SEO and drive traffic."
    try:
        completion = openai_client.completions.create(prompt=prompt, max_tokens=60, n=5, stop=["\n"])
        keywords = [choice['text'].strip() for choice in completion.choices]
        return keywords
    except Exception as e:
        return f"An error occurred while generating keyword suggestions: {str(e)}"

def fetch_keyword_volumes(keywords):
    url = "https://api.keywordseverywhere.com/v1/get_keyword_data"
    headers = {'Authorization': f'Bearer {keywords_everywhere_api_key}'}
    payload = {
        'country': 'US',  # Adjust as needed
        'currency': 'USD',  # Adjust as needed
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
            content, _, _ = scrape_content(url)
            
            if ranking is not None:
                st.markdown(f'## Your site is ranked {ranking} for the keyword "{keyword}" in {location}.')
                # Fetch keyword volumes
                suggested_keywords = suggest_new_keywords(content, keyword)
                if suggested_keywords:
                    keyword_volume_data = fetch_keyword_volumes(suggested_keywords)
                    # Generate enhanced recommendations
                    recommendations = get_enhanced_recommendations(content, ranking, url, keyword, keyword_volume_data)
                    st.markdown('## SEO Recommendations:')
                    st.markdown(recommendations)
                else:
                    st.write("No new keyword suggestions were generated.")
            else:
                st.write('Your site was not found in the top 50 results.')
    else:
        st.warning('Please enter a URL, a keyword, and a location.')
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

        # Tool descriptions
        st.markdown("---")
        tools = [
            {
                "header": "RepuSEO-Helper",
                "description": "Receive personalized SEO recommendations to improve your site's ranking and user experience.",
                "button_label": "Use Now - RepuSEO-Helper",
                "button_url": "https://seotool-qpb8fq8bygcusdsxn6pm6s.streamlit.app"
            },
            {
                "header": "Blog SEO Helper",
                "description": "Elevate your blog's visibility with targeted SEO strategies designed for maximum engagement.",
                "button_label": "Use Now - Blog SEO Helper",
                "button_url": "https://seotool-7uqzcambnfjnuuwh9pctlr.streamlit.app"
            },
            {
                "header": "RepuSEO Plagiarism Checker",
                "description": "Ensure the originality of your content with our advanced plagiarism detection tool.",
                "button_label": "Use Now - RepuSEO Plagiarism Checker",
                "button_url": "https://seotool-cdjzyqj4qrskqvkuahwjwm.streamlit.app"
            },
        ]

        # Displaying the tool sections
        for tool in tools:
            display_tool_section(tool['header'], tool['description'], tool['button_label'], tool['button_url'])

    # Adjusting columns for responsive image display at the bottom
    left_column, image_column, right_column = st.columns([1, 10, 1])
    with image_column:
        st.image("https://i.ibb.co/pxcB74N/Analysis.png", use_column_width=True)
