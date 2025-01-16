import streamlit as st
#naming the navigation panel

st.set_page_config(
    page_title=("Multi-page app"),
    page_icon="👋",
)

st.write("# Welcome to Multi-page app! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
   This Streamlit app is an AI-powered web scraper that allows users to input a URL, scrape the website's content, and parse the extracted content based on user-defined descriptions. The app consists of two main steps:

Scrape Website: Users can enter a URL and click the "Scrape Website" button to scrape the website's content. The app extracts and cleans the body content of the webpage and displays it in an expandable text box.

Parse Content: Users can describe what they want to parse from the scraped content and click the "Parse Content" button. The app uses the Ollama parsing tool to process the content based on the provided description and displays the parsed results.

The app leverages various functions to scrape, clean, and parse the website content, providing an interactive and user-friendly interface for web scraping and content analysis.
"""
)

        