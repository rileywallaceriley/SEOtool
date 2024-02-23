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

# Keywords Everywhere API Key
keywords_everywhere_api_key = os.getenv("KEYWORDS_EVERYWHERE_API_KEY")
if not keywords_everywhere_api_key:
    st.error("The KEYWORDS_EVERYWHERE_API_KEY environment variable is not set.")
    st.stop()

def get_recommendations(content, ranking, url, main_keyword, engine='gpt-4', purpose='general'):
    content_preview = (content[:500] + '...') if len(content) > 500 else content
    headings, meta_description = scrape_content(url)[1:]
    prompt = f"Analyze the provided content, headings, and meta description for the website {url} with SEO in mind. "\
             f"The site currently ranks {ranking} for the keyword '{main_keyword}'. "\
             f"Content (trimmed for brevity): {content_preview}\n"\
             f"Headings: {', '.join(headings)}\n"\
             f"Meta Description: {meta_description}\n\n"\
             "Provide a structured analysis with sections on:\n"\
             "What is currently working well for SEO and why.\n"\
             "What isn't working well for SEO and why.\n"\
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
        'country': 'CA',  # Adjust as needed
        'currency': 'CAD',  # Adjust as needed
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
            
            # After fetching the site ranking
            if ranking is not None:
                st.markdown(f'## Your site is ranked {ranking} for the keyword "{keyword}" in {location}.')
            else:
                st.write('Your site was not found in the top 50 results or an error occurred. Proceeding with recommendations...')
            
            # Proceed with SEO analysis and recommendations regardless of ranking
            content, headings, meta_description = scrape_content(url)
            seo_recommendations = get_recommendations(content, ranking if ranking is not None else "Not found", url, keyword)
            if seo_recommendations:
                st.markdown('## SEO Recommendations:')
                st.markdown(seo_recommendations)
            else:
                st.write("Unable to generate SEO recommendations.")

            # Suggest new keywords and fetch their volumes
            suggested_keywords = suggest_new_keywords(content, keyword)
            if suggested_keywords:
                keyword_volume_data = fetch_keyword_volumes(suggested_keywords)
                st.markdown('## Suggested Keywords and Their Search Volumes:')
                for data in keyword_volume_data:
                    st.markdown(f"### Keyword: {data['keyword']}, Volume: {data['vol']}, CPC: {data['cpc']['value']}, Competition: {data['competition']}")
            else:
                st.write("No new keyword suggestions were generated.")
    else:
        st.warning('Please enter a URL, a keyword, and a location.')
