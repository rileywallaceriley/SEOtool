import streamlit as st

# Define your password here
PASSWORD = 'repuseo'
REDIRECT_URL = 'https://seotool-b2twwogtwjgwvlpsuvevcu.streamlit.app'

# Function to redirect to the specified URL
def redirect(url):
    js = f"<script>window.location.href='{url}';</script>"
    st.markdown(js, unsafe_allow_html=True)

# Function to check password
def check_password(password):
    if password == PASSWORD:
        redirect(REDIRECT_URL)
    else:
        st.error("Incorrect password, please try again.")

# Use columns to horizontally center the login box
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Use a container to add some vertical space before the login box
    with st.container():
        # Calculate the space needed to center the content vertically
        _, row2, _ = st.columns([1, 6, 1])

        with row2:
            st.write("")  # This could be used to add vertical space

        st.title("Protected Access")

        # Collect password input
        password_input = st.text_input("Password", type="password", key="password")

        # Orange login button
        if st.button("Login", key="login"):
            check_password(password_input)

# Note: Streamlit doesn't currently support precise vertical centering out of the box,
# so this approach uses spacers and relative sizing to approximate it.
