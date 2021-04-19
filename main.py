from flask import Flask, render_template, url_for, jsonify
from data import queries
import math
from dotenv import load_dotenv

load_dotenv()
app = Flask('codecool_series')

@app.route('/')
def index():

    return render_template('main.html')

@app.route('/get-shows')
def get_shows():
    shows = queries.actors_most_chars()
    return jsonify(shows)

@app.route('/design')
def design():
    return render_template('design.html')


def main():
    app.run(debug=False)


if __name__ == '__main__':
    main()
