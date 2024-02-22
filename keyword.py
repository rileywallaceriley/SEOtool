import streamlit as st
import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from bs4 import BeautifulSoup

# Ensure necessary NLTK resources are available
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Using the Keywords Everywhere API key from Streamlit's secrets
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

def get_keyword_data(keywords, location="Canada"):
    """Fetches keyword data including volume, CPC, and competition."""
    url = "https://api.keywordseverywhere.com/v1/get_keyword_data"
    headers = {'Authorization': f'Bearer {KEYWORDS_EVERYWHERE_API_KEY}'}
    localized_keywords = [f"{keyword} in {location}" for keyword in keywords]
    payload = {
        'country': 'CA',  # Set to Canada
        'currency': 'CAD',
        'dataSource': 'gkp',
        'kw[]': localized_keywords
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        st.error("Failed to fetch keyword data.")
        return []

# Streamlit UI setup
st.title("SEO Keyword Analysis Tool")

option = st.radio("Choose an option:", ["Analyze My Website", "Analyze Specific Keywords"])

if option == "Analyze My Website":
    url = st.text_input("Enter your website URL:")
    description = st.text_area("Enter a brief description of your site:")
    if st.button("Analyze Website"):
        if url and description:
            web_copy = extract_web_copy(url)
            keywords = extract_keywords_from_text(web_copy + " " + description)
            keyword_data = get_keyword_data(keywords[:10], "Canada")
            if keyword_data:
                for keyword_info in keyword_data:
                    st.write(f"Keyword: {keyword_info['keyword']}, Volume: {keyword_info['vol']}, CPC: {keyword_info['cpc']['value']}, Competition: {keyword_info['competition']}")
            else:
                st.write("No data found for the extracted keywords.")
        else:
            st.warning("Please enter both your website URL and a brief description.")

elif option == "Analyze Specific Keywords":
    keywords_input = st.text_input("Enter keywords separated by commas (e.g., seo, digital marketing):")
    city_name = st.text_input("Enter a Canadian city for more localized analysis (e.g., Toronto):", "Canada")
    if st.button("Analyze Keywords"):
        if keywords_input:
            keywords = [keyword.strip() for keyword in keywords_input.split(',')]
            keyword_data = get_keyword_data(keywords, city_name)
            if keyword_data:
                for keyword_info in keyword_data:
                    st.write(f"Keyword: {keyword_info['keyword']}, Volume: {keyword_info['vol']}, CPC: {keyword_info['cpc']['value']}, Competition: {keyword_info['competition']}")
            else:
                st.write("No data found for the entered keywords.")
        else:
            st.warning("Please enter some keywords for analysis.")