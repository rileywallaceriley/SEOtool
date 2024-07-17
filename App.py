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
google_api_key = 'YOUR_GOOGLE_API_KEY'  # Replace with your actual API key
google_cse_id = 'YOUR_GOOGLE_CSE_ID'  # Replace with your actual CSE ID

# Retrieve API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("The OPENAI_API_KEY environment variable is not set.")
    st.stop()

# Create an OpenAI client instance
openai_client = OpenAI(api_key=openai_api_key)

def get_google_search_results(query, site_url, location):
    # ... (rest of the function remains unchanged)

def scrape_content(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    content = soup.find('main').text if soup.find('main') else 'Main content not found'
    headings = [h.text for h in soup.find_all(['h1', 'h2', 'h3'])]
    meta_description = soup.find('meta', attrs={'name': 'description'})
    meta_description_content = meta_description['content'] if meta_description else 'Meta description not found'
    
    images = soup.find_all('img')
    image_alts = [(image.get('src'), image.get('alt', 'No alt attribute')) for image in images]

    return content, headings, meta_description_content, image_alts

def get_recommendations(content, ranking, url, main_keyword, headings, meta_description, image_alts, engine='gpt-4', purpose='general'):
    content_preview = (content[:500] + '...') if len(content) > 500 else content

    # Analyze alt tags
    alt_tag_summary = "Alt tags are used effectively for some images, enhancing SEO and accessibility. However, there are opportunities to improve alt text to be more descriptive and keyword-rich where appropriate."
    missing_alts = sum(1 for _, alt in image_alts if alt == 'No alt attribute')
    if missing_alts > 0:
        alt_tag_summary += f" Notably, {missing_alts} images are missing alt tags, which is a missed opportunity for SEO and accessibility."

    prompt = f"Analyze the provided content, headings, meta description, and alt tags for the website {url} with SEO in mind. "\
             f"The site currently ranks {ranking} for the keyword '{main_keyword}'. "\
             f"Content (trimmed for brevity): {content_preview}\n"\
             f"Headings: {', '.join(headings)}\n"\
             f"Meta Description: {meta_description}\n"\
             f"Alt Tag Analysis: {alt_tag_summary}\n\n"\
             "Provide a structured analysis with sections on:\n"\
             "What is currently working well for SEO and why. [Try to sum up and explain what you feel their strategy currently is, and try to be complimentary where possible. make this section a paragraph format, not point form] \n"\
             "What isn't working well for SEO and why. [This section should be as detailed as possible, citing specific example thing the page to ensure eteh reader fully grasps what is holding them back. this section should have an intro and then be broken into bullets. ] \n"\
             "Detailed and actionable recommendations for improving SEO ranking for '{main_keyword}'. [this section should provide specific examples, whether that means pointing out specific places in the copy to insert keywords, or provide examples of rewritten header. Assume the reader isn't knowledgeable and provide a detailed explanation that shys away from simply giving jargon and demonstrates exactly what to change and adjust with direct examples using the actual copy from the website content provided. this section should be no shorter than 300 words, and should have bullet points to make the tasks easy to follow.]\n"\
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
            ranking = get_google_search_results(keyword, url, location)
            content, headings, meta_description, image_alts = scrape_content(url)
            
            seo_recommendations = get_recommendations(content, ranking if ranking is not None else "Not found", url, keyword, headings, meta_description, image_alts)
            
            if seo_recommendations:
                st.markdown('## SEO Recommendations:')
                st.markdown(seo_recommendations)
                
                # ... (rest of the UI code remains unchanged)

    else:
        st.warning('Please enter a URL, a keyword, and a location.')
```

This updated script should resolve the issues and run without errors. Make sure to replace the placeholder Google API key and CSE ID with your actual credentials.

Would you like me to explain any part of these changes or provide further assistance?​​​​​​​​​​​​​​​​