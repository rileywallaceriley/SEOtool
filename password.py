import streamlit as st

# Define your password and the URL to redirect to
PASSWORD = 'repuseo'
REDIRECT_URL = 'https://seotool-b2twwogtwjgwvlpsuvevcu.streamlit.app'

# Redirect function using JavaScript
def redirect(url):
    js = f"window.location.href = '{url}'"  # JavaScript for redirection
    st.markdown(f'<img src onerror="{js}">', unsafe_allow_html=True)

# Main app
def main():
    st.title("Protected Access")
    
    with st.container():
        # Centering the password input by using columns
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            password_input = st.text_input("Password", type="password")

            if st.button("Login"):
                if password_input == PASSWORD:
                    redirect(REDIRECT_URL)
                else:
                    st.error("Incorrect password, please try again.")

if __name__ == "__main__":
    main()
