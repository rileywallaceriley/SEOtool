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
    {
        "header": "Competitive Edge",
        "description": "Analyze and apply winning SEO strategies from your competitors directly into your campaign.",
        "button_label": "Use Now - Competitive Edge",
        "button_url": "https://seotool-mfvdnqmf32f3visjegsxho.streamlit.app"
    },
    {
        "header": "Blog SEO Helper",
        "description": "Elevate your blog's visibility with targeted SEO strategies designed for maximum engagement.",
        "button_label": "Use Now - Blog SEO Helper",
        "button_url": "https://seotool-7uqzcambnfjnuuwh9pctlr.streamlit.app/"
    },
    {
        "header": "RepuSEO Plagiarism Checker",
        "description": "Ensure the originality of your content with our advanced plagiarism detection tool.",
        "button_label": "Use Now - RepuSEO Plagiarism Checker",
        "button_url": "https://seotool-cdjzyqj4qrskqvkuahwjwm.streamlit.app"
    },
]

# Function to display each tool section with centered title and description
def display_tool_section(header, description, button_label, button_url):
    st.markdown(f"#### {header}")
    st.write(description)
    link = f"[{button_label}]({button_url})"
    st.markdown(link, unsafe_allow_html=True)

# Displaying the tool sections
for tool in tools:
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            display_tool_section(tool['header'], tool['description'], tool['button_label'], tool['button_url'])
        st.markdown("---")  # Divider for each section

# Responsive image display at the bottom
st.image("https://i.ibb.co/pxcB74N/Analysis.png", use_column_width=True)
