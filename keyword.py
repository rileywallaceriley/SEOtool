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

def generate_keywords(nouns, location):
    """Generates broad, longtail, and local SEO keywords."""
    broad = nouns[:5]  # Take the first 5 nouns for broad keywords
    longtail = [f"{noun} services" for noun in nouns[:3]] + [f"best {noun}" for noun in nouns[3:5]]  # Generate longtail keywords
    local = [f"{noun} near {location}" for noun in nouns[:2]] + [f"{noun} in {location}" for noun in nouns[2:4]]  # Generate local SEO keywords
    
    return broad, longtail, local

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
{broad_keywords_formatted}

**Insight**: Broad keywords are essential for capturing a wide audience and establishing your presence in a broad market. These keywords help in building brand awareness and are the foundation of any SEO strategy, though they tend to be highly competitive.

#### Longtail Keywords
{longtail_keywords_formatted}

**Insight**: Longtail keywords target specific queries and are crucial for attracting a targeted audience with clear intent. These keywords often result in higher conversion rates as they match closely with user searches. They allow you to cater to specific needs and stand out in a crowded market.

#### Local SEO Keywords
{local_keywords_formatted}

**Insight**: Local SEO keywords are key for businesses targeting a specific geographic area. They help you attract local customers who are looking for services or products in their immediate vicinity. Optimizing for local keywords increases your visibility in local searches, driving foot traffic and local online engagement.
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
        
        broad, longtail, local = generate_keywords(nouns, location)
        
        insights = format_keyword_insights(description, location, broad, longtail, local)
        st.markdown(insights)

if __name__ == "__main__":
    main()
