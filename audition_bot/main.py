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

# Scraper function
def scraper(driver):
    auditions = []
    base_url = "https://www.talenttalks.co.uk/audition/category/All/page/"
    pages = 3

    for page in range(1, pages + 1):
        driver.get(f"{base_url}{page}/")
        job_listings = driver.find_elements(By.CLASS_NAME, "white.job.media.cf")
        driver.implicitly_wait(5)

        for job in job_listings:
            title_element = job.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a")
            title = title_element.text.strip()
            link = title_element.get_attribute('href')
            
            driver.get(link)  # Open the job details page
            
            details_section = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "job-details"))
            )
            
            details_list = details_section.find_elements(By.TAG_NAME, "li")
            details_dict = {}
            for detail in details_list:
                text = detail.text.split(":")
                if len(text) == 2:
                    key, value = text[0].strip(), text[1].strip()
                    details_dict[key] = value
            
            location = details_dict.get("Location", "Not specified")
            payment = details_dict.get("Payment", "Not specified")
            job_category = details_dict.get("Job category", "Not specified")
            age = details_dict.get("Age", "Not specified")
            shoot_date = details_dict.get("Shoot Date", "Not specified")
            
            gender = extract_gender(title)
            ethnicity = extract_ethnicity(title)

            auditions.append({
                "title": title,
                "description": job.text.strip(),
                "link": link,
                "location": location,
                "payment": payment,
                "job_category": job_category,
                "age": age,
                "shoot_date": shoot_date,
                "gender": gender,
                "ethnicity": ethnicity
            })

    return auditions

def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    try:
        print("Scraping jobs...")
        auditions = scraper(driver)
        print(f"Found {len(auditions)} jobs matching criteria.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
