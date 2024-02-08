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
Our tools are crafted to provide you with competitive insights, enhance your blog's SEO, check for plagiarism,
and assist in optimizing your content for better search engine rankings. With our suite, empower your content to reach its maximum potential.
""")

# Helper function to create a button that acts as a link
def create_link_button(label, url):
    button_html = f"""<a href="{url}" target="_blank"><button style='margin: 10px; padding: 10px; border: none; color: white; background-color: #4CAF50;'>{label}</button></a>"""
    st.markdown(button_html, unsafe_allow_html=True)

# Competitive Edge
st.markdown("### Competitive Edge")
st.write("Gain an advantage by analyzing your competitors’ SEO strategies to understand their strengths and weaknesses.")
create_link_button("Use Now - Competitive Edge", "https://seotool-mfvdnqmf32f3visjegsxho.streamlit.app")

# Blog SEO Helper
st.markdown("### Blog SEO Helper")
st.write("Optimize your blog posts with targeted keywords and content strategies to improve your visibility and engagement.")
create_link_button("Use Now - Blog SEO Helper", "https://seotool-7uqzcambnfjnuuwh9pctlr.streamlit.app")

# RepuSEO Plagiarism Checker
st.markdown("### RepuSEO Plagiarism Checker")
st.write("Ensure your content is unique and free of plagiarism, enhancing its quality and SEO performance.")
create_link_button("Use Now - RepuSEO Plagiarism Checker", "https://seotool-cdjzyqj4qrskqvkuahwjwm.streamlit.app")

# RepuSEO-Helper
st.markdown("### RepuSEO-Helper")
st.write("Get personalized recommendations to improve your website’s SEO and overall user experience.")
create_link_button("Use Now - RepuSEO-Helper", "https://seotool-qpb8fq8bygcusdsxn6pm6s.streamlit.app")