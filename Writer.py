import os
import streamlit as st
from openai import OpenAI

# Define your navigation links
nav_links = {
    "Home": "http://link-to-home.com",
    "About": "http://link-to-about.com",
    "Services": "http://link-to-services.com",
    "Contact": "http://link-to-contact.com",
}

# Create a container for the header (logo + navigation bar)
header_container = st.container()

# Determine the number of columns: one for the logo + one for each navigation link
num_columns = 1 + len(nav_links)
cols = header_container.columns([1, *([3] * len(nav_links))])

# Display the logo in the first column
cols[0].image('https://i.ibb.co/JHrXTjz/REPU-03.png', width=200)

# Create buttons for navigation in the remaining columns
for col, (label, url) in zip(cols[1:], nav_links.items()):
    # Use the button widget in Streamlit for consistent styling
    if col.button(label):
        # Here you can define what happens when a button is clicked
        # For example, you might navigate to different pages of the app
        pass

st.title('RepuSEO-Helper')

# Retrieve API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=openai_api_key)

def get_seo_enhanced_copy(current_copy, keywords, links_to_embed):
    prompt = (
        f"Original Copy: {current_copy}\n"
        f"Keywords: {keywords}\n"
        f"Links to Embed: {links_to_embed}\n"
        "Edit the copy to improve its SEO score. Start the results by providing a current SEO score, then provide a final SEO score after the copy is edited. Also, provide a brief explainer of the changes for learning purposes. Your output should be in html format; no need to add header tags, page, and <p>and all that...only add all teh relevant header tags and href tags. you shoudl be able to knwo teh appropriate place to insert the given links. Also include all teh necessary meta data for SEO purposes. The meta shoudl be in a different section, as you shouldn't be delivering and header or body tags. Please present teh results with proper spacing as teh HTML code needs to be easily read by teh user. Thsi means addind spaces between paragraphs, for example ... for the changes made section add a proper bolded header. Do teh same for the meta section. The meta shoudl appear seperate from the HTMl code, with a header that says META. and teh meta shoudl not be in html format."
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

if st.button('Enhance SEO'):
    if current_copy and keywords and links_to_embed:
        with st.spinner('Enhancing SEO...'):
            seo_enhanced_copy = get_seo_enhanced_copy(current_copy, keywords, links_to_embed)
        
        st.subheader('SEO Enhanced Copy:')
        st.write(seo_enhanced_copy)
    else:
        st.warning('Please enter the required information in all input fields.')
