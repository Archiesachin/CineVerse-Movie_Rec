import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender:
    def __init__(self, matrix_path, metadata_path):
        self.matrix_path = matrix_path
        self.metadata_path = metadata_path
        self.svd = TruncatedSVD(n_components=100, random_state=42)
        self.user_similarity_threshold = 0.3

    def load_data(self):
        try:
            # Load existing user-item matrix
            self.matrix = pd.read_csv(self.matrix_path)
        except FileNotFoundError:
            print("No recommendations available if matrix file doesn't exist")
            return False
        return True

    def preprocess_data(self):
        if not self.load_data():
            return False

        if user_id not in self.matrix['userId'].unique():
            print("No recommendations available for new user")
            return False

        # Pivot the data to create user-item matrix
        self.pivot_matrix = self.matrix.pivot(index='userId', columns='movieId', values='rating').fillna(0)

        # Load movies metadata
        self.movies_metadata = pd.read_csv(self.metadata_path, low_memory=False)

        # Convert the 'id' column to int64 data type
        self.movies_metadata['id'] = pd.to_numeric(self.movies_metadata['id'], errors='coerce')

        return True

    def fit_svd(self):
        if not self.preprocess_data():
            return False
        # Fit SVD to the existing user-item matrix
        self.svd.fit(self.pivot_matrix)
        return True

    def recommend_movies(self, user_id, n=10):
        if not self.fit_svd():
            return []

        # Get user index
        user_index = self.pivot_matrix.index.get_loc(user_id)

        # Compute latent user-item matrix
        latent_matrix = self.svd.transform(self.pivot_matrix)

        # Calculate similarity between users
        user_similarity = cosine_similarity(latent_matrix)

        # Get similar users
        similar_users = user_similarity[user_similarity[:, user_index] > self.user_similarity_threshold]

        # Calculate predicted ratings for unrated movies
        predicted_ratings = np.dot(latent_matrix[user_index], latent_matrix.T)

        # Filter out movies already watched by the user
        unwatched_movies_indices = np.where(self.pivot_matrix.iloc[user_index] == 0)[0]

        # Ensure unwatched_movies_indices are valid
        valid_indices = np.intersect1d(unwatched_movies_indices, np.arange(len(predicted_ratings)))

        if len(valid_indices) == 0:
            print("No recommendations available")
            return []

        # Get predicted ratings for unwatched movies
        unwatched_movies_predicted_ratings = predicted_ratings[valid_indices]

        # Get indices of top recommended movies
        top_movie_indices = valid_indices[np.argsort(unwatched_movies_predicted_ratings)[-n:]]

        # Get titles of top recommended movies
        top_movies = self.movies_metadata.iloc[top_movie_indices]['title']

        return top_movies.tolist()


# Example usage:
matrix_path = "datasets/ratings_small.csv"
metadata_path = "datasets/movie_metadata.csv"
user_id = 25

recommender = MovieRecommender(matrix_path, metadata_path)
recommended_movies = recommender.recommend_movies(user_id)
print(recommended_movies)