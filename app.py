from flask import Flask, render_template
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import requests

app = Flask(__name__)

# Load MovieLens dataset
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

data = pd.merge(ratings, movies, on="movieId")

# Create matrix
matrix = data.pivot_table(index='userId', columns='title', values='rating').fillna(0)

similarity = cosine_similarity(matrix)
sim_df = pd.DataFrame(similarity, index=matrix.index, columns=matrix.index)

# TMDB API
API_KEY = "YOUR_API_KEY"

def get_poster(title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
    res = requests.get(url).json()
    if res['results']:
        poster = res['results'][0]['poster_path']
        if poster:
            return f"https://image.tmdb.org/t/p/w500{poster}"
    return "https://via.placeholder.com/300x450"

def get_trailer(title):
    return f"https://www.youtube.com/results?search_query={title}+trailer"

# Auto recommend (no input)
def recommend_movies():
    user = sim_df.index[0]  # first user
    similar_users = sim_df[user].sort_values(ascending=False)[1:]
    top_user = similar_users.index[0]

    user_movies = set(data[data['userId']==user]['title'])
    other_movies = set(data[data['userId']==top_user]['title'])

    recs = list(other_movies - user_movies)[:12]

    result = []
    for m in recs:
        result.append({
            "title": m,
            "poster": get_poster(m),
            "trailer": get_trailer(m)
        })
    return result

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/recommend')
def recommend():
    movies = recommend_movies()
    return render_template('recommend.html', movies=movies)

@app.route('/search', methods=['GET','POST'])
def search():
    result = []
    from flask import request
    if request.method == 'POST':
        name = request.form['movie']
        result.append({
            "title": name,
            "poster": get_poster(name),
            "trailer": get_trailer(name)
        })
    return render_template('search.html', result=result)
    
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
