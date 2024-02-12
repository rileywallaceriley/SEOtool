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

# Function to generate SEO analysis and recommendations using OpenAI
def generate_seo_analysis_and_recommendations(user_data, competitor_data):
    analysis_prompt = """
    # Analyze your competitor's SEO strategy:
    # [Here, you would include a 150-word analysis based on competitor positioning]
    
    # Analyze your competitor's Meta & main copy:
    # [Include meta titles, descriptions, and main copy analysis here. be sure to include any potential weaknesses and opportunities for improvement. thsi section should be detailed.]
    
    # Identify your competitor's keywords:
    # [Detail the competitor's keywords from meta tags or content]
    
    # Roadmap for your SEO improvements:
    # [Discuss your page's strengths and suggest improvements based on competitor analysis]
    
    # Your SEO homework:
    # [Outline specific tasks for implementing the suggested improvements. The tasks shoudlnbe detailed and include the users actual content to create engaging personalized recommendations theybcan actually implement. also include a detailed logic as to why the change will help them. Each point should be at least 100 words minimum. please refrain from providing too much general information; keep it specific, personalized and tailored to the user's actual content.]
    """
    
    if user_data:
        analysis_prompt += f"User's Website Meta Title: {user_data['title']}\nUser's Meta Description: {user_data['meta_description']}\nUser's Meta Keywords: {user_data['meta_keywords']}\nUser's Main Content: {user_data['content']}\n\n"
    
    for data in competitor_data:
        if data:
            analysis_prompt += f"Competitor's URL: {data['url']}\nCompetitor's Meta Title: {data['title']}\nCompetitor's Meta Description: {data['meta_description']}\nCompetitor's Meta Keywords: {data['meta_keywords']}\nCompetitor's Main Content: {data['content']}\n\n"

    try:
        with st.spinner('Analyzing competitors...'):
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI trained in advanced SEO, content optimization, and competitive analysis."},
                    {"role": "user", "content": analysis_prompt}
                ]
            )
            recommendations = completion.choices[0].message.content
            return recommendations
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "An error occurred while generating recommendations."

# UI for input fields
user_url = st.text_input('Enter your website URL:')
competitor_urls_input = st.text_area('Enter competitor URLs (comma-separated):')

# Button to trigger analysis
if st.button('Analyze Competitors'):
    if competitor_urls_input:
        competitor_urls = [url.strip() for url in competitor_urls_input.split(',')]
        competitor_data = [scrape_competitor_data(url) for url in competitor_urls]
        user_data = scrape_competitor_data(user_url) if user_url else None
        
        recommendations = generate_seo_analysis_and_recommendations(user_data, competitor_data)
        
        st.subheader('Comprehensive SEO Recommendations:')
        st.markdown(recommendations)
    else:
        st.warning('Please enter at least one competitor URL.')