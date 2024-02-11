import streamlit as st

# Display the logo and video
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)
st.video('https://youtu.be/G6GIb9nwUYE?si=kUrABMKxnwtoKO-M')

# Brief overview
st.markdown("""
<div style="text-align: center;">
    <h2>Elevate Your SEO Game</h2>
    <p>Unlock the full potential of your website with our SEO Tools Suite...</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Define a function to display each tool section with centered title and description
def display_tool_section(header, description, button_label, button_url):
    with st.container():
        # Use HTML to center the header and description
        st.markdown(f"<h3 style='text-align: center;'>{header}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>{description}</p>", unsafe_allow_html=True)
        
        # Centered button with HTML
        button_html = f"""<div style="text-align: center;"><a href="{button_url}" target="_blank"><button style='margin-top: 10px; width: auto; padding: 10px 20px; border-radius: 5px; border: none; color: black; background-color: #f4a261;'>{button_label}</button></a></div>"""
        st.markdown(button_html, unsafe_allow_html=True)
        
        # Divider
        st.markdown("---")

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

# Add the SEO Analysis image at the bottom
st.image("https://i.ibb.co/pxcB74N/Analysis.png", caption="SEO Analysis", width=700)