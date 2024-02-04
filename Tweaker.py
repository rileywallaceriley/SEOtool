import streamlit as st
import nltk
import requests
from bs4 import BeautifulSoup as bs
from difflib import SequenceMatcher
import pandas as pd
import warnings

warnings.filterwarnings("ignore", module='bs4')

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(nltk.corpus.stopwords.words('english')) 

# Function to purify text by removing stop words
def purifyText(string):
    words = nltk.word_tokenize(string)
    return (" ".join([word for word in words if word not in stop_words]))

# Function to search on Bing and get URLs
def searchBing(query, num):
    url = 'https://www.bing.com/search?q=' + query
    urls = []
    page = requests.get(url, headers = {'User-agent': 'John Doe'})
    soup = bs(page.text, 'html.parser')
    for link in soup.find_all('a'):
        url = str(link.get('href'))
        if url.startswith('http'):
            if not url.startswith('http://go.m') and not url.startswith('https://go.m'):
                urls.append(url)
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
    for url in searchBing(query=string, num=results_per_sentence):
        matching_sites.append(url)
    for sentence in sentences:
        for url in searchBing(query=sentence, num=results_per_sentence):
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
