import sqlite3
import pickle


books = pickle.load(open('data/books.pkl', 'rb'))

# print(books.columns)

#Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('data/database.db')
cursor = conn.cursor()

# SQL query to insert books
insert_query = "INSERT INTO books (title, author, image_url) VALUES (?, ?, ?)"

# Insert data from the pickle file
try:
    for _, row in books.iterrows():
        cursor.execute(insert_query, (row['title'], row['author'], row['image_url']))
    conn.commit()
    print(f"Successfully inserted {cursor.rowcount} books into the 'books' table.")
except Exception as e:
    print(f"Error occurred: {e}")
finally:
    # Close the connection
    conn.close()
