import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# Load the dataset
df = pd.read_csv('books_new.csv')

# Combine relevant text columns into a single feature
df['features'] = df['Genre'] + ' ' + df['SubGenre']

# Initialize the TF-IDF Vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the features into vectors
tfidf_matrix = vectorizer.fit_transform(df['features'])

# Initialize the KNN model
knn_model = NearestNeighbors(n_neighbors=10, metric='cosine')

# Fit the KNN model with the TF-IDF matrix
knn_model.fit(tfidf_matrix)

# Function to recommend books based on genre and sub-genre using KNN
def recommend_books_knn(genre_input, sub_genre_input):
    # Combine the genre and sub-genre input
    combined_input = genre_input + ' ' + sub_genre_input
    
    # Vectorize the input
    input_vec = vectorizer.transform([combined_input])
    
    # Find the nearest neighbors (top 10 similar books)
    distances, indices = knn_model.kneighbors(input_vec)
    
    # Get the recommended books based on the nearest neighbors
    recommended_books = df.iloc[indices[0]]
    
    return recommended_books[['Title', 'Author', 'Genre', 'SubGenre']]
