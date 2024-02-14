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

def get_individual_search_interest(keyword):
    try:
        pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='', gprop='')
        interest_over_time = pytrends.interest_over_time()
        if not interest_over_time.empty:
            normalized_score = interest_over_time.mean().round(0).astype(int)[keyword]
            return normalized_score
        else:
            return None
    except Exception as e:
        print(f"Error fetching search interest for {keyword}: {e}")
        return None

def calculate_average_interest(interests):
    valid_interests = [interest for interest in interests.values() if interest is not None]
    if valid_interests:
        return sum(valid_interests) / len(valid_interests)
    return "N/A"

def format_keyword_insights(description, location, broad_keywords, longtail_keywords, local_seo_keywords):
    broad_avg = calculate_average_interest(broad_keywords)
    longtail_avg = calculate_average_interest(longtail_keywords)
    local_avg = calculate_average_interest(local_seo_keywords)

    result = f"""### SEO Keyword Research Insights

#### Business Description Input:
{description}
Location: {location}

#### Broad Keywords
**Average Search Volume**: {broad_avg}
**Insight**: Broad keywords are foundational for your SEO strategy, helping to establish a wide net in search results. They are essential for capturing high-level interest in your business domain, although they might be more competitive.

#### Longtail Keywords
**Average Search Volume**: {longtail_avg}
**Insight**: Longtail keywords are critical for targeting specific customer intents and queries. These keywords, being more detailed, can drive higher conversion rates as they often match closely with the user's search intent.

#### Local SEO Keywords
**Average Search Volume**: {local_avg}
**Insight**: Local SEO keywords are indispensable for businesses serving specific geographic areas. They help in capturing searches with local intent, essential for attracting customers in your vicinity. High-performing local keywords can significantly increase visibility in local search results, driving foot traffic and local engagements.
"""

    return result

def main():
    st.title("SEO Keyword Research Tool")
    logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
    st.image(logo_url, width=200)
    
    description = st.text_area("Enter your business description:")
    location = st.text_input("Enter your business location:")
    
    if st.button("Generate Keywords"):
        nouns = extract_nouns(description)
        
        all_keywords = nouns[:5]  # Simplified for demonstration
        interests = {keyword: get_individual_search_interest(keyword) for keyword in all_keywords}
        
        # Simulate categorization for demonstration
        broad_interests = {k: v for k, v in interests.items() if k in nouns[:2]}
        longtail_interests = {k: v for k, v in interests.items() if k in nouns[2:4]}
        local_interests = {k: v for k, v in interests.items() if k in nouns[4:5]}
        
        insights = format_keyword_insights(description, location, broad_interests, longtail_interests, local_interests)
        st.markdown(insights)

if __name__ == "__main__":
    main()
