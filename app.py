from flask import Flask, render_template, request , jsonify
import requests

app = Flask(__name__)

API_KEY = 'ff17793b9ec34ddfe7d19a4958678639'
BASE_URL = 'https://api.themoviedb.org/3'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        genre = request.form.get('genre', '')
        search_term = request.form.get('search_term', '')
        release_year = request.form.get('release_year', '')
        actor_name =request.form.get('search_actor', '')  
        if genre:
            movies = fetch_movies_by_genre(genre,pages=[1,2,3])
            movies.sort(key=lambda x: x.get('vote_average', 0), reverse=True)
        elif search_term:
            movies = search_movies(search_term)
            movies.sort(key=lambda x: x.get('vote_average', 0), reverse=True)
        elif release_year:
            movies = fetch_movies_by_release_year(release_year,pages=[1,2,3])
            movies.sort(key=lambda x: x.get('vote_average', 0), reverse=True)
                  
        elif actor_name:
            movies = search_movies_by_actor(actor_name)
        else:
            movies = fetch_popular_movies(pages=[1,2,3])          
    else:
       
        movies = fetch_popular_movies(pages=[1,2,3])   
    return render_template('index.html', movies=movies)

@app.route('/get_trailer/<int:movie_id>', methods=['GET'])
def get_trailer(movie_id):
    trailer_link = fetch_movie_trailer(movie_id)
    return jsonify(trailer_link=trailer_link)

@app.route('/templates/movie.html/<int:movie_id>', methods=['GET'])
def movie(movie_id):
    movie_details = fetch_movie_details(movie_id)
    movie_cast = fetch_movie_cast(movie_id)
    return render_template('movie.html', movie=movie_details, cast=movie_cast)

def fetch_movie_details(movie_id):
    endpoint = f'/movie/{movie_id}'
    params = {'api_key': API_KEY}
    response = requests.get(BASE_URL + endpoint, params=params)
    data = response.json()

    return data 

def fetch_movie_cast(movie_id):
    endpoint = f'/movie/{movie_id}/credits'
    params = {'api_key': API_KEY}
    response = requests.get(BASE_URL + endpoint, params=params)
    data = response.json()
    if 'cast' in data:
        return data['cast']
    else:
        return []

def fetch_movie_trailer(movie_id):
    endpoint = f'/movie/{movie_id}/videos'
    params = {
        'api_key': API_KEY,
    }
    response = requests.get(BASE_URL + endpoint, params=params)
    data = response.json()

    if 'results' in data and data['results']:
       return 'https://www.youtube.com/embed/' + data['results'][0]['key']
    
    return None

def fetch_movies_by_genre(genre_id,pages):
    all_results = []
    for page in pages:
       endpoint = '/discover/movie'
       params = {
        'api_key': API_KEY,
        'with_genres': genre_id,
        'page':page
      }
       response = requests.get(BASE_URL + endpoint, params=params)
       data = response.json()

       if 'results' in data:
            all_results.extend(data['results'])

    return all_results

def search_movies(query):
    endpoint = '/search/movie'
    params = {
        'api_key': API_KEY,
        'query': query
    }

    response = requests.get(BASE_URL + endpoint, params=params)
    data = response.json()

    if 'results' in data:
        return data['results']
    else:
        return []
    
def fetch_movies_by_release_year(release_year,pages):
    all_results = []
    for page in pages:
      endpoint = '/discover/movie'
      params = {
        'api_key': API_KEY,
        'primary_release_year': release_year,
        'page': page
      }
      response = requests.get(BASE_URL + endpoint, params=params)
      data = response.json()
      if 'results' in data:
            all_results.extend(data['results'])

    return all_results

def fetch_popular_movies(pages):
    all_results = []
    for page in pages:
      endpoint = '/movie/popular'
      params = {
        'api_key': API_KEY ,
        'page': page
      }
      response = requests.get(BASE_URL + endpoint, params=params)
      data = response.json()
      if 'results' in data:
            all_results.extend(data['results'])    
    return all_results
   
def search_movies_by_actor(actor_name):
    endpoint = '/search/person'
    params = {
        'api_key': API_KEY,
        'query': actor_name
    }

    response = requests.get(BASE_URL + endpoint, params=params)
    data = response.json()

    if 'results' in data:
        # Extract the actor's ID from the search results
        actor_id = data['results'][0]['id']
        movies_endpoint = f'/person/{actor_id}/movie_credits'
        movies_response = requests.get(BASE_URL + movies_endpoint, params={'api_key': API_KEY})
        movies_data = movies_response.json()

        if 'cast' in movies_data:
            return movies_data['cast']
  
    return []

if __name__ == '__main__':
    app.run(debug=True)
