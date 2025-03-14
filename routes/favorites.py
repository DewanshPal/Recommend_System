from flask import Blueprint, request, redirect, url_for, session, render_template
import sqlite3

favorites_bp = Blueprint('favorites', __name__)

# Add a book to favorites
@favorites_bp.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    user_id = session.get('user_id')  # Retrieve the logged-in user's ID from the session
    image_url = request.form.get('image_url')  # Get the image_url from the form
    print(image_url)
    if not user_id or not image_url:
        return "User ID or Image URL missing!", 400

    # Connect to the database
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()

    # Retrieve the book_id using the image_url
    cursor.execute("SELECT id FROM books WHERE image_url = ?", (image_url,))
    book_row = cursor.fetchone()

    if not book_row:
        conn.close()
        return "Book not found in database!", 404

    book_id = book_row[0]

    # Check if the book is already in the favorites table for this user
    cursor.execute(
        "SELECT * FROM favorites WHERE user_id = ? AND book_id = ?",
        (user_id, book_id),
    )
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return "Book already in favorites!", 400

    # Add the book to the favorites table
    cursor.execute(
        "INSERT INTO favorites (user_id, book_id) VALUES (?, ?)",
        (user_id, book_id),
    )
    conn.commit()
    conn.close()

    return "Book added to favorites successfully!", 200

# View user's favorite books
@favorites_bp.route('/favorites')
def view_favorites():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    try:
        conn = sqlite3.connect('data/database.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT books.title, books.author, books.image_url 
            FROM favorites 
            JOIN books ON favorites.book_id = books.id 
            WHERE favorites.user_id = ?""", (user_id,))
        favorites = cursor.fetchall()
        conn.close()
        return render_template('favorites.html', favorites=favorites)
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while fetching favorites."
