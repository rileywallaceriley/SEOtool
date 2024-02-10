import streamlit as st

# Display the logo
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)

# Page Title
st.title('SEO Tools Suite')

# Embed YouTube Video
st.video('https://www.youtube.com/watch?v=XXXXX')

# Brief overview of your tools
st.write("""
## Elevate Your SEO Game
Unlock the full potential of your website with our SEO Tools Suite. We take the complexity out of SEO, making it accessible and actionable for everyone. Whether you're a small business owner, a solo entrepreneur, or a content creator, our tools are designed to give you clear, straightforward recommendations that drive results. Improve your search engine rankings, learn from your competition, and make SEO work for you.
""")

# Define the light orange color for the button based on your logo
light_orange = "#f4a261"  # Example hex code, adjust as needed to match your logo

# Updated function to create a button with custom color and centered text
def create_link_button(label, url, color=light_orange):
    button_html = f"""<div style="text-align: center; width: 50%; margin: 20px auto;"><a href="{url}" target="_blank"><button style='padding: 10px; border-radius: 5px; border: none; color: black; background-color: {color};'>{label}</button></a></div>"""
    st.markdown(button_html, unsafe_allow_html=True)

# Adjusted sections for centered text, constrained width, and increased spacing
def display_tool_section(header, description, button_label, button_url):
    st.markdown(f"<div style='text-align: center; width: 50%; margin: 20px auto; padding-top: 20px; padding-bottom: 20px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);'><h2 style='margin-bottom: 0;'>{header}</h2><p>{description}</p></div>", unsafe_allow_html=True)
    create_link_button(button_label, button_url)

# Use the updated function to display each tool section
display_tool_section("Competitive Edge", "Analyze and apply winning SEO strategies from your competitors directly into your campaign.", "Use Now - Competitive Edge", "https://seotool-mfvdnqmf32f3visjegsxho.streamlit.app")

display_tool_section("Blog SEO Helper", "Elevate your blog's visibility with targeted SEO strategies designed for maximum engagement.", "Use Now - Blog SEO Helper", "https://seotool-7uqzcambnfjnuuwh9pctlr.streamlit.app")

display_tool_section("RepuSEO Plagiarism Checker", "Ensure the originality of your content with our advanced plagiarism detection tool.", "Use Now - RepuSEO Plagiarism Checker", "https://seotool-cdjzyqj4qrskqvkuahwjwm.streamlit.app")

display_tool_section("RepuSEO-Helper", "Receive personalized SEO recommendations to improve your site's ranking and user experience.", "Use Now - RepuSEO-Helper", "https://seotool-qpb8fq8bygcusdsxn6pm6s.streamlit.app")