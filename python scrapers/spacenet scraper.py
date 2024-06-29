import requests
from bs4 import BeautifulSoup
import csv

url = "https://spacenet.tn/recherche"

def scrape_products(search_query):
    page = 1
    totalPages = None
    products = []
    while True:
        # Parameters
        params = {
            'search_query': search_query,
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
            totalProductsText = soup.find("div", {'class': 'total-products'}).find("p").text
            # Split the string by spaces
            parts = totalProductsText.split()

            # Retrieve the numbers
            range_numbers = parts[1]  # '61-80'
            total_products = parts[3]  # '670'

            # Extract the numeric values
            start_number, end_number = range_numbers.split('-')
            start_number = int(start_number)
            end_number = int(end_number)
            total_products_number = int(total_products)

            totalPages = (total_products_number + end_number - start_number) // (end_number - start_number + 1)

        # print(soup.prettify())
        product_items = soup.find_all("div", {'class':"field-product-item item-inner product-miniature js-product-miniature"})
        for product_item in product_items:
            # Extract product details
            product_name = product_item.find('h2', class_='product_name').text.strip()
            product_price = product_item.find('span', class_='price').text.strip()
            product_link = product_item.find('a', href=True)['href']
            product_image = product_item.find('img', class_='img-responsive product_image')['src']
            product_ref = product_item.find('div', class_='product-reference').find('span').text.strip()
            
            # Check stock status
            stock_status = product_item.find('span', class_='product-flag out_of_stock nn0')
            stock_status = 'Out of stock' if stock_status else 'In stock'
            
            # Store product data in a dictionary
            product_data = {
                'Product Name': product_name,
                'Product Price': product_price,
                'Product Link': product_link,
                'Product Image': product_image,
                'Product Reference': product_ref,
                'Stock Status': stock_status
            }
            
            # Append the product dictionary to the products list
            products.append(product_data)

        print(f"treated pages {page} / {totalPages}")
        page += 1
        if page > totalPages:
            break

    return products

# Scrape product data
scraped_data = scrape_products("pc")

# Define CSV file path
csv_file = 'spacenet_scraped_products.csv'

# Define CSV fieldnames based on product data keys
fieldnames = ['Product Name', 'Product Price', 'Product Link', 'Product Image', 'Product Reference', 'Stock Status']

# Write to CSV
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
    
    # Write header
    writer.writeheader()
    
    # Write each product data as a row
    for product in scraped_data:
        writer.writerow(product)

print(f"Scraped data has been successfully saved to {csv_file}")