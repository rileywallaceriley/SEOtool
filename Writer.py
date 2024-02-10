import os
import streamlit as st
import openai

# Display the logo and set the app title
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)
st.title('Blog Post Generator')

# Retrieve the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Initialize OpenAI client
openai.api_key = openai_api_key

def generate_blog_post(topic, keywords, links):
    """Generate an SEO-optimized blog post using GPT-4 with the chat completions API."""
    prompt = f"Create a 350-word blog post about '{topic}' that includes the keywords {keywords} and incorporates the following links: {links}. The post should be engaging, informative, and optimized for SEO."

    try:
        with st.spinner('Generating blog post...'):
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Ensure this model supports chat completions
                messages=[{
                    "role": "system",
                    "content": "You are an AI trained to generate SEO-optimized blog posts."
                }, {
                    "role": "user",
                    "content": prompt
                }]
            )
            # Extracting the generated text from the response
            blog_post = response.choices[0].message['content']
            return blog_post
    except Exception as e:
        return f"An error occurred: {str(e)}"

# UI for input fields
topic = st.text_input('Blog Topic:', '')  # Single-row text input for topic
keywords = st.text_input('Keywords (separated by comma):')
links = st.text_input('Links to Embed (separated by comma):')

# Button to trigger blog post generation
if st.button('Generate Blog Post'):
    if topic and keywords and links:
        blog_post = generate_blog_post(topic, keywords, links)
        st.subheader('Generated Blog Post:')
        st.text_area('Blog Post:', value=blog_post, height=350)
    else:
        st.warning('Please enter the required information in all input fields.')