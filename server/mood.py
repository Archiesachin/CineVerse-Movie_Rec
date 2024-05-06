import pandas as pd

def load_dataset(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
        return None
    except Exception as e:
        print("An error occurred while loading the dataset:", e)
        return None

def get_release_year(release_date):
    try:
        return pd.to_datetime(release_date).year
    except:
        return None

def get_movie_recommendations(dataset, emotion, preferred_language):
    # Map emotion to genre
    emotion_to_genre = {
        "Happy" : "Horror",
        "Sad" : "Drama",
        "Satisfied" : "Animation",
        "Angry" : "Romance",
        "Peaceful" : "Fantasy",
        "Fearful" : "Adventure",
        "Excited" : "Crime",
        "Depressed" : "Comedy",
        "Content" : "Mystery",
        "Sorrowful" : "Action"
        # Add more mappings as needed
    }

    genre = emotion_to_genre.get(emotion)

    if genre:
        # Filter dataset by genre
        genre_movies = dataset[dataset['genres'].str.contains(genre, case=False)]

        # Filter by preferred language
        if preferred_language:
            genre_movies = genre_movies[genre_movies['original_language'] == preferred_language]

       

        # Sort by vote_average in descending order to get highest-rated movies first
        genre_movies_sorted = genre_movies.sort_values(by='vote_average', ascending=False)

        # Get the top 5 movies with highest ratings
        top_recommendations = genre_movies_sorted.head(5)[['original_title', 'release_date', 'overview', 'vote_average']].values.tolist()

        return top_recommendations
    else:
        print("Sorry, we don't have recommendations for that emotion.")
        return []

def main():
    file_path = 'datasets\movie_metadata.csv'  # Adjust the file path as needed
    dataset = load_dataset(file_path)

    if dataset is not None:
        # Ask for user preferences
        emotion = input("How are you feeling today? ").capitalize()
        preferred_language = input("What language do you prefer? ")
       

        # Get movie recommendations
        recommended_movies = get_movie_recommendations(dataset, emotion, preferred_language)

        # Print recommendations
        print(f"\nTop 5 recommended movies for {emotion}:")
        if recommended_movies:
            for idx, movie in enumerate(recommended_movies, start=1):
                title, release_date, overview, rating = movie
                release_year = get_release_year(release_date)
                print(f"{idx}. {title} ({release_year}) - Rating: {rating}\n   {overview}\n")
        else:
            print("No recommendations found for this mood.")

