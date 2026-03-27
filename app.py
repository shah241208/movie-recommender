from flask import Flask, render_template

app = Flask(__name__)

# Dummy data (replace with your ML model output)
movies = [
    {"title": "Movie 1", "poster": "https://via.placeholder.com/200", "trailer": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
    {"title": "Movie 2", "poster": "https://via.placeholder.com/200", "trailer": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
    {"title": "Movie 3", "poster": "https://via.placeholder.com/200", "trailer": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
    {"title": "Movie 4", "poster": "https://via.placeholder.com/200", "trailer": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
    {"title": "Movie 5", "poster": "https://via.placeholder.com/200", "trailer": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
]

@app.route('/')
def home():
    return render_template(
        'recommend.html',
        hero=movies[0],
        trending=movies,
        action=movies,
        comedy=movies
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
