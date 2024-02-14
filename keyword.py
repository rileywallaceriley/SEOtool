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

def get_search_interests(keywords):
    interests = {}
    for keyword in keywords:
        interest = get_individual_search_interest(keyword)
        interests[keyword] = interest if interest is not None else "N/A"
    return interests

def calculate_average_interest(interests):
    valid_interests = [interest for interest in interests.values() if interest is not None and interest != "N/A"]
    if valid_interests:
        average = sum(valid_interests) / len(valid_interests)
        return round(average, 2)
    return "N/A"

def format_keyword_insights(description, location, broad, longtail, local, broad_interests, longtail_interests, local_interests):
    broad_avg = calculate_average_interest(broad_interests)
    longtail_avg = calculate_average_interest(longtail_interests)
    local_avg = calculate_average_interest(local_interests)

    result = f"""### SEO Keyword Research Insights

#### Business Description Input:
{description}
Location: {location}

#### Broad Keywords
**Keywords**: {', '.join(broad)}
**Average Search Volume**: {broad_avg}
**Insight**: Broad keywords establish your presence in wide-reaching topics related to your business. They're essential but competitive, offering a high-level view of your market.

#### Longtail Keywords
**Keywords**: {', '.join(longtail)}
**Average Search Volume**: {longtail_avg}
**Insight**: Longtail keywords target specific queries, leading to higher conversion rates. They're less competitive and closely align with user intent, making them valuable for targeted content.

#### Local SEO Keywords
**Keywords**: {', '.join(local)}
**Average Search Volume**: {local_avg}
**Insight**: Local keywords are crucial for businesses targeting specific areas. They help capture users with local intent, driving relevant traffic and potential in-person visits.
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
        
        # Generate keyword categories
        broad = nouns[:3]
        longtail = [f"{noun} services" for noun in nouns[3:5]]
        local = [f"{noun} in {location}" for noun in nouns[5:7]]
        
        # Collect all keywords for interest analysis
        all_keywords = broad + longtail + local
        interests = get_search_interests(all_keywords)
        
        insights = format_keyword_insights(description, location, broad, longtail, local, interests, interests, interests)
        st.markdown(insights)

if __name__ == "__main__":
    main()
