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
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(description)
    nouns = [word for (word, pos) in pos_tag(words) if pos[:2] == 'NN' and word.lower() not in stop_words]
    return list(set(nouns))  # Return unique nouns

def get_search_interest(keywords):
    """
    Uses Google Trends to estimate the relative search interest of keywords.
    """
    try:
        pytrends.build_payload(keywords, cat=0, timeframe='today 12-m', geo='', gprop='')
        interest_over_time = pytrends.interest_over_time()
        if not interest_over_time.empty:
            # Normalize the scores to provide rough "volume"
            normalized_scores = (interest_over_time.mean() / interest_over_time.mean().max() * 100).round(0).astype(int)
            return normalized_scores.to_dict()
        else:
            return {keyword: "N/A" for keyword in keywords}
    except Exception as e:
        st.error(f"Error fetching search interest: {e}")
        return {keyword: "Error" for keyword in keywords}

def expand_keywords(nouns, location):
    broad_keywords = nouns
    longtail_keywords = [f"{noun} services" for noun in nouns] + [f"how to use {noun}" for noun in nouns]
    local_seo_keywords = [f"{noun} in {location}" for noun in nouns]
    return broad_keywords, longtail_keywords, local_seo_keywords

def main():
    st.title("SEO Keyword Research Tool")
    logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
    st.image(logo_url, width=200)
    
    description = st.text_area("Enter your business description:")
    location = st.text_input("Enter your business location:")
    
    if st.button("Generate Keywords"):
        nouns = extract_nouns(description)
        broad_keywords, longtail_keywords, local_seo_keywords = expand_keywords(nouns, location)
        
        # Combine all keywords for volume estimation
        all_keywords = list(set(broad_keywords + longtail_keywords + local_seo_keywords))
        search_interests = get_search_interest(all_keywords)
        
        # Prepare results with search interest
        results_with_interest = [(keyword, f"Rough search interest estimate: {search_interests.get(keyword, 'N/A')}") for keyword in all_keywords]
        
        results = format_keyword_results(description, location, results_with_interest, results_with_interest, results_with_interest)
        st.markdown(results)

if __name__ == "__main__":
    main()
