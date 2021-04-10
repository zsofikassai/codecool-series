from flask import Flask, render_template, url_for, request, jsonify
from data import queries
import math
from dotenv import load_dotenv


load_dotenv()
app = Flask('codecool_series')

@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)

@app.route('/shows/most-rated')
def most_rated():
    headers = ['Title', 'Year', 'Runtime (min)', 'Rating', 'Genres', 'Trailer', 'Homepage']
    most_rated=queries.get_most_rated()
    return render_template('most-rated.html', shows=most_rated, headers = headers)

@app.route('/get-shows')
def get_shows():
    shows = queries.get_shows()
    return jsonify(shows)

@app.route('/design')
def design():
    return render_template('design.html')


def main():
    app.run(debug=False)


if __name__ == '__main__':
    main()
