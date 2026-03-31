from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import csv

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