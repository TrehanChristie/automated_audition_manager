from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import csv

# Helper functions for data extraction
def extract_age(from_text):
    """Extract age"""
    age_match = re.search(r'aged (\d{1,2}-\d{1,2})', from_text, re.IGNORECASE)
    if age_match:
        return age_match.group(1)
    age_match = re.search(r'aged (\d{1,2}\+)', from_text, re.IGNORECASE)
    if age_match:
        return age_match.group(1)
    return None

def extract_gender(from_text):
    """Extract gender"""
    from_text = from_text.lower()

    pairs = ["boy & girl", "boy and girl", "boys & girls", "boys and girls", "female & male", "female and male",   
             "girl & boy", "girl and boy", "girls & boys", "girls and boys", "male & female", "male and female",   
             "man & woman", "man and woman", "men & women", "women & men", "woman & man", "woman and man"]
    
    if any(pair in from_text for pair in pairs):
        return "Not specified"
    
    elif any(word in from_text for word in ["female", "females", "woman", "women", "girl", "girls"]):
        return "Female"
    
    elif any(word in from_text for word in ["male", "males", "man", "men", "boy", "boys"]):
        return "Male"
    
    return "Not specified"

def extract_ethnicity(from_text):
    """Extract ethnicity/background"""
    ethnicity_keywords = ["White", "Asian", "Indian", "Black", "Mixed race", "all background"]
    ethnicity = next((word for word in ethnicity_keywords if word.lower() in from_text.lower()), "Not specified")
    return ethnicity