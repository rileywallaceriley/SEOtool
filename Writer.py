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
    Generates structured blog content using GPT-4's chat completions.
    """
    messages = [
        {"role": "system", "content": "You are a highly skilled AI trained to write SEO-rich blog posts with natural headings and structured content."},
        {"role": "user", "content": f"Create a structured blog post on '{topic}' targeting around {length} words. Please format with natural headings for sections without explicitly naming them 'Introduction' or 'Conclusion'. Include various subtopics for a comprehensive coverage."}
    ]

    if include_cta and cta_text:
        messages.append({"role": "user", "content": f"Conclude with a call to action: '{cta_text}'."})
    
    if url:
        messages.append({"role": "user", "content": f"Reference URL: {url}"})

    try:
        with st.spinner('Please wait... Writing'):
            completion = client.chat.completions.create(
                model='gpt-4',
                messages=messages
            )
        blog_content = completion.choices[0].message.content
        return blog_content
    except Exception as e:
        return f"An error occurred: {str(e)}"

if st.button('Generate Blog Content'):
    blog_content = generate_structured_blog(blog_topic, blog_length, url, include_cta, cta_text)
    st.markdown("### Blog Content")
    st.markdown(blog_content, unsafe_allow_html=True)  # Display the blog content

    # Display the additional SEO tools and resources
    st.markdown("---")
    tools = [
        # Tool descriptions as provided in the request
    ]

    # Function to display each tool section with centered title and description
    def display_tool_section(header, description, button_label, button_url):
        with st.container():
            st.markdown(f"#### {header}", unsafe_allow_html=True)
            st.markdown(f"{description}", unsafe_allow_html=True)
            
            # Centered button with HTML
            st.markdown(f"""<div style="text-align: center;"><a href="{button_url}" target="_blank"><button style='margin-top: 10px; width: auto; padding: 10px 20px; border-radius: 5px; border: none; color: black; background-color: #f4a261;'>{button_label}</button></a></div>""", unsafe_allow_html=True)
            
            # Divider
            st.markdown("---")

    # Displaying the tool sections
    for tool in tools:
        display_tool_section(tool['header'], tool['description'], tool['button_label'], tool['button_url'])

    # Responsive image display at the bottom
    left_column, image_column, right_column = st.columns([1, 10, 1])
    with image_column:
        st.image("https://i.ibb.co/pxcB74N/Analysis.png", use_column_width=True)
