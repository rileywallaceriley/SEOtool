import streamlit as st

# Display the logo
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)

# Embed YouTube Video
st.video('https://youtu.be/G6GIb9nwUYE?si=kUrABMKxnwtoKO-M')

# Brief overview of your tools, centered
st.markdown("""
<div style="text-align: center;">
    <h2>Elevate Your SEO Game</h2>
    <p>Unlock the full potential of your website with our SEO Tools Suite. We take the complexity out of SEO, making it accessible and actionable for everyone. Whether you're a small business owner, a solo entrepreneur, or a content creator, our tools are designed to give you clear, straightforward recommendations that drive results. Improve your search engine rankings, learn from your competition, and make SEO work for you.<br><br></p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Define the function to display the tool section with description
def display_tool_section(header, description, button_label, button_url):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div style="text-align: center;">
            <h2>{header}</h2>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <a href="{button_url}" target="_blank">
            <button style='width: 100%; height: 50px; padding: 10px; border-radius: 5px; border: none; color: black; background-color: #f4a261;'>
                {button_label}
            </button>
        </a>
        """, unsafe_allow_html=True)

# Tool descriptions
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
        "button_url": "https://seotool-7uqzcambnfjnuuwh9pctlr.streamlit.app"
    },
    {
        "header": "RepuSEO Plagiarism Checker",
        "description": "Ensure the originality of your content with our advanced plagiarism detection tool.",
        "button_label": "Use Now - RepuSEO Plagiarism Checker",
        "button_url": "https://seotool-cdjzyqj4qrskqvkuahwjwm.streamlit.app"
    },
    {
        "header": "RepuSEO-Helper",
        "description": "Receive personalized SEO recommendations to improve your site's ranking and user experience.",
        "button_label": "Use Now - RepuSEO-Helper",
        "button_url": "https://seotool-qpb8fq8bygcusdsxn6pm6s.streamlit.app"
    }
]

# Loop through each tool and display its section
for tool in tools:
    display_tool_section(tool["header"], tool["description"], tool["button_label"], tool["button_url"])