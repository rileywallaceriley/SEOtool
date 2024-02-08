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

# Function to create a button with custom color
def create_link_button(label, url, color=light_orange):
    button_html = f"""<a href="{url}" target="_blank"><button style='margin: 10px; padding: 10px; border-radius: 5px; border: none; color: black; background-color: {color};'>{label}</button></a>"""
    st.markdown(button_html, unsafe_allow_html=True)

# Competitive Edge
st.subheader("Competitive Edge")
st.write("Analyze and apply winning SEO strategies from your competitors directly into your campaign.")
create_link_button("Use Now - Competitive Edge", "https://seotool-mfvdnqmf32f3visjegsxho.streamlit.app")

# Blog SEO Helper
st.subheader("Blog SEO Helper")
st.write("Elevate your blog's visibility with targeted SEO strategies designed for maximum engagement.")
create_link_button("Use Now - Blog SEO Helper", "https://seotool-7uqzcambnfjnuuwh9pctlr.streamlit.app")

# RepuSEO Plagiarism Checker
st.subheader("RepuSEO Plagiarism Checker")
st.write("Ensure the originality of your content with our advanced plagiarism detection tool.")
create_link_button("Use Now - RepuSEO Plagiarism Checker", "https://seotool-cdjzyqj4qrskqvkuahwjwm.streamlit.app")

# RepuSEO-Helper
st.subheader("RepuSEO-Helper")
st.write("Receive personalized SEO recommendations to improve your site's ranking and user experience.")
create_link_button("Use Now - RepuSEO-Helper", "https://seotool-qpb8fq8bygcusdsxn6pm6s.streamlit.app")