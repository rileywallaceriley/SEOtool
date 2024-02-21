import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Assuming API key is set as an environment variable
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

def display_keyword_data(data):
    """Displays keyword data fetched from Keywords Everywhere."""
    # Similar to previous display_keyword_data function
    pass

def get_keyword_data(keywords):
    """Fetches keyword data from Keywords Everywhere API."""
    # Similar to previous get_keyword_data function
    pass

def main():
    st.title("SEO Keyword Tool")

    option = st.radio("Choose a mode:", ("Keyword Analysis", "Keyword Planner"))

    if option == "Keyword Analysis":
        user_keywords = st.text_input("Enter keywords separated by commas (e.g., seo tools, keyword research):")
        if st.button("Analyze Keywords"):
            if user_keywords:
                keywords_list = [keyword.strip() for keyword in user_keywords.split(",")]
                keyword_data = get_keyword_data(keywords_list)
                display_keyword_data(keyword_data)
            else:
                st.warning("Please enter at least one keyword to analyze.")
    elif option == "Keyword Planner":
        url = st.text_input("Enter your website URL:")
        description = st.text_area("Enter a brief description of your brand, including location and products:")
        if st.button("Generate Keyword Suggestions"):
            if url and description:
                web_copy = extract_web_copy(url)
                if web_copy:
                    combined_text = f"{description} {web_copy}"
                    suggested_keywords = extract_keywords_from_text(combined_text)
                    keyword_data = get_keyword_data(suggested_keywords[:10])  # Limit to first 10 suggestions for brevity
                    display_keyword_data(keyword_data)
                else:
                    st.error("Failed to extract content from the provided URL.")
            else:
                st.warning("Please enter both your website URL and brand description.")

if __name__ == "__main__":
    main()
