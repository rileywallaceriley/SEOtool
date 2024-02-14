import streamlit as st
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

def extract_nouns(description):
    """Extracts nouns from the business description to use as keywords."""
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(description)
    nouns = [word for (word, pos) in pos_tag(words) if pos[:2] == 'NN' and word.lower() not in stop_words]
    return list(set(nouns))

def format_keyword_insights(description, location, broad, longtail, local):
    """Formats insights with detailed logic and keyword lists."""
    broad_keywords_formatted = "\n".join(f"- {keyword}" for keyword in broad)
    longtail_keywords_formatted = "\n".join(f"- {keyword}" for keyword in longtail)
    local_keywords_formatted = "\n".join(f"- {keyword}" for keyword in local)

    result = f"""### SEO Keyword Research Insights

#### Business Description Input:
- {description}
- Location: {location}

#### Broad Keywords
- {broad_keywords_formatted}

**Insight**: Broad keywords are the pillars of your SEO strategy, providing a foundation that helps you capture a wide audience. They are crucial for creating a strong initial impression in search engines, though they can be highly competitive. By strategically using broad keywords, businesses can improve their visibility for general topics, which is essential for attracting a diverse audience. However, balancing these with more specific keywords is key to targeting the right customers.

#### Longtail Keywords
- {longtail_keywords_formatted}

**Insight**: Longtail keywords are vital for targeting niche markets and specific customer intents. They allow for more precise targeting, leading to improved conversion rates as they often match closely with what users are searching for. Crafting content around longtail keywords enables businesses to address specific needs, questions, and concerns of their audience, making it a powerful tool for engaging with potential customers on a deeper level.

#### Local SEO Keywords
- {local_keywords_formatted}

**Insight**: Local SEO keywords are indispensable for businesses operating in specific geographical locations. They target users who are searching for products or services in their area, making them crucial for driving foot traffic and local online visibility. By optimizing for local SEO keywords, businesses can significantly increase their chances of being discovered by nearby customers, enhancing local engagement and opportunities for in-person visits. Effective use of local keywords can transform how businesses connect with their community and local market.

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
        broad = nouns[:5]  # Adjust as needed
        longtail = [f"{noun} services" for noun in nouns[5:10]]
        local = [f"{noun} in {location}" for noun in nouns[10:15]]
        
        insights = format_keyword_insights(description, location, broad, longtail, local)
        st.markdown(insights, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
