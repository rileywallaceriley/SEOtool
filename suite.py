import streamlit as st


# Display the logo and video
logo_url = 'https://i.ibb.co/VvYtGFg/REPU-11.png'
st.image(logo_url, width=200)
st.video('https://youtu.be/G6GIb9nwUYE?si=kUrABMKxnwtoKO-M')

# Brief overview
st.markdown("""
<div style="text-align: center;">
<h2>SEO? Easy peasy with RepuRocket!</h2>

<p>There are close to 200 factors that Google considers when ranking websites in its search. But, did you know that over 60% of marketers agree that on-page content development is the most effective SEO tactic?</p> 

<p>It's true! <strong>Better content, keywords and meta</strong> can make a world of difference, once you have a clear strategy. RepuRocket can help you create and carry out that strategy; think of us as your friendly neighbourhood SEO buddy, here to help you climb those Google ranks without the headache.</p>

<p>With a few simple clicks, you can discover the right keywords, peek at what your competitors are up to, and get easy tips that <em>actually</em> work.</p>

<h3>More results, without the big-agency price tag.</h3>

<p>No more SEO jargon or confusion. <strong>Just clear, straightforward advice to boost your site</strong>. Join RepuRocket, and let’s make your website shine together.</p>
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
        "header": "RepuSEO-Helper",
        "description": "Receive personalized SEO recommendations to improve your site's ranking and user experience.",
        "button_label": "Use Now - RepuSEO-Helper",
        "button_url": "https://seotool-qpb8fq8bygcusdsxn6pm6s.streamlit.app"
    },
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
    
]

# Loop through each tool and display its section
for tool in tools:
    display_tool_section(tool["header"], tool["description"], tool["button_label"], tool["button_url"])

# Attempt to make the bottom image responsive
left_column, image_column, right_column = st.columns([1, 10, 1])
with image_column:
    st.image("https://i.ibb.co/pxcB74N/Analysis.png")