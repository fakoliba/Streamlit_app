import selenium.webdriver as webdriver  # Importing the Selenium WebDriver module
from selenium.webdriver.chrome.service import Service  # Importing the Service class to manage the ChromeDriver service
from selenium.webdriver.common.by import By  # Importing the By class for locating elements
from selenium.webdriver.common.keys import Keys  # Importing the Keys class for keyboard actions
from selenium.webdriver.chrome.options import Options  # Importing the Options class to set Chrome options
from bs4 import BeautifulSoup  # Importing BeautifulSoup for parsing HTML content
from selenium.webdriver.support.ui import WebDriverWait  # Importing WebDriverWait for explicit waits
#from dotenv import load_dotenv  # Importing load_dotenv to load environment variables from a .env file
import os  # Importing the os module for interacting with the operating system
import time  # Importing the time module for time-related functions
#load_dotenv()  # Loading environment variables from a .env file


def scrape_website(website):
    print("Launching the browser...")
    # Set the path to the chromedriver executable
    chrome_driver_path = "./chromedriver"
    options = webdriver.ChromeOptions()  # Creating an instance of ChromeOptions
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)  # Initializing the Chrome WebDriver with the specified options and service
    try:
        print("Navigating to the website...")
        driver.get(website)  # Navigating to the specified website
        print("page loaded...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scrolling to the bottom of the page using JavaScript
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )  # Waiting until the page is fully loaded
        html = driver.page_source  # Getting the page source HTML
        return html  # Returning the page source HTML
    except Exception as e:
        print(f"An error occurred: {e}")  # Printing any errors that occur
    finally:
        driver.quit()  # Quitting the WebDriver

def extract_body_content(dom_content):
    soup = BeautifulSoup(dom_content, "html.parser")  # Parsing the HTML content with BeautifulSoup
    body_content = soup.body  # Extracting the body content
    if body_content:
        return str(body_content)  # Returning the body content as a string
    return "No body content found."  # Returning a message if no body content is found

#clean the boday content
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script in soup(["script", "style"]):
        script.decompose()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content= "\n".join([line for line in cleaned_content.split("\n") if line.strip()])
    return cleaned_content
#split the DOM content
def split_dom_content(dom_content, max_chunks=7000):
    return [dom_content[i:i + max_chunks] for i in range(0, len(dom_content), max_chunks)]





