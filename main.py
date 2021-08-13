from flask import Flask, render_template, url_for, request, jsonify
from data import queries
import math
from dotenv import load_dotenv


load_dotenv()
app = Flask('codecool_series')

@app.route('/')
def index():
    return render_template('index.html')

# Show the TV-shows ordered by rating, with paginated display
@app.route('/shows/most-rated')
def most_rated():
    return render_template('most-rated.html')

@app.route('/get-most-rated')
def get_most_rated():
    most_rated = queries.get_all_most_rated()
    for show in most_rated:
        for key in show.keys():
            if key == 'rating' or key == 'id':
                show[key]= str(show[key])
    return jsonify(most_rated)


# Shows detailed view of given show based on its id
@app.route('/show/<show_id>')
def show_page(show_id):
    headers = ['Season number', 'Title', 'Overview']
    show = queries.get_show(show_id)
    actors = queries.get_actors(show_id)
    for key in show.keys():
        if key == 'runtime':
            if show[key]//60 != 0:
                show[key] = str(show[key]//60) + "h" + str(show[key]%60) + "m"
            else:
                show[key] = str(show[key] % 60) + "m"
    seasons = queries.get_seasons(show_id)
    return render_template('show.html', show=show, headers=headers, seasons=seasons, actors=actors[0:3])

#Route for loading all shows dynamically
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
