import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

# Set your API keys here
openai.api_key = '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'
google_api_key = 'AIzaSyC0qDb3rdkRKxFrMaFyyDPMqBMYtOrrC4c'
google_cse_id = '34200d9d3c6084a1f'

def get_google_search_results(query, site_url):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'cx': google_cse_id,
        'key': google_api_key
    }
    response = requests.get(url, params=params)
    results = response.json()
    
    for i, item in enumerate(results.get('items', [])):
        if i >= 50:  # Cap the ranking at 50
            break
        if site_url in item.get('link'):
            return i + 1
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
            engine=engine,
            prompt=prompt,
            max_tokens=500  # Increased max_tokens for more detailed recommendations
        )
        return response.choices[0].text.strip()
    except Exception as e:  # Catching a general exception
        return f"An error occurred: {str(e)}"

# Streamlit UI
st.title('SEO Analysis Tool')

url = st.text_input('Enter your URL here:')
keyword = st.text_input('Enter your target keyword here:')

if st.button('Analyze'):
    if url and keyword:
        ranking = get_google_search_results(keyword, url)
        content = scrape_content(url)
        recommendations = get_recommendations(content, ranking, url, engine='text-davinci-004')
        
        if ranking is not None and ranking <= 50:
            st.write(f'Your site is ranked {ranking} for the keyword "{keyword}".')
        elif ranking is None:
            st.write('Your site was not found in the top 50 results.')
        
        st.subheader('Content Scraped:')
        st.write(content)  # Display a portion of the scraped content
        st.subheader('SEO Recommendations:')
        st.write(recommendations)
    else:
        st.warning('Please enter both a URL and a keyword.')
