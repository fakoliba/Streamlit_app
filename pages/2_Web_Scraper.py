import streamlit as st
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_ollama

# Streamlit UI
st.title("AI Web Scraper")
st.markdown(
    """
   This Streamlit app is an AI-powered web scraper that allows users to input a URL, scrape the website's content, and parse the extracted content based on user-defined descriptions. The app consists of two main steps:

Scrape Website: Users can enter a URL and click the "Scrape Website" button to scrape the website's content. The app extracts and cleans the body content of the webpage and displays it in an expandable text box.

Parse Content: Users can describe what they want to parse from the scraped content and click the "Parse Content" button. The app uses the Ollama parsing tool to process the content based on the provided description and displays the parsed results.

The app leverages various functions to scrape, clean, and parse the website content, providing an interactive and user-friendly interface for web scraping and content analysis.
"""
)

def scrape_website_step(url):
    if st.button("Scrape Website"):
        if url:
            st.write("Scraping the website...")

            try:
                # Scrape the website
                dom_content = scrape_website(url)
                if dom_content is None:
                    st.error("Failed to scrape the website. Please check the URL and try again.")
                    return

                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)

                # Store the DOM content in Streamlit session state
                st.session_state.dom_content = cleaned_content

                # Display the DOM content in an expandable text box
                with st.expander("View DOM Content"):
                    st.text_area("DOM Content", cleaned_content, height=300)
            except Exception as e:
                st.error(f"An error occurred while scraping the website: {e}")

def parse_dom_content_step():
    if "dom_content" in st.session_state:
        parse_description = st.text_area("Describe what you want to parse")

        if st.button("Parse Content"):
            if parse_description:
                st.write("Parsing the content...")
                try:
                    # Parse the content with Ollama
                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    result = parse_with_ollama(dom_chunks, parse_description)
                    st.write(result)
                except Exception as e:
                    st.error(f"An error occurred while parsing the content: {e}")

# Main app logic
url = st.text_input("Enter URL")
scrape_website_step(url)
parse_dom_content_step()