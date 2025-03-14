import sqlite3

# Connect to the database
conn = sqlite3.connect('data/database.db')
cursor = conn.cursor()

# Define genre keywords
genre_keywords = {
    "Fantasy": [
        "magic", "dragon", "wizard", "fairy", "kingdom", "sorcery", "elf",
        "dwarf", "spell", "mythical", "witch", "warlock", "unicorn",
        "quest", "tale", "epic"
    ],
    "Science Fiction": [
        "space", "alien", "robot", "cyborg", "future", "galaxy", "time travel",
        "dystopia", "utopia", "artificial intelligence", "sci-fi", "extraterrestrial",
        "warp", "quantum", "terraform", "clone", "spaceship"
    ],
    "Mystery": [
        "detective", "murder", "crime", "investigation", "thriller", "case",
        "sleuth", "whodunit", "suspense", "clue", "forensic", "heist",
        "spy", "law", "homicide", "missing", "puzzle", "conspiracy"
    ],
    "Romance": [
        "love", "romance", "heart", "passion", "affair", "relationship",
        "kiss", "soulmate", "wedding", "desire", "dating", "courtship",
        "honeymoon", "crush", "valentine", "attraction"
    ],
    "Non-Fiction": [
        "biography", "memoir", "autobiography", "history", "self-help",
        "guide", "philosophy", "science", "psychology", "how to", "manual",
        "leadership", "business", "success", "health", "diet", "cooking",
        "travel", "education", "essay"
    ],
    "Horror": [
        "ghost", "vampire", "zombie", "haunted", "monster", "gothic",
        "creepy", "supernatural", "nightmare", "demon", "occult", "evil",
        "curse", "possession", "satan", "fear", "darkness", "witchcraft",
        "serial killer", "blood", "gruesome"
    ],
    "Historical Fiction": [
        "historical", "war", "empire", "victorian", "medieval", "ancient",
        "renaissance", "royalty", "colonial", "battle", "dynasty",
        "crusade", "revolution", "aristocracy", "castle"
    ],
    "Adventure": [
        "adventure", "explore", "journey", "voyage", "treasure",
        "expedition", "danger", "wild", "survival", "island", "jungle",
        "desert", "quest", "mountain", "pirate", "exploration"
    ],
    "Young Adult (YA)": [
        "teen", "high school", "coming of age", "first love", "bully",
        "friendship", "diary", "youth", "rebellion", "school", "crush",
        "prom", "summer", "adolescence", "identity", "peer"
    ],
    "Children's Literature": [
        "children", "kids", "fairy tale", "storybook", "bedtime",
        "nursery", "picture book", "magic", "animal", "adventure",
        "playful", "illustrated", "princess", "hero", "cartoon",
        "learning"
    ],
    "Self-Help": [
        "self-help", "motivation", "productivity", "habits", "success",
        "confidence", "growth", "mindset", "positivity", "well-being",
        "goal", "career", "inspiration", "mindfulness", "discipline",
        "life improvement"
    ],
    "Biography/Autobiography": [
        "biography", "autobiography", "memoir", "diary", "life story",
        "inspirational", "political leader", "scientist", "innovator",
        "historical figure", "athlete", "celebrity", "philanthropist",
        "activist", "pioneer", "revolutionary"
    ],
    "Thriller": [
        "thriller", "suspense", "chase", "stalker", "kidnap", "hostage",
        "plot", "twist", "psychological", "action-packed", "betrayal",
        "revenge", "espionage", "conspiracy", "manhunt", "adrenaline"
    ],
    "Classics": [
        "classic", "timeless", "literature", "masterpiece", "19th century",
        "18th century", "victorian", "renaissance", "aristocracy",
        "famous authors", "award-winning", "novel", "poetry", "epic",
        "tragedy", "comedy"
    ]
}


# Function to determine the genre based on the title
def determine_genre(title):
    title_lower = title.lower()
    for genre, keywords in genre_keywords.items():
        if any(keyword in title_lower for keyword in keywords):
            return genre
    return "Uncategorized"  # Default if no keywords match


# Fetch books without genres
cursor.execute("SELECT id, title FROM books WHERE genre IS NULL")
books = cursor.fetchall()

# Assign genres to books
for book_id, title in books:
    genre = determine_genre(title)
    cursor.execute("UPDATE books SET genre = ? WHERE id = ?", (genre, book_id))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Genres have been assigned based on book titles.")
