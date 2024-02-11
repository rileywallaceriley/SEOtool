import streamlit as st

PASSWORD = 'repuseo'

def show_protected_content():
    """
    Function to show the protected content or display a link to redirect.
    """
    # Display the content or redirect link
    st.markdown("### Access Granted")
    st.markdown("Click the link below to proceed:")
    st.markdown(f"[Go to Dashboard](https://seotool-b2twwogtwjgwvlpsuvevcu.streamlit.app/)", unsafe_allow_html=True)

def main():
    st.title("Protected Access")

    password_input = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if password_input == PASSWORD:
            show_protected_content()
        else:
            st.error("Incorrect password, please try again.")

if __name__ == "__main__":
    main()
