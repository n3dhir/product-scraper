import requests
from bs4 import BeautifulSoup
import re
import csv

url = "https://www.jumia.com.tn/catalog/"

#how many products are displayed in a page in jumia
ProductsPerPage = 40

def scrape_products(search_query):
    page = 1
    totalPages = None
    products = []
    while True:
        # Parameters
        params = {
            'q': search_query,
            'page': page 
        }
        # Send a GET request to the URL
        response = requests.get(url, params=params)
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve page: {response.status_code}")
            continue
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'lxml')
        
        if totalPages is None:
            totalProductsDiv = soup.find("p", {'class': '-phs -gy5'})
            # Total Products Number Not Found Meaning there is no product found
            if totalProductsDiv == None:
                return []
            totalProductsText = totalProductsDiv.text
            # Use regular expression to extract numbers
            numbers = re.findall(r'\d+', totalProductsText)

            # If there are multiple numbers, take the first one
            if numbers:
                total_results = int(numbers[0])
                print("Total results:", total_results)
            else:
                print("No numeric value found.")
                return []

            totalPages = (total_results + ProductsPerPage - 1) // ProductsPerPage
            print(totalPages)

        # print(soup.prettify())
        product_items = soup.find_all("article", {'class':"prd _fb col c-prd"})
        for product_item in product_items:
            # Extracting data
            product_name = product_item.find('h3', class_='name').text.strip()
            product_price = product_item.find('div', class_='prc').text.strip()
            product_old_price = product_item.find('div', class_='old').text.strip() if product_item.find('div', class_='old') else ''
            product_discount = product_item.find('div', class_='bdg _dsct _sm').text.strip() if product_item.find('div', class_='bdg _dsct _sm') else ''
            product_rating = product_item.find('div', class_='stars _s').text.strip().split(' ')[0] if product_item.find('div', class_='stars _s') else ''
            product_reviews = product_item.find('div', class_='rev').text.strip().split('(')[1].split(')')[0] if product_item.find('div', class_='rev') else ''
            product_image = product_item.find('img', class_='img')['data-src']
            product_link = 'https://jumia.com.tn' + product_item.find('a', class_='core')['href']
            
            # Store product data in a dictionary
            product_data = {
                'Product Name': product_name,
                'Product Price': product_price,
                'Product Old Price': product_old_price,
                'Product Discount': product_discount,
                'Product Rating': product_rating,
                'Product Reviews': product_reviews,
                'Product Link': product_link,
                'Product Image': product_image,
            }
            
            # Append the product dictionary to the products list
            products.append(product_data)

        print(f"treated pages {page} / {totalPages}")
        page += 1
        if page > totalPages:
            break

    return products

# Scrape product data
scraped_data = scrape_products("velo")
# Define CSV file path
csv_file = 'jumia_scraped_products.csv'

# Define CSV fieldnames based on product data keys
fieldnames = ['Product Name', 'Product Price', 'Product Old Price', 'Product Discount', 'Product Rating', 'Product Reviews', 'Product Link', 'Product Image']

# Write to CSV
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
    
    # Write header
    writer.writeheader()
    
    # Write each product data as a row
    for product in scraped_data:
        writer.writerow(product)

print(f"Scraped data has been successfully saved to {csv_file}")