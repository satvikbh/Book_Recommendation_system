from flask import Flask, render_template, request, jsonify, send_from_directory
import requests  # For fetching data from the external recommendation service
from book_recommendation import recommend_books_knn

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    password = request.form.get('password')
    if password == 'muskan':
        return render_template('carousel.html')
    else:
        return render_template('carousel.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    genre = data.get('genre')
    sub_genre = data.get('sub_genre')  # Add this field if you want to use sub-genre

    # Get recommendations using the KNN model
    recommended_books = recommend_books_knn(genre, sub_genre)
    
    # Convert the result to a list of dictionaries
    recommendations = recommended_books.to_dict(orient='records')
    
    return jsonify(recommendations)

@app.route('/external-recommend', methods=['POST'])
def external_recommend():
    data = request.get_json()
    try:
        response = requests.post('http://localhost:5000/recommend', json=data)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({'error': 'Error getting recommendations from external service'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
