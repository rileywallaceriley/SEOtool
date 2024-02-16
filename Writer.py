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

def generate_structured_blog(keyword, url, length, include_cta=False, cta_text=""):
    """
    Generates structured blog content with specified sections and optional CTA.

    Parameters:
    - keyword: Main keyword for the blog.
    - url: Reference URL for linking within the blog.
    - length: Target length of the blog (350, 700, or 1250 words).
    - include_cta: Whether to include a Call to Action.
    - cta_text: Text for the Call to Action (if included).

    Returns:
    A string containing the structured blog content.
    """
    # Adjusting the prompt based on the blog length
    word_count = length
    section_word_counts = {
        'intro': word_count // 10,  # Approx. 10% of the words for the introduction
        'main_body': word_count * 7 // 10,  # Approx. 70% for the main body
        'conclusion': word_count * 2 // 10,  # Approx. 20% for the conclusion
    }

    prompt = (f"Create a structured blog post about '{keyword}' that is SEO optimized and includes the following sections: "
              f"SEO Title, Introduction (~{section_word_counts['intro']} words), "
              f"Main Body Copy (~{section_word_counts['main_body']} words), "
              f"Conclusion (~{section_word_counts['conclusion']} words).")

    if include_cta:
        prompt += f" End with a Call to Action: '{cta_text}'."
    
    try:
          completion = client.chat.completions.create(
            model='gpt-4',  # Assuming using GPT-4, adjust as necessary
            messages=messages
        )
        return completion.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI for input
keyword = st.text_input('Enter your target keyword here:')
url = st.text_input('Enter a reference URL here:')
blog_length = st.selectbox('Choose the blog length:', [350, 700, 1250])
include_cta = st.checkbox('Include a Call to Action?')
cta_text = st.text_input('Enter your Call to Action text here:') if include_cta else ""

if st.button('Generate Blog Content'):
    blog_content = generate_structured_blog(keyword, url, blog_length, include_cta, cta_text)
    st.text_area("Generated Blog Content:", value=blog_content, height=250)
