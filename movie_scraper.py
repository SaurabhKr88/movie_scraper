from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import os
import time
import re

# --- CONFIGURE CHROME OPTIONS ---
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Enable this after testing
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")

# --- LAUNCH BROWSER ---
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

# --- INPUT IMDb URL ---
movie_url = input("🔗 Enter IMDb movie URL: ").strip()
movie_url = movie_url.split('?')[0]  # Optional: remove query params

# --- VALIDATE URL ---
if "imdb.com/title/tt" not in movie_url:
    print("❌ Invalid IMDb URL format.")
    driver.quit()
    exit()



# --- OPEN DIRECT URL ---
try:
    driver.get(movie_url)
    print(f"✅ Opened: {driver.title}")
except:
    print("❌ Failed to open IMDb URL.")
    driver.quit()
    exit()

time.sleep(2)

# --- SAFE FIND FUNCTION ---
def safe_find(selector, by=By.CSS_SELECTOR):
    try:
        return wait.until(EC.presence_of_element_located((by, selector))).text
    except:
        return "N/A"

# --- FORMAT RUNTIME INTO MINUTES ---
def parse_runtime(text):
    if "h" in text or "m" in text:
        hours = re.search(r'(\d+)\s*h', text)
        minutes = re.search(r'(\d+)\s*m', text)
        total = 0
        if hours:
            total += int(hours.group(1)) * 60
        if minutes:
            total += int(minutes.group(1))
        return f"{total} mins"
    return text

# --- SCRAPE DETAILS ---
title = safe_find("h1")
release_date = safe_find("//a[contains(@href, 'releaseinfo')]", By.XPATH)
duration_raw = safe_find("li[data-testid='title-techspec_runtime'] span")
duration = parse_runtime(duration_raw)
rating = safe_find("span.sc-bde20123-1")
director = safe_find("//a[contains(@href, '/name/') and ancestor::li[contains(., 'Director')]]", By.XPATH)

# --- CAST (Top 3) ---
cast = []
try:
    cast_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-testid='title-cast-item__actor']")))
    cast = [el.text for el in cast_elements[:3]]
except:
    cast = ["N/A"]

# --- DISPLAY OUTPUT ---
print("\n🎬 Movie Info:")
print(f"Title: {title}")
print(f"Release Date: {release_date}")
print(f"Runtime: {duration}")
print(f"IMDb Rating: {rating}")
print(f"Director: {director}")
print(f"Cast: {', '.join(cast)}\n")

# --- SAVE TO EXCEL (append or create) ---
data = {
    "Title": [title],
    "Release Date": [release_date],
    "Runtime": [duration],
    "Rating": [rating],
    "Director": [director],
    "Cast": [', '.join(cast)]
}

df_new = pd.DataFrame(data)
excel_file = "movies.xlsx"

if os.path.exists(excel_file):
    df_existing = pd.read_excel(excel_file)
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
else:
    df_combined = df_new

df_combined.to_excel(excel_file, index=False)
print(f"✅ Movie info saved to '{excel_file}'")

driver.quit()
