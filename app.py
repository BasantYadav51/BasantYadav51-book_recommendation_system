from flask import Flask, render_template, request
import pickle
import numpy as np
import os

# Load pickle files (make sure they are in the same folder as app.py)
popular_df = pickle.load(open(os.path.join(os.path.dirname(__file__), 'popular.pkl'), 'rb'))
pt = pickle.load(open(os.path.join(os.path.dirname(__file__), 'pt.pkl'), 'rb'))
books = pickle.load(open(os.path.join(os.path.dirname(__file__), 'books.pkl'), 'rb'))
similarity_scores = pickle.load(open(os.path.join(os.path.dirname(__file__), 'similarity_scores.pkl'), 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    if user_input not in pt.index:
        return render_template('recommend.html', data=[], message="Book not found in dataset.")

    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    # Use host 0.0.0.0 for Render, debug=True for local testing
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
