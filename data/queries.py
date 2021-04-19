from psycopg2._psycopg import AsIs

from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_episodes():
    query="""
    SELECT shows.title, COUNT(e.id) as episode_number FROM shows
    LEFT JOIN seasons s on shows.id = s.show_id
    LEFT JOIN episodes e on s.id = e.season_id
    GROUP BY shows.title;
    
    """
    return data_manager.execute_select(query)

def actors_most_chars():
    query ="""
    SELECT actors.name , count(sc.actor_id) as chars, string_agg(sc.character_name, ', '), ROUND(AVG(s.rating), 1)::float as rating FROM actors
    LEFT JOIN show_characters sc on actors.id = sc.actor_id
    LEFT JOIN shows s on s.id = sc.show_id
    GROUP BY actors.name
    ORDER BY chars desc
    limit 10
    ;"""
    return data_manager.execute_select(query)
    
def get_shows_s_e(season, episode):
    query="""
    SELECT shows.title, count(DISTINCT s.id) as s_count, count(e.id) as e_count FROM shows
    LEFT JOIN seasons s on shows.id = s.show_id
    LEFT JOIN episodes e on s.id = e.season_id
    GROUP BY shows.title
    HAVING count(DISTINCT s.id) >= %(season)s and count(e.id) >=%(episode)s
    """

    return data_manager.execute_select(query, {'season': season, 'episode': episode})
    


def get_rated(genre):
    query ="""
    SELECT shows.title, shows.year, shows.rating::float as rating FROM shows
    LEFT JOIN show_genres sg on shows.id = sg.show_id
    LEFT JOIN genres g on g.id = sg.genre_id
    WHERE %(genre)s LIKE g.name
    ORDER BY rating desc
    LIMIT 10;
    """
    return data_manager.execute_select(query, {'genre:genre'})


def all_years():
    query="""
    SELECT Count(shows.title), EXTRACT('year' FROM year) as years, ROUND(AVG(rating), 1)::float from shows
    WHERE EXTRACT('year' FROM year)::int BETWEEN 1970 AND 2010
    GROUP BY years
    ORDER BY years
    ;
    
    """
    return data_manager.execute_select(query)

def longest():
    query="""
    SELECT shows.title, count(e.id)*shows.runtime as run FROM shows
    LEFT JOIN seasons s on shows.id = s.show_id
    LEFT JOIN episodes e on s.id = e.season_id
    GROUP BY shows.title, shows.runtime
    ORDER BY run DESC
    LIMIT 10;
    """
    return data_manager.execute_select(query)



def get_longest_actors(titles):
    query ="""
    SELECT actors.name, s.title FROM actors
    LEFT JOIN show_characters sc on actors.id = sc.actor_id
    LEFT JOIN shows s on s.id = sc.show_id
    WHERE s.title IN %(titles)s;
    """
    return data_manager.execute_select(query, {'titles': titles})

def search_titles(search_string):
    query ="""
    SELECT title FROM shows
    WHERE title LIKE  %(search_string)s ;
    """
    return data_manager.execute_select(query, {'search_string': '%'+search_string+'%'})

def most_active():
    query="""
    SELECT name,
    CASE 
    WHEN death is null then DATE_PART('YEAR', AGE('2021-04-20', birthday))
    ELSE DATE_PART('YEAR', AGE(death, birthday))
    END as age,  count(e.id) as episode_count, CASE WHEN death is null then 'true' ELSE 'false' END as alive
    FROM actors
    LEFT JOIN show_characters sc on actors.id = sc.actor_id
    LEFT JOIN shows s on sc.show_id = s.id
    LEFT JOIN seasons s2 on s.id = s2.show_id
    LEFT JOIN episodes e on s2.id = e.season_id
    GROUP BY name, age, alive
    ORDER BY episode_count desc
    """
    return data_manager.execute_select(query)


def average(year):
    query = """
    SELECT name, birthday FROM actors
    LEFT JOIN show_characters sc on actors.id = sc.actor_id
    LEFT JOIN shows s on s.id = sc.show_id
    WHERE birthday > (%(year)s)::date
    """
    return data_manager.execute_select(query, {'year': str(year)+'-01-01'})

def shows_by_genre(genre):
    query="""
    SELECT title, count(sc.id) as character_count FROM shows 
    LEFT JOIN show_genres sg on shows.id = sg.show_id
    LEFT JOIN genres g on g.id = sg.genre_id
    LEFT JOIN show_characters sc on shows.id = sc.show_id
    WHERE g.name = %(genre)s
    GROUP BY title
    """
    return data_manager.execute_select(query, {'genre': genre})

def actors_given_year(year):
    query="""
    SELECT actors.name, DATE_PART('YEAR', AGE(NOW(), birthday)) as age from actors
    LEFT JOIN show_characters sc on actors.id = sc.actor_id
    LEFT JOIN shows s on s.id = sc.show_id
    WHERE DATE_PART('YEAR', s.year) = (%(year)s)
    ORDER BY age DESC 
    ;
    """
    return data_manager.execute_select(query, {'year': year})

def get_search(search_string):
    query="""
    SELECT name, sc.character_name, s.title FROM actors
    LEFT JOIN show_characters sc on actors.id = sc.actor_id
    LEFT JOIN shows s on s.id = sc.show_id
    WHERE sc.character_name ILIKE %(search_string)s;
    """
    return data_manager.execute_select(query, {'search_string': search_string})

def highest_no_season():
    query ="""
    SELECT MAX(season_number) FROM seasons;
    """
    return data_manager.execute_select(query)

def genre(genre_id):
    query="""
    SELECT shows.title, count(e.id) as episode_count FROM shows
    LEFT JOIN show_genres sg on shows.id = sg.show_id
    LEFT JOIN genres g on g.id = sg.genre_id
    LEFT JOIN seasons s on shows.id = s.show_id
    LEFT OUTER JOIN episodes e on s.id = e.season_id
    WHERE g.id = %(genre_id)s
    GROUP BY shows.title
    HAVING count(e.id) > 20
    Order by episode_count desc
    LIMIT 50;
    """
    return data_manager.execute_select(query, {'genre_id': genre_id})

def get_data(datatype, order):
    query="""
    SELECT title FROM %(datatype)s
    ORDER BY title %(order)s
    """
    return data_manager.execute_select(query, {'datatype': AsIs(datatype), 'order': AsIs(order)})

def get_actors_shows():
    query="""
    SELECT actors.name, count(s.id), string_agg(s.title, ', ') FROM actors
    LEFT JOIN show_characters sc on actors.id = sc.actor_id
    LEFT JOIN shows s on s.id = sc.show_id
    GROUP BY  actors.name
    ORDER BY count(s.id) desc
    """
    return data_manager.execute_select(query)