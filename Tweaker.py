import streamlit as st
import nltk
import requests
from bs4 import BeautifulSoup as bs
from difflib import SequenceMatcher
import pandas as pd
from urllib.parse import quote_plus
import warnings

warnings.filterwarnings("ignore", module='bs4')

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(nltk.corpus.stopwords.words('english'))

# Define your Google Cloud API key and Custom Search Engine ID
google_api_key = 'AIzaSyC0qDb3rdkRKxFrMaFyyDPMqBMYtOrrC4c'
google_cse_id = '34200d9d3c6084a1f'

# Function to purify text by removing stop words
def purifyText(string):
    words = nltk.word_tokenize(string)
    return (" ".join([word for word in words if word not in stop_words]))

# Function to search using Google Custom Search JSON API
def searchGoogle(query, num, api_key=GOOGLE_API_KEY, cse_id=GOOGLE_CSE_ID):
    query = quote_plus(query)
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={cse_id}&key={api_key}&num={num}"

    data = requests.get(url).json()
    search_items = data.get("items")
    
    urls = []
    if search_items:
        for item in search_items:
            urls.append(item.get("link"))
    
    return urls[:num]

# Function to extract text from a webpage
def extractText(url):
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    return soup.get_text()

# Function to verify web content for similarity
def webVerify(string, results_per_sentence):
    sentences = nltk.sent_tokenize(string)
    matching_sites = []
    for url in searchGoogle(query=string, num=results_per_sentence):
        matching_sites.append(url)
    for sentence in sentences:
        for url in searchGoogle(query=sentence, num=results_per_sentence):
            matching_sites.append(url)
    return (list(set(matching_sites)))

# Function to calculate similarity between two strings
def similarity(str1, str2):
    return (SequenceMatcher(None, str1, str2).ratio()) * 100

# Function to generate a plagiarism report
def report(text):
    matching_sites = webVerify(purifyText(text), 2)
    matches = {}
    for i in range(len(matching_sites)):
        matches[matching_sites[i]] = similarity(text, extractText(matching_sites[i]))
    matches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)}
    return matches

# Function to return the report as an HTML table
def returnTable(dictionary):
    df = pd.DataFrame({'Similarity (%)': dictionary})
    return df.to_html()

# Streamlit UI Components
st.title('RepuSEO Plagiarism Checker')
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)  # Adjust the width as needed

input_text = st.text_area('Text to Check for Plagiarism:', height=300)

if st.button('Check for Plagiarism'):
    if input_text:
        with st.spinner('Checking for plagiarism...'):
            plagiarism_report = report(input_text)
            formatted_report = returnTable(plagiarism_report)
            st.markdown('## Plagiarism Check Results')
            st.write(formatted_report, unsafe_allow_html=True)
    else:
        st.warning('Please enter the text you want to check.')
