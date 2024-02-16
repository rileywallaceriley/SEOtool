import os
import streamlit as st
from openai import OpenAI

# Display the logo at the top of the app
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)

st.title('SEO-Rich Blog Writer')

# Retrieve API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=openai_api_key)

# Streamlit UI for input fields
blog_topic = st.text_input('Enter the blog topic here:')
blog_length = st.selectbox('Choose the blog length:', [350, 700, 1250], index=1)  # Default to 700 words
url = st.text_input('Enter a reference URL here (optional):')
include_cta = st.checkbox('Include a Call to Action?')
cta_text = st.text_input('Enter your Call to Action text here:', '') if include_cta else ""

def generate_structured_blog(topic, length, url="", include_cta=False, cta_text=""):
    """
    Generates structured blog content with specified sections and optional CTA using GPT-4's chat completions.

    Parameters:
    - topic: The topic for the blog.
    - length: Target length of the blog (350, 700, or 1250 words).
    - url: Optional reference URL for linking within the blog.
    - include_cta: Whether to include a Call to Action.
    - cta_text: Text for the Call to Action (if included).

    Returns:
    A string containing the structured blog content.
    """
    # Preparing messages for the chat
    messages = [
        {"role": "system", "content": "You are a highly skilled AI trained to write SEO-rich blog posts. Include an SEO Title, Introduction, Main Body Copy, and Conclusion."},
        {"role": "user", "content": f"Write a blog post about '{topic}' that is approximately {length} words long."}
    ]

    if include_cta:
        messages.append({"role": "user", "content": f"Include a call to action: '{cta_text}'."})
    
    if url:
        messages.append({"role": "user", "content": f"Reference URL: {url}"})

    try:
        completion = client.chat.completions.create(
            model='gpt-4',
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

if st.button('Generate Blog Content'):
    blog_content = generate_structured_blog(blog_topic, blog_length, url, include_cta, cta_text)
    st.text_area("Generated Blog Content:", value=blog_content, height=400)
