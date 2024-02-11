import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# Display the logo at the top of the app
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)  # Adjust the width as needed

st.title('SEO-Rich Blog Writer')

# Initialize session states for button presses
if 'generate_blog_pressed' not in st.session_state:
    st.session_state['generate_blog_pressed'] = False

# Retrieve API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=openai_api_key)

# Streamlit UI for input fields
blog_topic = st.text_input('Enter the blog topic here:')
main_keywords = st.text_input('Enter the main keywords (comma-separated) here:')
blog_length = st.number_input('Enter the desired blog length (number of words):', min_value=150, max_value=3000, value=1000)

def generate_blog_post(topic, keywords, length):
    # Generate a prompt that instructs the AI to write an SEO-rich blog post
    prompt = f"Write a detailed, engaging, and SEO-optimized blog post about '{topic}'. Include the following keywords: {keywords}. The blog post should be around {length} words long, well-structured with headers, subheaders, and include a keyword-optimized title."

    messages = [
        {"role": "system", "content": "You are an AI trained in advanced SEO and content optimization."},
        {"role": "user", "content": prompt}
    ]
    
    try:
        completion = client.chat.completions.create(
            model='gpt-4',  # Assuming using GPT-4, adjust as necessary
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

if st.button('Generate Blog Post'):
    if blog_topic and main_keywords and blog_length:
        with st.spinner('Generating blog post...'):
            blog_post = generate_blog_post(blog_topic, main_keywords, blog_length)
            st.session_state['generate_blog_pressed'] = True
            st.subheader('Generated Blog Post:')
            st.write(blog_post)
    else:
        st.warning('Please enter a blog topic, main keywords, and desired blog length.')

# Ensure there are no repeated declarations or sensitive information like API keys hardcoded in your script.