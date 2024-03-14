import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client


# todo api key are there for testing purpose !!
def create_supabase_client():
    url = "https://seuqlacxzpyohiajgvei.supabase.co"
    key = "your_key_here"
    return create_client(url, key)


def scrape_page(page_number):
    response = requests.get(
        f"https://books.toscrape.com/catalogue/page-{page_number}.html"
    )
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "html.parser")


def extract_book_data(book):
    price = book.find("p", class_="price_color").text
    stock = book.find("p", class_="instock availability").text.strip()
    title = book.find("h3").find("a").get("title")
    rating = book.find("p", class_="star-rating").get("class")[1]
    return {"name": title, "price": price, "availability": stock, "ratings": rating}


def insert_book_to_db(supabase, book_data):
    supabase.table("books").insert(book_data).execute()


def main():
    supabase = create_supabase_client()

    for i in range(1, 51):
        soup = scrape_page(i)
        books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

        for book in books:
            book_data = extract_book_data(book)
            insert_book_to_db(supabase, book_data)


if __name__ == "__main__":
    main()
