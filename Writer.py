import os
import streamlit as st
from openai import OpenAI

# Display the logo at the top of the app
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)  # Adjust the width as needed

st.title('RepuSEO Writing Assistant')

# Retrieve API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=openai_api_key)

def generate_seo_blog_post(topic_description, keywords, links_to_embed):
    prompt = (
        f"Write a 250-word blog post based on the following topic description: {topic_description}\n"
        f"Incorporate these keywords: {keywords}.\n"
        f"Include these links within the content where appropriate: {links_to_embed}.\n"
        "Ensure the blog post is engaging, informative, and optimized for SEO."
    )
    
    try:
        completion = client.completions.create(
            model='text-davinci-003',  # Consider updating this to 'gpt-4' or the latest available model
            prompt=prompt,
            temperature=0.7,
            max_tokens=1024,  # Adjust as necessary to ensure the output length is as desired
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return completion.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI for input fields
topic_description = st.text_area('Blog Topic Description:', height=150)
keywords = st.text_input('Keywords (separated by comma):')
links_to_embed = st.text_input('Links to Embed (separated by comma):')

if st.button('Generate Blog Post'):
    if topic_description and keywords and links_to_embed:
        with st.spinner('Generating SEO-optimized blog post...'):
            blog_post = generate_seo_blog_post(topic_description, keywords, links_to_embed)
        
        st.subheader('SEO-Optimized Blog Post:')
        st.text_area('Generated Post:', value=blog_post, height=250, help="Here's the generated SEO-optimized blog post based on your input.")
    else:
        st.warning('Please enter the required information in all input fields.')