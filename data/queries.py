from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')

def get_most_rated():
    query="""SELECT title, year, runtime, round(rating, 1) as rating, 
    string_agg(g.name, ',' order by name) as genres, trailer, homepage
    FROM shows
    LEFT JOIN show_genres sg on shows.id = sg.show_id
    INNER JOIN genres g on g.id = sg.genre_id
    GROUP BY title, year, runtime, rating, trailer, homepage 
    ORDER BY rating desc limit 15;
    """
    return data_manager.execute_select(query)
