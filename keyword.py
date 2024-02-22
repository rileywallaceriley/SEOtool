import streamlit as st
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Use API key from Streamlit secrets
KEYWORDS_EVERYWHERE_API_KEY = st.secrets["keywords_everywhere_api_key"]

def extract_web_copy(url):
    """Extracts text from the homepage of the provided URL."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.stripped_strings
        return " ".join(text for text in texts)
    except Exception as e:
        st.error(f"Failed to fetch webpage: {e}")
        return ""

def extract_keywords_from_text(text):
    """Extracts keywords from the provided text using NLTK."""
    try:
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text)
        keywords = [word for (word, pos) in pos_tag(words) if pos[:2] in ['NN', 'JJ'] and word.lower() not in stop_words]
        return list(set(keywords))
    except LookupError as e:
        st.error("NLTK resources not found. Please download them using nltk.download().")
        return []

def get_keyword_data(keywords):
    """Fetches keyword data including volume, CPC, and competition."""
    url = "https://api.keywordseverywhere.com/v1/get_keyword_data"
    headers = {
        'Authorization': f'Bearer {KEYWORDS_EVERYWHERE_API_KEY}'
    }
    data = {
        'country': 'us',
        'currency': 'USD',
        'dataSource': 'gkp',
        'kw[]': keywords
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['data']
    else:
        st.error("Failed to fetch keyword data.")
        return []

# Streamlit UI setup
st.title("SEO Keyword Analysis Tool")

url = st.text_input("Enter your website URL:", "")
analyze_button = st.button("Analyze Keywords")

if analyze_button and url:
    with st.spinner("Extracting content and analyzing keywords..."):
        web_copy = extract_web_copy(url)
        if web_copy:
            keywords = extract_keywords_from_text(web_copy)
            if keywords:
                keyword_data = get_keyword_data(keywords[:10])  # Limiting to first 10 keywords for brevity
                if keyword_data:
                    for keyword_info in keyword_data:
                        st.write(f"Keyword: {keyword_info['keyword']}, Volume: {keyword_info['vol']}, CPC: {keyword_info['cpc']['value']}, Competition: {keyword_info['competition']}")
                else:
                    st.write("No data found for the extracted keywords.")
            else:
                st.write("No keywords extracted from the website content.")
        else:
            st.write("Failed to extract content from the URL provided.")