import sqlite3
import pandas as pd
#Create a connection to the SQLite database
conn = sqlite3.connect("data_pipeline/books.db")
#Query1
query1 = """SELECT title,rating
            FROM books
            WHERE rating=5;"""

result1=pd.read_sql_query(query1, conn)
print("Query1: Five Star Books")
print(result1.head())

#Query2
query2 = """SELECT title,price_inr
            FROM books
            ORDER BY price_inr DESC;
            """

result2=pd.read_sql_query(query2, conn)
print("Query2: Highest Price Books")
print(result2.head(10))

#Query3
query3 = """SELECT title,category_id
            FROM books
            LIMIT 10;"""

result3=pd.read_sql_query(query3, conn)
print("Query3: First 10 Books")
print(result3)

#Query4
query4 = """SELECT DISTINCT rating
            FROM books
            ORDER BY rating DESC;
            """

result4=pd.read_sql_query(query4, conn)
print("Query4: Unique Ratings")
print(result4)

#Query5 (Join Query)
query5="""SELECT title,price_inr
            FROM books
            WHERE price_inr BETWEEN 500 AND 1500;"""
result5=pd.read_sql_query(query5, conn)
print("Query5: Books Between 500 and 1500 INR")
print(result5.head())

#Query6 (Join Query)
join_query="""SELECT b.title, c.category_name, b.rating, b.price_inr
            FROM books b
            JOIN categories c ON b.category_id = c.category_id
            ORDER BY b.rating DESC;"""

join_df=pd.read_sql_query(join_query, conn)
print("Query6:Books with Categories")
print(join_df.head(10))
 
print("All SQL Queries Executed Successfully!")

#Read categories table into pandas
categories_df=pd.read_sql_query("SELECT * FROM categories", conn)
print("Categories Table")
print(categories_df.head())
books_df=pd.read_sql("SELECT * FROM books", conn)
print("Books Table")
print(books_df.head())
#merge books and categories without using SQL JOIN
merged_df=pd.merge(books_df,categories_df,on="category_id",how="inner")
print("Pandas Merge Result")
print(merged_df[["title","category_name","rating","price_inr"]].head(10))

#Compare SQL JOIN and Pandas Merge
sql_result=join_df[["title","category_name","rating","price_inr"]].reset_index(drop=True)
pandas_result=merged_df[["title","category_name","rating","price_inr"]].sort_values(by=["title"]).reset_index(drop=True)
print("Number of rows from SQL JOIN Result:",len(sql_result))
print("Number of rows from Pandas Merge Result:",len(pandas_result))
print("Do both contain same number of rows?",len(sql_result)==len(pandas_result))

#Save important query outputs
result1.to_csv("data_pipeline/query1_five_star_books.csv",index=False)
join_df.to_csv("data_pipeline/query6_books_with_categories.csv",index=False)
print("SQL query outputs saved successfully.")
conn.close()
print("Module 1 SQL pipeline completed successfully!")