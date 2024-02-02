import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai  # Make sure this import is here

# Display the logo at the top of the app
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)

st.title('Blog Post Generator')

# Retrieve API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=openai_api_key)

# Function to scrape content from a URL
def scrape_content(url):
    # Ensure the URL starts with http:// or https://
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.find('main').text if soup.find('main') else 'Main content not found'
    return content

# Function to generate a blog post using OpenAI's GPT model
def generate_blog_post(content, url):
    prompt = f"Write a 350-word blog post that is SEO rich, includes the following content: {content}, and links back to {url}."
    messages = [
        {"role": "system", "content": "You are an AI trained in content creation and SEO optimization."},
        {"role": "user", "content": prompt}
    ]
    
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",  # Ensure this matches your desired model
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI for input fields
url = st.text_input('Enter your URL here:')

if st.button('Generate Blog Post'):
    if url:
        with st.spinner('Generating Blog Post...'):
            content = scrape_content(url)
            blog_post = generate_blog_post(content, url)
            st.subheader('Generated Blog Post:')
            st.write(blog_post)
    else:
        st.warning('Please enter a URL.')
