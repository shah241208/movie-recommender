from flask import Flask, render_template, request, redirect
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

# TMDB API (Replace with your key)
API_KEY = "YOUR_API_KEY"

def get_poster(title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
        res = requests.get(url).json()
        if res['results']:
            poster = res['results'][0]['poster_path']
            if poster:
                return f"https://image.tmdb.org/t/p/w500{poster}"
    except:
        pass
    return "https://via.placeholder.com/300x450"

def get_trailer(title):
    return f"https://www.youtube.com/results?search_query={title}+trailer"

# Auto recommend (no input)
def recommend_movies():
    user = sim_df.index[0]
    similar_users = sim_df[user].sort_values(ascending=False)[1:]
    top_user = similar_users.index[0]

    user_movies = set(data[data['userId'] == user]['title'])
    other_movies = set(data[data['userId'] == top_user]['title'])

    recs = list(other_movies - user_movies)[:12]

    result = []
    for m in recs:
        result.append({
            "title": m,
            "poster": get_poster(m),
            "trailer": get_trailer(m)
        })
    return result

# 🔐 LOGIN (FIXED)
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return redirect('/home')
    return render_template('login.html')

# 🏠 HOME
@app.route('/home')
def home():
    return render_template('home.html')

# 🎬 RECOMMEND (AUTO)
@app.route('/recommend')
def recommend():
    movies = recommend_movies()
    return render_template('recommend.html', movies=movies)

# 🔍 SEARCH
@app.route('/search', methods=['GET','POST'])
def search():
    result = []
    if request.method == 'POST':
        name = request.form['movie']
        result.append({
            "title": name,
            "poster": get_poster(name),
            "trailer": get_trailer(name)
        })
    return render_template('search.html', result=result)

# ℹ️ ABOUT
@app.route('/about')
def about():
    return render_template('about.html')

# 🚀 RUN (RENDER READY)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
