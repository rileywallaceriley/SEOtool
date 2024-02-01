import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

# Set your API keys here (preferably as environment variables)
openai.api_key = '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'
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
    content = soup.find('main').text
    return content

def get_recommendations(content, ranking, url, engine='text-davinci-004'):
    content_preview = (content[:500] + '...') if len(content) > 500 else content
    prompt = (
        f"Website URL: {url}\n"
        f"Content Preview (first 500 characters): {content_preview}\n\n"
        "Provide a detailed on-page SEO analysis with specific tasks for improvement. Analyze aspects such as:\n"
        "- Use of keywords in titles (H1, H2 tags) and meta descriptions.\n"
        "- Content relevance and quality.\n"
        "- Presence of internal and external links.\n"
        "- URL structure and user-friendliness.\n"
        "- Mobile-friendliness and loading speed.\n"
    )

    if ranking is not None and ranking <= 50:
        prompt += f"\nThe site is currently ranked {ranking} for the given keyword. Include additional strategic advice on how to further improve the ranking, considering both on-page and off-page SEO factors."
    else:
        prompt += "\nThe site is not in the top 50. Focus on crucial improvements that can significantly impact the site's SEO performance."

    try:
        response = openai.Completion.create(
            model=engine,
            prompt=prompt,
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:  # Catching a general exception
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
        recommendations = get_recommendations(content, ranking, url, engine='text-davinci-003')
        
        if ranking is not None and ranking <= 50:
            st.write(f'Your site is ranked {ranking} for the keyword "{keyword}".')
        elif ranking is None:
            st.write('Your site was not found in the top 50 results.')
        
        # Display the SEO recommendations
        st.subheader('SEO Recommendations:')
        st.write(recommendations)
    else:
        st.warning('Please enter a URL, a keyword, and a location.')
