from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')

def get_show(id):
    query= """
    SELECT title, year, runtime, round(rating, 1) as rating, 
    string_agg(g.name, ', ' order by g.name) as genres, overview, trailer, homepage
    FROM shows
   
    LEFT JOIN show_genres sg on shows.id = sg.show_id
    INNER JOIN genres g on g.id = sg.genre_id
    WHERE shows.id = %(id)s
    GROUP BY shows.id, title, year, runtime, rating, overview, trailer, homepage 
    """
    return data_manager.execute_select(query, variables={"id": id}, fetchall=False)


def get_actors(show_id):
    query= """
        SELECT actors.name FROM actors
        INNER JOIN show_characters on actors.id = show_characters.actor_id
        INNER JOIN shows on show_characters.show_id = shows.id
        WHERE shows.id = %(id)s
        ORDER BY actors.name
        """
    return data_manager.execute_select(query, variables={"id": show_id})

def get_seasons(id):
    query =""" SELECT season_number, title, overview FROM seasons 
    WHERE show_id = %(id)s    
    ORDER BY season_number;
    """
    return data_manager.execute_select(query, variables={"id": id})


def get_most_rated():
    query="""SELECT shows.id, title, year, runtime, round(rating, 1) as rating, 
    string_agg(g.name, ',' order by name) as genres, trailer, homepage
    FROM shows
    LEFT JOIN show_genres sg on shows.id = sg.show_id
    INNER JOIN genres g on g.id = sg.genre_id
    GROUP BY shows.id, title, year, runtime, rating, trailer, homepage 
    ORDER BY rating desc limit 15;
    """
    return data_manager.execute_select(query)

def get_all_most_rated():
    query = """SELECT shows.id, title, year, runtime, round(rating, 1) as rating, 
        string_agg(g.name, ',' order by name) as genres, trailer, homepage
        FROM shows
        LEFT JOIN show_genres sg on shows.id = sg.show_id
        INNER JOIN genres g on g.id = sg.genre_id
        GROUP BY shows.id, title, year, runtime, rating, trailer, homepage 
        ORDER BY rating desc;
        """
    return data_manager.execute_select(query)