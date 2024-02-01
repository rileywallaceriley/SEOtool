import os
import streamlit as st
from openai import OpenAI

# Display the logo at the top of the app
logo_url = 'https://i.ibb.co/JHrXTjz/REPU-03.png'
st.image(logo_url, width=200)  # Adjust the width as needed

st.title('RepuSEO-Helper')

# Retrieve API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=openai_api_key)

def get_seo_enhanced_copy(current_copy, keywords, links_to_embed, anchor_text):
    prompt = (
        f"Original Copy: {current_copy}\n"
        f"Keywords: {keywords}\n"
        f"Links to Embed: {links_to_embed}\n"
        f"Desired Anchor Text: {anchor_text}\n\n"
        "Edit the copy to improve its SEO score. Start the results by providing a current SEO score, then provide a final SEO score after the copy is edited. Also, provide a brief explainer of the changes for learning purposes."
    )
    
    messages = [
        {"role": "system", "content": "You are an AI trained in advanced SEO and content optimization."},
        {"role": "user", "content": prompt}
    ]
    
    try:
        completion = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"
# Streamlit UI for input fields
current_copy = st.text_area('Current Copy:', height=300)
keywords = st.text_input('Keywords (separated by comma):')
links_to_embed = st.text_input('Links to Embed (separated by comma):')
anchor_text = st.text_input('Desired Anchor Text:')

if st.button('Enhance SEO'):
    if current_copy and keywords and links_to_embed and anchor_text:
        with st.spinner('Enhancing SEO...'):
            seo_enhanced_copy = get_seo_enhanced_copy(current_copy, keywords, links_to_embed, anchor_text)
        
        st.subheader('SEO Enhanced Copy:')
        st.write(seo_enhanced_copy)
    else:
        st.warning('Please enter the required information in all input fields.')

