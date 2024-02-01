import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
from openai import OpenAI

# Load the API key from an environment variable
openai_api_key = os.getenv("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")
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Create an OpenAI client instance
client = OpenAI(api_key=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)

# Create an OpenAI client instance
client = OpenAI()

def get_google_search_results(query, site_url, location):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'cx': google_cse_id,
        'key': google_api_key,
        'num': 10,  # Number of results per page
        'gl': location  # Location parameter
    }
    ranking = None
    for start_index in range(1, 51, 10):  # Look through the first 50 results
        params['start'] = start_index
        response = requests.get(url, params=params)
        results = response.json()

        for i, item in enumerate(results.get('items', [])):
            if site_url in item.get('link'):
                ranking = i + 1 + start_index - 1  # Adjusting ranking based on the page
                return ranking
    return None

def scrape_content(url):
    # Ensure the URL starts with http:// or https://
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.find('main').text
    return content

def get_recommendations(content, ranking, url, engine='text-davinci-004'):
    content_preview = (content[:500] + '...') if len(content) > 500 else content
    prompt = (
        f"Website URL: {url}\n"
        f"Content Preview (first 500 characters): {content_preview}\n\n"
        "Provide a detailed on-page SEO analysis with specific tasks for improvement..."
        # [rest of your prompt]
    )

    if ranking is not None and ranking <= 50:
        prompt += f"\nThe site is currently ranked {ranking}..."
        # [rest of your prompt]

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=engine,
        )
        return chat_completion.choices[0].message['content']
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI
# [rest of your Streamlit code]
