from flask import Flask, render_template, request , redirect , url_for , session
import pickle
from flask_bcrypt import Bcrypt
import sqlite3
import numpy as np
from routes.favorites import favorites_bp


# Load pickled data
popular_books = pickle.load(open('data/popular.pkl', 'rb'))
pivot_table = pickle.load(open('data/pt.pkl', 'rb'))
books = pickle.load(open('data/books.pkl', 'rb'))
similarity_scores = pickle.load(open('data/similarity_scores.pkl', 'rb'))


app = Flask(__name__)


# Replace with a strong secret key
app.secret_key = 'your_secret_key'
bcrypt = Bcrypt(app)


# Register the blueprint
app.register_blueprint(favorites_bp)


# SQLite connection function
def get_db_connection():
    conn = sqlite3.connect('data/database.db')
    conn.row_factory = sqlite3.Row
    return conn


#Allow users to create an account. Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            return redirect('/login')
        except sqlite3.IntegrityError:
            return "Username already exists. Try another.", 400
    return render_template('register.html')


#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect('/')
        return "Invalid username or password.", 401
    return render_template('login.html')


#logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect('/')


@app.route('/')
def index():
    conn = get_db_connection()
    genres = conn.execute(
        "SELECT DISTINCT genre FROM books WHERE genre IS NOT NULL AND genre != 'Uncategorized'").fetchall()
    conn.close()
    return render_template(
        'index.html',
        book_name=list(popular_books['title'].values),
        author=list(popular_books['author'].values),
        image_url=list(popular_books['image_url'].values),
        votes=list(popular_books['num_ratings'].values),
        avg_rating=np.round(list(popular_books['avg_rating'].values), 1),
        genres=genres
    )

@app.route('/recommend' , methods=['GET'])
def recommend_ui():
    conn = get_db_connection()

    # Fetch distinct genres for the dropdown
    genres = conn.execute(
        "SELECT DISTINCT genre FROM books WHERE genre IS NOT NULL AND genre != 'Uncategorized'").fetchall()
    conn.close()
    # Fallback for book_titles if pivot_table is None
    book_titles = list(pivot_table.index) if pivot_table is not None else []
    return render_template('recommend.html', book_titles=book_titles, genres=genres)

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    if user_input not in pivot_table.index:
        # Fallback: Redirect to recommend page with an error message
        return redirect(url_for('recommend_ui'))

    try:
        index = np.where(pivot_table.index == user_input)[0][0]
        similar_items = sorted(
            list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True
        )[1:11]

        data = []
        for i in similar_items:
            temp_df = books[books['title'] == pivot_table.index[i[0]]].drop_duplicates('title')
            item = [
                temp_df['title'].values[0],
                temp_df['author'].values[0],
                temp_df['image_url'].values[0],
            ]
            data.append(item)

        # if data is not present then return popular books

        return render_template('recommend.html', data=data, book_titles=list(pivot_table.index))
    except Exception as e:
        # Log and display a generic error with fallback
        print(f"Error occurred: {e}")
        return redirect(url_for('recommend_ui'))


@app.route('/filter_by_genre', methods=['GET'])
def filter_by_genre():
    genre = request.args.get('genre')
    conn = get_db_connection()

    # Fetch books of the selected genre
    books = conn.execute("SELECT * FROM books WHERE genre = ?", (genre,)).fetchall() if genre else []

    # Fetch distinct genres for the dropdown
    genres = conn.execute(
        "SELECT DISTINCT genre FROM books WHERE genre IS NOT NULL AND genre != 'Uncategorized'").fetchall()
    conn.close()

    return render_template('genre_books.html', books=books, genres=genres, selected_genre=genre)

if __name__ == '__main__':
    app.run(debug=True)

