import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_listing_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []

    for product in soup.find_all('div', {'data-component-type': 's-search-result'}):
        try:
            product_url = "https://www.amazon.in" + product.find('a', {'class': 'a-link-normal'})['href']
            product_name = product.find('span', {'class': 'a-size-medium'}).text.strip()
            product_price = product.find('span', {'class': 'a-offscreen'}).text.strip()
            product_rating = product.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]
            product_num_reviews = product.find('span', {'class': 'a-size-base'}).text.strip().replace(',', '')

            products.append({
                'Product URL': product_url,
                'Product Name': product_name,
                'Product Price': product_price,
                'Rating': product_rating,
                'Number of Reviews': product_num_reviews
            })
        except:
            continue
    print("------------------product---------------------------------")
    print(products)
    return products

def scrape_product_details(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    print(response, url,'-----------response-------url--------')
    # soup = BeautifulSoup(response.content, "lxml")
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        # product_asin = soup.find('th', string='ASIN').find_next('td').text.strip()
        # product_description = soup.find('div', {'id': 'productDescription'}).text.strip()
        # product_manufacturer = soup.find('a', {'id': 'bylineInfo'}).text.strip()

                # ASIN code
        product_asin = soup.select_one("div[data-asin]")["data-asin"]

        # Manufacturer
        manufacturer_tag = soup.find("a", {"id": "bylineInfo"})
        product_manufacturer = manufacturer_tag.text.strip() if manufacturer_tag else None

        # Product description
        description_tag = soup.find("span", {"id": "productTitle"})
        product_description = description_tag.text.strip() if description_tag else None

        product_details = {
            'ASIN': product_asin,
            'Description': product_description,
            'Manufacturer': product_manufacturer
        }
        print("------------------product deatail---------------------------------")
        # print(product_details)

        return product_details
    except:
        print("------------------No product deatail---------------------------------")
        return None

def main():
    base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
    pages_to_scrape = 20
    products_data = []
    print(products_data)
    # Scrape product listing pages
    # for page_number in range(1, pages_to_scrape + 1):
    page_number=1
    while len(products_data)<200:
        url = base_url + str(page_number)
        page_number+=1
        print(url,'---------------url---------------------')
        products_data.extend(scrape_product_listing_page(url))

    # Scrape individual product URLs for additional information
    for product_data in products_data:
        product_url = product_data['Product URL']
        product_details = scrape_product_details(product_url)
        if product_details:
            product_data.update(product_details)

    # Export data to CSV
    with open('amazon_products_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'ASIN', 'Description', 'Manufacturer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products_data)

if __name__ == "__main__":
    main()
