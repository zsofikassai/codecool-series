from flask import Flask, render_template, url_for, request, jsonify
from data import queries
import math
from dotenv import load_dotenv


load_dotenv()
app = Flask('codecool_series')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shows/most-rated')
def most_rated():
    return render_template('most-rated.html')

@app.route('/get-most-rated')
def get_most_rated():
    most_rated = queries.get_all_most_rated()
    for show in most_rated:
        for key in show.keys():
            if key == 'rating':
                show[key]= str(show[key])
    return jsonify(most_rated)


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
