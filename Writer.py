import os
import streamlit as st
from openai import OpenAI

# Display the logo and set the app title
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)
st.title('Blog Post Generator')

# Retrieve the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=openai_api_key)

# Function to generate a blog post using OpenAI
def generate_blog_post(topic, keywords, links):
    prompt = (
        f"Topic: {topic}\n"
        f"Keywords: {keywords}\n"
        f"Links: {links}\n\n"
        "Write a 350-word engaging, informative, and SEO-optimized blog post based on the above topic, incorporating the keywords and embedding the links appropriately."
    )
    
    try:
        with st.spinner('Generating blog post...'):
            completion = client.completions.create(
                model="gpt-4",  # Specify GPT-4 as the model
                prompt=prompt,
                temperature=0.7,
                max_tokens=1024,  # Adjusted for a longer output
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            blog_post = completion.choices[0].text.strip()
            return blog_post
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "An error occurred while generating the blog post."

# UI for input fields
topic = st.text_input('Blog Topic:', '')  # Single-row text box for concise topic description
keywords = st.text_input('Keywords (separated by comma):')
links = st.text_input('Links to Embed (separated by comma):')

# Button to trigger blog post generation
if st.button('Generate Blog Post'):
    if topic and keywords and links:
        blog_post = generate_blog_post(topic, keywords, links)
        st.subheader('Generated Blog Post:')
        st.text_area('Blog Post:', value=blog_post, height=350, help="Generated SEO-optimized blog post.")
    else:
        st.warning('Please enter the required information in all input fields.')