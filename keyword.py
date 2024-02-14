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
    return list(set(nouns))

def get_search_interest(keywords):
    try:
        pytrends.build_payload(keywords, cat=0, timeframe='today 12-m', geo='', gprop='')
        interest_over_time = pytrends.interest_over_time()
        if not interest_over_time.empty:
            normalized_scores = (interest_over_time.mean() / interest_over_time.mean().max() * 100).round(0).astype(int)
            return normalized_scores.to_dict()
        else:
            return {keyword: "N/A" for keyword in keywords}
    except Exception as e:
        st.error(f"Error fetching search interest: {e}")
        return {keyword: "Error" for keyword in keywords}

def format_keyword_results(description, location, broad_keywords, longtail_keywords, local_seo_keywords):
    result = f"""### SEO Keyword Research Results

#### Business Description Input:
{description}
Location: {location}

#### Broad Keywords
**Description**: General keywords relevant to the business's core activities.
**Keywords**:
"""
    for keyword, interest in broad_keywords.items():
        result += f"- {keyword}: *Estimated Search Interest: {interest}*\n"

    result += """
#### Longtail Keywords
**Description**: More specific queries that potential customers might use.
**Keywords**:
"""
    for keyword, interest in longtail_keywords.items():
        result += f"- {keyword}: *Estimated Search Interest: {interest}*\n"

    result += """
#### Local SEO Keywords
**Description**: Keywords that include the geographical location to target local searches.
**Keywords**:
"""
    for keyword, interest in local_seo_keywords.items():
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
        broad_keywords = nouns[:5]  # Simplification for demonstration
        longtail_keywords = [f"{noun} services" for noun in nouns[:5]]
        local_seo_keywords = [f"{noun} in {location}" for noun in nouns[:5]]
        
        all_keywords = list(set(broad_keywords + longtail_keywords + local_seo_keywords))
        search_interests = get_search_interest(all_keywords)
        
        # Divide search interests back into categories
        broad_interests = {k: search_interests[k] for k in broad_keywords}
        longtail_interests = {k: search_interests[k] for k in longtail_keywords}
        local_interests = {k: search_interests[k] for k in local_seo_keywords}
        
        results = format_keyword_results(description, location, broad_interests, longtail_interests, local_interests)
        st.markdown(results)

if __name__ == "__main__":
    main()
