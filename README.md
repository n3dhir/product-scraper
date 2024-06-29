# Product Scraper

## Overview

This project is designed to scrape product information from e-commerce websites like Jumia and SpaceNet. It retrieves details such as product name, price, availability, and links, storing them in a CSV file for further analysis or use.

## Features

- **Scraping Capabilities**: Fetch product data from multiple pages of specified websites.
- **Data Extraction**: Extracts product name, price, availability, image link, and other relevant details.
- **CSV Export**: Saves scraped data into a CSV file for easy integration with other tools or databases.

## Setup

1. **Clone the repository**:
   
   ```sh
   https://github.com/n3dhir/product-scraper.git
   cd product-scraper
   
3. **Install dependencies**:
   
     ```sh
      pip install -r requirements.txt
     
4. **Navigate to the scraper directory**:

   Before running any script, change directory to python scrapers:
   ```sh
   cd "python scrapers"
   
5. **Run the scraper**:
     ```sh
     python jumia_scraper.py
      ```
     Replace jumia_scraper.py with the appropriate scraper script for the website you want to scrape (spacenet_scraper.py, for instance).
   
6. **Usage**:

    * Modify the scraper scripts (jumia_scraper.py, spacenet_scraper.py, etc.) to adjust scraping parameters (search queries).
   * Data is saved automatically to a CSV file. Customize the CSV formatting as needed.
     
7. **Contributing**:

   - Contributions are welcome! Please fork the repository and submit a pull request with your changes.
   
