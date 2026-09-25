import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to get the category from a book page
def get_category(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text
    return category

books=[]
BASE_URL="https://books.toscrape.com/catalogue/"

#Scrape the first 5 pages of the website
for page in range(1, 6):
    url = f'https://books.toscrape.com/catalogue/page-{page}.html'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    all_books = soup.find_all('article', class_='product_pod')

    for book in all_books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        star_rating = book.find("p")["class"][1]
        availability = book.find("p", class_="instock availability").text.strip()
        relative_link=book.h3.a["href"]
        book_url=BASE_URL+relative_link.replace('../../../', '')
        category=get_category(book_url)
        books.append({
            "title": title,
            "price": price,
            "star_rating": star_rating,
            "availability": availability,
            "category": category
        })
         
#create a DataFrame
df=pd.DataFrame(books)
print("Total Books Scraped:", len(df))
#save as csv file
df.to_csv("data_pipeline/raw_books.csv", index=False)
print("raw_books.csv created successfully!")
 