# 🎬 IMDb Movie Scraper

A Python-based IMDb movie scraper that uses Selenium to extract key information from any IMDb movie page and save it to an Excel file.

## ✅ Features

- Extracts:
  - Movie Title
  - Release Date
  - Runtime (formatted in minutes)
  - IMDb Rating
  - Director Name
  - Top 3 Cast Members
- Saves data into an `Excel` file (`movies.xlsx`)
- Supports input of any direct IMDb movie URL
- Automatically appends new entries without overwriting existing data

---

## 🛠️ Tech Stack

- Python 3
- Selenium WebDriver
- WebDriver Manager
- pandas
- re (for regex formatting)
- IMDb.com as the data source

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/movie_scraper.git
cd movie_scraper
