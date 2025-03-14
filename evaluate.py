import numpy as np
import pandas as pd
import pickle

# Load the dataset
books = pickle.load(open('data/books.pkl', 'rb'))
pivot_table = pickle.load(open('data/pt.pkl', 'rb'))  # User-book interaction matrix
similarity_scores = pickle.load(open('data/similarity_scores.pkl', 'rb'))  # Precomputed similarity matrix

# Sample ground truth (actual books a user interacted with)
user_actual_books = {
    "Harry Potter and the Sorcerer's Stone": ["Harry Potter and the Chamber of Secrets (Book 2)", "Harry Potter and the Prisoner of Azkaban (Book 3)", "The Chronicles of Narnia","Harry Potter and the Goblet of Fire (Book 4)","Jacob Have I Loved","Harry Potter and the Order of the Phoenix (Book 5)","The Mists of Avalon","The Bonesetter's Daughter","The Tao of Pooh","G Is for Gumshoe (Kinsey Millhone Mysteries (Paperback))","Harry Potter and the Sorcerer's Stone (Harry Potter (Paperback))"],

    "The Great Gatsby": ["To Kill a Mockingbird", "Catcher in the Rye", "Of Mice and Men"]
}

# Function to get recommendations for a given book
def get_recommendations(book_title, k=10):
    if book_title not in pivot_table.index:
        return []
    
    index = np.where(pivot_table.index == book_title)[0][0]
    similar_books = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:k+1]
    
    recommended_books = [pivot_table.index[i[0]] for i in similar_books]
    return recommended_books

# Function to compute Precision@K
def precision_at_k(book_title, k=10):
    recommended_books = get_recommendations(book_title, k)
    print(recommended_books)
    relevant_books = set(user_actual_books.get(book_title, []))
    # print(relevant_books)
    
    if not relevant_books:
        return 0  # No ground truth available
    
    relevant_count = sum(1 for book in recommended_books if book in relevant_books)
    return relevant_count / k

# Function to compute Average Precision for a given book
def average_precision(book_title, k=10):
    recommended_books = get_recommendations(book_title, k)
    relevant_books = set(user_actual_books.get(book_title, []))

    if not relevant_books:
        return 0  # No ground truth available

    score = 0
    num_relevant = 0

    for i, book in enumerate(recommended_books):
        if book in relevant_books:
            num_relevant += 1
            precision_at_i = num_relevant / (i + 1)
            score += precision_at_i

    return score / len(relevant_books) if relevant_books else 0

# Function to compute Mean Average Precision (MAP)
def mean_average_precision(k=10):
    total_ap = 0
    valid_cases = 0

    for book_title in user_actual_books.keys():
        ap = average_precision(book_title, k)
        if ap > 0:
            total_ap += ap
            valid_cases += 1

    return total_ap / valid_cases if valid_cases > 0 else 0

# Running the evaluation
k = 10
precision_scores = {book: precision_at_k(book, k) for book in user_actual_books.keys()}
map_score = mean_average_precision(k)

# Display results
print("Precision@K for each book:")
for book, score in precision_scores.items():
    print(f"{book}: {score:.2f}")

print(f"\nMean Average Precision (MAP): {map_score:.2f}")
