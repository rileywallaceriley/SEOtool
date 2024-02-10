import os
import streamlit as st
import openai

# Display the logo at the top of the app
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)
st.title('RepuSEO Writing Assistant')

# Retrieve API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Ensure to use the updated method for setting the API key if required by the new version
openai.api_key = openai_api_key

def generate_seo_blog_post(topic_description, keywords, links_to_embed):
    """Generate an SEO-optimized blog post using GPT-4 with the updated OpenAI API."""
    prompt = f"Write a 350-word blog post based on the topic: '{topic_description}', " \
             f"including keywords: {keywords}, and embedding links: {links_to_embed}. " \
             "Ensure the post is engaging, informative, and optimized for SEO."

    try:
        with st.spinner('Generating SEO-optimized blog post...'):
            # Adjusted to use the possibly updated method for completions in the new API version
            response = openai.Completion.create(
                model="gpt-4",
                prompt=prompt,
                temperature=0.7,
                max_tokens=800,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            return response['choices'][0]['text'].strip()  # Adjusted according to the new response structure
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Adjusted UI component for the blog topic description
topic_description = st.text_input('Blog Topic Description:', '')  # Single-row text box
keywords = st.text_input('Keywords (separated by comma):')
links_to_embed = st.text_input('Links to Embed (separated by comma):')

if st.button('Generate Blog Post'):
    if topic_description and keywords and links_to_embed:
        blog_post = generate_seo_blog_post(topic_description, keywords, links_to_embed)
        st.subheader('SEO-Optimized Blog Post:')
        st.text_area('Generated Post:', value=blog_post, height=250)
    else:
        st.warning('Please enter the required information in all input fields.')