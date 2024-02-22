import streamlit as st
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Streamlit UI setup
st.title("SEO Analysis and Optimization Tool")
st.markdown("""
This tool helps you analyze your website's top search queries from Google Search Console and provides recommendations to optimize your site's SEO.
""")

# Input for Google Search Console API credentials
site_url = st.text_input("Enter your site URL:", help="The full URL of your site as registered in Google Search Console.")
api_key = st.text_input("Enter your Google Search Console API key:", help="Your API key for accessing Google Search Console data.")

# Function to initialize the Google Search Console service
def init_search_console_service(api_key):
    credentials = Credentials(token=api_key)
    service = build('webmasters', 'v3', credentials=credentials)
    return service

# Function to fetch top search queries from Google Search Console
def fetch_top_search_queries(service, site_url):
    query_request = {
        'startDate': '2024-01-01',  # Example start date, adjust as needed
        'endDate': '2024-12-31',    # Example end date, adjust as needed
        'dimensions': ['query'],
        'rowLimit': 10  # Fetches top 10 queries
    }
    response = service.searchanalytics().query(siteUrl=site_url, body=query_request).execute()
    return response.get('rows', [])

# Display button to start analysis
if st.button("Analyze SEO"):
    if not site_url or not api_key:
        st.error("Please enter both your site URL and Google Search Console API key.")
    else:
        with st.spinner("Analyzing SEO..."):
            try:
                service = init_search_console_service(api_key)
                top_queries = fetch_top_search_queries(service, site_url)
                if top_queries:
                    st.success("Analysis complete. Here are your top search queries and recommendations:")
                    for query in top_queries:
                        keyword = query['keys'][0]
                        impressions = query['impressions']
                        clicks = query['clicks']
                        ctr = query['ctr']
                        st.write(f"Keyword: {keyword}, Impressions: {impressions}, Clicks: {clicks}, CTR: {ctr:.2%}")
                        # Here, include logic or calls to functions that generate SEO recommendations based on the query data
                else:
                    st.info("No top search queries found. Please check your inputs and try again.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("""
**Note:** Ensure your API key has the necessary permissions and the site URL matches exactly with your Google Search Console registration.
""")
