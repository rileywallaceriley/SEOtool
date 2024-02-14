import streamlit as st
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

def extract_nouns_and_adjectives(description):
    """Extracts nouns and adjectives from the business description for keyword generation."""
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(description)
    relevant_words = [word for (word, pos) in pos_tag(words) if pos[:2] in ['NN', 'JJ'] and word.lower() not in stop_words]
    return list(set(relevant_words))

def generate_keywords(words, location):
    """Generates broad, longtail, and local SEO keywords based on extracted words and location."""
    # Example keyword generation; adjust based on your strategy
    broad = words[:5]  # Simplified example, consider enhancing logic
    longtail = [f"{word} services in {location}" for word in words[:3]]  # Tailored longtail keywords
    local = [f"{word} near {location}" for word in words[:2]]  # Localized keywords
    
    return broad, longtail, local

def format_keyword_insights(description, location, broad, longtail, local):
    """Formats insights with generated keywords."""
    broad_keywords_formatted = "\n".join(f"- {keyword}" for keyword in broad)
    longtail_keywords_formatted = "\n".join(f"- {keyword}" for keyword in longtail)
    local_keywords_formatted = "\n".join(f"- {keyword}" for keyword in local)

    result = f"""### SEO Keyword Research Insights

#### Business Description Input:
- Description: {description}
- Location: {location}

#### Broad Keywords
{broad_keywords_formatted}

**Insight**: Broad keywords help establish a wide-reaching presence in your market, ideal for building brand awareness.

#### Longtail Keywords
{longtail_keywords_formatted}

**Insight**: Longtail keywords target specific user intents, crucial for attracting a focused audience and improving conversion rates.

#### Local SEO Keywords
{local_keywords_formatted}

**Insight**: Local SEO keywords are essential for businesses targeting a geographical area, helping to attract local customers.
"""

    return result

def main():
    st.title("SEO Keyword Research Tool")
    st.image('https://i.ibb.co/VvYtGFg/REPU-11.png', width=200)
    
    description = st.text_area("Enter your business description:")
    location = st.text_input("Enter your business location:")
    
    if st.button("Generate Keywords"):
        if description and location:
            relevant_words = extract_nouns_and_adjectives(description)
            broad, longtail, local = generate_keywords(relevant_words, location)
            insights = format_keyword_insights(description, location, broad, longtail, local)
            st.markdown(insights)
        else:
            st.warning("Please enter both a business description and location.")

if __name__ == "__main__":
    main()
