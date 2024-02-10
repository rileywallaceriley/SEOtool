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
    st.error("The OPENAI_API_KEY environment variable is not set.")
    st.stop()

# Initialize OpenAI client
openai.api_key = openai_api_key

def generate_seo_blog_post(topic_description, keywords, links_to_embed, engine='gpt-4', purpose='general'):
    """Generate an SEO-optimized blog post using a specified GPT model."""
    prompt = f"Write a 250-word blog post based on the topic: '{topic_description}', " \
             f"including keywords: {keywords}, and embedding links: {links_to_embed}. " \
             "Ensure the post is engaging, informative, and optimized for SEO."

    try:
        with st.spinner('Generating SEO-optimized blog post...'):
            response = openai.Completion.create(
                model=engine,  # Use the engine parameter to specify the model
                prompt=prompt,
                temperature=0.7,
                max_tokens=600,  # Adjusted for approximately 250 words
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI for input fields
topic_description = st.text_area('Blog Topic Description:', height=150)
keywords = st.text_input('Keywords (separated by comma):')
links_to_embed = st.text_input('Links to Embed (separated by comma):')

if st.button('Generate Blog Post'):
    if topic_description and keywords and links_to_embed:
        blog_post = generate_seo_blog_post(topic_description, keywords, links_to_embed)
        st.subheader('SEO-Optimized Blog Post:')
        st.text_area('Generated Post:', value=blog_post, height=250, help="Here's the generated SEO-optimized blog post based on your input.")
    else:
        st.warning('Please enter the required information in all input fields.')