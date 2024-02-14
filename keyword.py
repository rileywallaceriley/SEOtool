import streamlit as st
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

def extract_nouns(description):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(description)
    # Enhance noun extraction by considering adjectives (JJ) for more descriptive keywords
    relevant_words = [word for (word, pos) in pos_tag(words) if pos[:2] in ['NN', 'JJ'] and word.lower() not in stop_words]
    return list(set(relevant_words))

def generate_keywords(words, location):
    """Generates more targeted and descriptive keywords."""
    broad = ['plant-based bakery', 'vegan baked goods', 'online vegan treats']  # Directly relevant to the business
    longtail = [f"plant-based treats in {location}", "dine safe certified bakery", "vegan cookie delivery GTA"]  # Specific services and location
    local = [f"vegan bakery near {location}", f"plant-based bakery in GTA", f"vegan treats in {location}"]  # Emphasize location
    
    return broad, longtail, local

def format_keyword_insights(description, location, broad, longtail, local):
    broad_keywords_formatted = "\n".join(f"- {keyword}" for keyword in broad)
    longtail_keywords_formatted = "\n".join(f"- {keyword}" for keyword in longtail)
    local_keywords_formatted = "\n".join(f"- {keyword}" for keyword in local)

    result = f"""### SEO Keyword Research Insights

#### Business Description Input:
- {description}
- Location: {location}

#### Broad Keywords
{broad_keywords_formatted}

Broad keywords help to establish your business's presence online, targeting audiences interested in vegan and plant-based offerings. They form the cornerstone of your SEO strategy, enhancing your brand's visibility.

#### Longtail Keywords
{longtail_keywords_formatted}

Longtail keywords are essential for reaching users with specific search intents. These more detailed queries often lead to higher engagement and conversion rates by precisely matching user interest.

#### Local SEO Keywords
{local_keywords_formatted}

Local SEO keywords focus on attracting customers within your immediate geographic area. They are crucial for businesses that rely on local patronage and want to boost their local online presence and foot traffic.
"""

    return result

def main():
    st.title("SEO Keyword Research Tool")
    logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
    st.image(logo_url, width=200)
    
    description = "Welcome to Better Batter Cookie Co., your go-to for delicious baked treats in Whitby. We're excited to announce Friday shipping to most of the GTA – check your postal code at checkout! Our dine safe certified bakery, offers all plant-based treats. Find our products directly on our site, at Mathilda’s restaurant in Oshawa, The Nooks in the Oshawa Centre, and Markets in Bowmanville."
    location = "Whitby, GTA"
    
    nouns = extract_nouns(description)
    broad, longtail, local = generate_keywords(nouns, location)
    insights = format_keyword_insights(description, location, broad, longtail, local)
    st.markdown(insights)

if __name__ == "__main__":
    main()
