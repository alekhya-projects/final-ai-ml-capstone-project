import sqlite3
import pandas as pd

#load cleaned data
df=pd.read_csv("data_pipeline/cleaned_books.csv")

#create a database connection
conn=sqlite3.connect("data_pipeline/books.db")
cursor=conn.cursor()

#categories table
cursor.execute("""CREATE TABLE IF NOT EXISTS categories (
                    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_name TEXT UNIQUE )""")

#Books table
cursor.execute("""CREATE TABLE IF NOT EXISTS books (
                    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    category_id INTEGER,
                    price_gbp REAL,
                    price_inr REAL,
                    rating INTEGER,
                    in_stock INTEGER,
                    FOREIGN KEY (category_id) REFERENCES categories (category_id)
                )""")

#Insert categories into the categories table
categories=df["category"].unique()

for category in categories:
    cursor.execute("INSERT OR IGNORE INTO categories (category_name) VALUES (?)", (category,))

#Read the categories table to get category_id
cursor.execute("SELECT category_id, category_name FROM categories")
category_dict={
    name:cid for cid, name in cursor.fetchall()
}

#Insert books into the books table
for _, row in df.iterrows():
    cursor.execute("""INSERT INTO books (title, category_id, price_gbp, price_inr, rating, in_stock)
                      VALUES (?, ?, ?, ?, ?, ?)""",
                   (row["title"], category_dict[row["category"]], row["price_gbp"], row["price_inr"], row["rating"], int(row["in_stock"])))
conn.commit()
conn.close()
print("books.db created successfully!")
