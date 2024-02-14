import streamlit as st

def generate_seo_keywords(description, location):
    """
    Generates SEO keywords based on the business description and location.
    This function manually defines keywords for demonstration purposes.
    """
    broad_keywords = [
        'plant-based bakery',
        'vegan cookies',
        'baked treats',
        'online bakery shop',
    ]

    longtail_keywords = [
        'plant-based bakery in Whitby',
        'vegan cookie delivery GTA',
        'dine safe certified vegan treats',
        'online vegan treats ordering',
    ]

    local_seo_keywords = [
        'vegan bakery Whitby',
        'plant-based treats Oshawa',
        'vegan cookies Bowmanville',
        'GTA vegan baked goods delivery',
    ]

    return broad_keywords, longtail_keywords, local_seo_keywords

def format_keyword_insights(broad, longtail, local):
    """
    Formats the generated keywords into a markdown string with insights.
    """
    broad_formatted = "\n".join(f"- {keyword}" for keyword in broad)
    longtail_formatted = "\n".join(f"- {keyword}" for keyword in longtail)
    local_formatted = "\n".join(f"- {keyword}" for keyword in local)

    insights = f"""
### SEO Keyword Research Insights

#### Broad Keywords
{broad_formatted}

Broad keywords help establish your presence in the market, targeting a wide audience interested in vegan and plant-based options.

#### Longtail Keywords
{longtail_formatted}

Longtail keywords target specific queries, leading to higher conversion rates as they closely match user search intent.

#### Local SEO Keywords
{local_formatted}

Local SEO keywords target users in specific geographic areas, essential for attracting local traffic and enhancing visibility in local search results.
    """

    return insights

def main():
    st.title("SEO Keyword Research Tool")
    description = "Welcome to Better Batter Cookie Co., your go-to for delicious baked treats in Whitby. We're excited to announce Friday shipping to most of the GTA – check your postal code at checkout! Our dine safe certified bakery, offers all plant-based treats. Find our products directly on our site, at Mathilda’s restaurant in Oshawa, The Nooks in the Oshawa Centre, and Markets in Bowmanville."
    location = "Whitby, GTA, Oshawa, Bowmanville"

    broad_keywords, longtail_keywords, local_seo_keywords = generate_seo_keywords(description, location)
    insights = format_keyword_insights(broad_keywords, longtail_keywords, local_seo_keywords)
    st.markdown(insights)

if __name__ == "__main__":
    main()
