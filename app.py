from flask import request
from flask_restx import Api, Resource
from init_app import app
from db_models import *
from serialize import *
from create_data import data_to_db

api = Api(app)
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        movies_query = db.session.query(Movie)
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if director_id is not None:
            if genre_id is not None:
                movies_query = movies_query.filter(Movie.director_id == director_id, Movie.genre_id == genre_id)
            else:
                movies_query = movies_query.filter(Movie.director_id == director_id)
        elif genre_id is not None:
            movies_query = movies_query.filter(Movie.genre_id == genre_id)
        return movies_schema.dump(movies_query.all()), 200

    def post(self):
        req_json = request.json
        movie = Movie(**req_json)

        with db.session.begin():
            db.session.add(movie)

        return 'Movie added', 201

@movies_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid):
        movie = db.session.query(Movie).get(uid)
        if not movie:
            return 'Movie not found', 404
        return movie_schema.dump(movie), 200

    def put(self, uid):
        req_json = request.json
        movie = db.session.query(Movie).get(uid)
        if movie == None:
            return 'Movie not found', 404

        movie.title = req_json.get('title')
        movie.description = req_json.get('description')
        movie.trailer = req_json.get('trailer')
        movie.year = req_json.get('year')
        movie.rating = req_json.get('rating')
        movie.genre_id = req_json.get('genre_id')
        movie.director_id = req_json.get('director_id')

        db.session.add(movie)
        db.session.commit()

        return 'Movie updated', 204

    def delete(self, uid):
        movie = db.session.query(Movie).get(uid)
        if not movie:
            return 'Movie not found', 404
        db.session.delete(movie)
        db.session.commit()
        return 'Movie deleted', 204


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors_query = db.session.query(Director)
        return directors_schema.dump(directors_query.all()), 200

    def post(self):
        req_json = request.json
        director = Director(**req_json)

        with db.session.begin():
            db.session.add(director)

        return 'Director added', 201


@directors_ns.route('/<int:uid>')
class DirectorView(Resource):
    def get(self, uid):
        director = db.session.query(Director).get(uid)
        if not director:
            return 'Director not found', 404
        return director_schema.dump(director), 200

    def put(self, uid):
        req_json = request.json
        director = db.session.query(Director).get(uid)
        if director == None:
            return 'Director not found', 404

        director.name = req_json.get('name')

        db.session.add(director)
        db.session.commit()

        return 'Director updated', 204

    def delete(self, uid):
        director = db.session.query(Director).get(uid)
        if not director:
            return 'Director not found', 404
        db.session.delete(director)
        db.session.commit()
        return 'Director deleted', 204


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres_query = db.session.query(Genre)
        return genres_schema.dump(genres_query.all()), 200

    def post(self):
        req_json = request.json
        genre = Genre(**req_json)

        with db.session.begin():
            db.session.add(genre)

        return 'Genre added', 201


@genres_ns.route('/<int:uid>')
class GenreView(Resource):
    def get(self, uid):
        genre = db.session.query(Genre).get(uid)
        if not genre:
            return 'Genre not found', 404
        return genre_schema.dump(genre), 200

    def put(self, uid):
        req_json = request.json
        genre = db.session.query(Genre).get(uid)
        if genre == None:
            return 'Genre not found', 404

        genre.name = req_json.get('name')

        db.session.add(genre)
        db.session.commit()

        return 'Genre updated', 204

    def delete(self, uid):
        genre = db.session.query(Genre).get(uid)
        if not genre:
            return 'Genre not found', 404
        db.session.delete(genre)
        db.session.commit()
        return 'Genre deleted', 204

if __name__ == '__main__':
    app.config.from_object('config.Config')
    db.init_app(app)

    db.drop_all()
    db.create_all()
    data_to_db()

    app.run(debug=True)
