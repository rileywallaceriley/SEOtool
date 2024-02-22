import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag

# Assuming you've set your API key as an environment variable
KEYWORDS_EVERYWHERE_API_KEY = os.getenv("KEYWORDS_EVERYWHERE_API_KEY")

def extract_web_copy(url):
    """Extracts text from the homepage of the provided URL."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            texts = soup.stripped_strings
            return " ".join(text for text in texts)
        else:
            return None
    except Exception as e:
        st.error(f"Failed to fetch webpage: {e}")
        return None

def extract_keywords_from_text(text):
    """Extracts keywords from the provided text using NLTK."""
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    keywords = [word for (word, pos) in pos_tag(words) if pos[:2] in ['NN', 'JJ'] and word.lower() not in stop_words]
    return list(set(keywords))

def get_keyword_data(keywords, location):
    """Fetches keyword data from Keywords Everywhere API, considering the user's location."""
    api_url = "https://api.keywordseverywhere.com/v1/get_keyword_data"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {KEYWORDS_EVERYWHERE_API_KEY}'
    }
    data = {
        'country': location,  # Using the location input to tailor the API request
        'currency': 'USD',
        'dataSource': 'gkp',
        'kw[]': keywords
    }
    
    response = requests.post(api_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data: {response.text}")
        return None

def display_keyword_data(data):
    """Displays keyword data fetched from Keywords Everywhere."""
    if data and 'data' in data:
        for keyword_info in data['data']:
            keyword = keyword_info['keyword']
            volume = keyword_info['vol']
            cpc = keyword_info['cpc']['value']
            competition = keyword_info['competition']
            st.write(f"**Keyword:** {keyword}, **Volume:** {volume}, **CPC:** {cpc}, **Competition:** {competition}")
            if 'trend' in keyword_info and keyword_info['trend']:
                st.write("Monthly Trends (Last 12 Months):")
                for month_data in keyword_info['trend']:
                    st.write(f"Month: {month_data['month']} {month_data['year']}, Volume: {month_data['value']}")
            st.write("---")
    else:
        st.write("No data available for the keywords provided.")

def main():
    st.title("SEO Keyword Tool")

    option = st.radio("Choose a mode:", ("Keyword Analysis", "Keyword Planner"))

    location = st.text_input("Enter your target location (e.g., US, CA, GB):", help="Use country codes for better accuracy.")

    if option == "Keyword Analysis":
        user_keywords = st.text_input("Enter keywords separated by commas (e.g., seo tools, keyword research):")
        if st.button("Analyze Keywords") and location:
            if user_keywords:
                keywords_list = [keyword.strip() for keyword in user_keywords.split(",")]
                keyword_data = get_keyword_data(keywords_list, location)
                display_keyword_data(keyword_data)
            else:
                st.warning("Please enter at least one keyword to analyze.")
    elif option == "Keyword Planner":
        url = st.text_input("Enter your website URL:")
        description = st.text_area("Enter a brief description of your brand, including location and products:")
        if st.button("Generate Keyword Suggestions") and location:
            if url and description:
                web_copy = extract_web_copy(url)
                if web_copy:
                    combined_text = f"{description} {web_copy}"
                    suggested_keywords = extract_keywords_from_text(combined_text)
                    keyword_data = get_keyword_data(suggested_keywords[:10], location)  # Limit to first 10 suggestions
                    display_keyword_data(keyword_data)
                else:
                    st.error("Failed to extract content from the provided URL.")
            else:
                st.warning("Please enter both your website URL and brand description.")

if __name__ == "__main__":
    main()