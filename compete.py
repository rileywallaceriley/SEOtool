import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from openai import OpenAI

# Display the logo and set the app title
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)
st.title('Competitive Edge')

# Retrieve the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=openai_api_key)

# Function to scrape content, meta title, meta description, and keywords from a URL
def scrape_competitor_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extracting meta title, description, and keywords
        title_tag = soup.title.text if soup.title else 'Title not found'
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_description_content = meta_description['content'] if meta_description else 'No meta description provided'
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        meta_keywords_content = meta_keywords['content'] if meta_keywords else 'No keywords provided'
        
        # Extracting main content for broader analysis
        content_sections = [soup.find(tag).text for tag in ['main', 'article', 'section'] if soup.find(tag)]
        main_content = ' '.join(content_sections).replace('\n', ' ') if content_sections else 'Main content not found'
        
        return {
            'url': url,
            'title': title_tag,
            'meta_description': meta_description_content,
            'meta_keywords': meta_keywords_content,
            'content': main_content
        }
    except Exception as e:
        st.error(f"Failed to scrape content: {str(e)}")
        return None

# UI for input fields
user_url = st.text_input('Enter your website URL:')
competitor_urls_input = st.text_area('Enter competitor URLs (comma-separated):')

# Button to trigger analysis
if st.button('Analyze Competitors'):
    if competitor_urls_input:
        competitor_urls = [url.strip() for url in competitor_urls_input.split(',')]
        competitor_data = [scrape_competitor_data(url) for url in competitor_urls]
        user_data = scrape_competitor_data(user_url) if user_url else None
        
        # Assuming generate_seo_analysis_and_recommendations is defined elsewhere or is meant to be part of the script
        recommendations = "Placeholder for SEO recommendations."  # Placeholder text
        
        st.subheader('Comprehensive SEO Recommendations:')
        st.markdown(recommendations)
    else:
        st.warning('Please enter at least one competitor URL.')

# Add spacing after the analysis section
st.markdown("##")  # Creates a visual space between sections

# Header for the new tools section
st.markdown("# Explore our other tools")

# Additional spacing before listing the tools
st.markdown("##")  # Adjust as needed for more space

# Define a function to display each tool section with centered title and description
def display_tool_section(header, description, button_label, button_url):
    with st.container():
        st.markdown(f"### {header}")
        st.markdown(description)
        st.markdown(f"[{button_label}]({button_url})", unsafe_allow_html=True)
        st.markdown("---")  # Divider for visual separation

# Tool descriptions
tools = [
    {
        "header": "RepuSEO-Helper",
        "description": "Receive personalized SEO recommendations to improve your site's ranking and user experience.",
        "button_label": "Use Now - RepuSEO-Helper",
        "button_url": "https://seotool-qpb8fq8bygcusdsxn6pm6s.streamlit.app"
    },
    {
        "header": "Blog SEO Helper",
        "description": "Elevate your blog's visibility with targeted SEO strategies designed for maximum engagement.",
        "button_label": "Use Now - Blog SEO Helper",
        "button_url": "https://seotool-7uqzcambnfjnuuwh9pctlr.streamlit.app"
    },
    {
        "header": "RepuSEO Plagiarism Checker",
        "description": "Ensure the originality of your content with our advanced plagiarism detection tool.",
        "button_label": "Use Now - RepuSEO Plagiarism Checker",
        "button_url": "https://seotool-cdjzyqj4qrskqvkuahwjwm.streamlit.app"
    },
]

# Loop through each tool and display its section
for tool in tools:
    display_tool_section(tool["header"], tool["description"], tool["button_label"], tool["button_url"])

# Responsive image at the bottom
left_column, image_column, right_column = st.columns([1, 10, 1])
with image_column:
    st.image("https://i.ibb.co/pxcB74N/Analysis.png")