import streamlit as st
from pytrends.request import TrendReq
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

def extract_nouns(description):
    """
    Extracts nouns from the business description to use as keywords.
    """
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(description)
    nouns = [word for (word, pos) in pos_tag(words) if pos[:2] == 'NN' and word.lower() not in stop_words]
    return list(set(nouns))

def get_search_interest(keyword):
    """
    Fetches relative search interest for a single keyword using Google Trends.
    Returns a dictionary with the keyword and its interest or error status.
    """
    try:
        pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='', gprop='')
        interest_over_time = pytrends.interest_over_time()
        if not interest_over_time.empty:
            normalized_score = (interest_over_time.mean() / interest_over_time.mean().max() * 100).round(0).astype(int)
            return {keyword: normalized_score[keyword]}
        else:
            return {keyword: "N/A"}
    except Exception as e:
        st.error(f"Error fetching search interest for {keyword}: {e}")
        return {keyword: "Error"}

def format_keyword_results(description, location, keywords_interest_dict):
    """
    Formats the keyword research results, including search interest.
    """
    result = f"""### SEO Keyword Research Results

#### Business Description Input:
{description}
Location: {location}

#### Keywords and Estimated Search Interest
"""
    for keyword, interest in keywords_interest_dict.items():
        result += f"- {keyword}: *Estimated Search Interest: {interest}*\n"

    return result

def main():
    st.title("SEO Keyword Research Tool")
    logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
    st.image(logo_url, width=200)
    
    description = st.text_area("Enter your business description:")
    location = st.text_input("Enter your business location:")
    
    if st.button("Generate Keywords"):
        nouns = extract_nouns(description)
        
        keywords_interest_dict = {}
        for noun in nouns[:5]:  # Limit to 5 to prevent overloading pytrends
            interest_dict = get_search_interest(noun)
            keywords_interest_dict.update(interest_dict)
        
        results = format_keyword_results(description, location, keywords_interest_dict)
        st.markdown(results)

if __name__ == "__main__":
    main()
