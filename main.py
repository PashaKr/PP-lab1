import json
import xml.etree.ElementTree as ET


class Cinema:
    def __init__(self, name):
        self.name = name
        self.catalog = []
        self.users = []

    def add_movie(self, movie):
        self.catalog.append(movie)

    def add_user(self, user):
        self.users.append(user)

    def search_movie(self, title):
        return [movie for movie in self.catalog if title.lower() in movie.title.lower()]

    def to_json(self, file_path):
        data = {
            "name": self.name,
            "catalog": [movie.to_dict() for movie in self.catalog],
            "users": [user.to_dict() for user in self.users]
        }
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    def to_xml(self, file_path):
        root = ET.Element("Cinema", name=self.name)
        catalog_elem = ET.SubElement(root, "Catalog")
        users_elem = ET.SubElement(root, "Users")

        for movie in self.catalog:
            catalog_elem.append(movie.to_xml())
        for user in self.users:
            users_elem.append(user.to_xml())

        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)


class Movie:
    def __init__(self, title, genre, duration, description, release_year, director):
        self.title = title
        self.genre = genre
        self.duration = duration
        self.description = description
        self.release_year = release_year
        self.director = director
        self.actors = []
        self.comments = []

    def add_actor(self, actor):
        self.actors.append(actor)

    def add_comment(self, comment):
        self.comments.append(comment)

    def to_dict(self):
        return {
            "title": self.title,
            "genre": self.genre,
            "duration": self.duration,
            "description": self.description,
            "release_year": self.release_year,
            "director": self.director.to_dict(),
            "actors": [actor.to_dict() for actor in self.actors],
            "comments": [comment.to_dict() for comment in self.comments]
        }

    def to_xml(self):
        movie_elem = ET.Element("Movie", title=self.title, genre=self.genre, duration=str(self.duration),
                                release_year=str(self.release_year))
        ET.SubElement(movie_elem, "Description").text = self.description
        movie_elem.append(self.director.to_xml())

        actors_elem = ET.SubElement(movie_elem, "Actors")
        for actor in self.actors:
            actors_elem.append(actor.to_xml())

        comments_elem = ET.SubElement(movie_elem, "Comments")
        for comment in self.comments:
            comments_elem.append(comment.to_xml())

        return movie_elem


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.favorite_list = FavoriteList()
        self.watchlist = Watchlist()

    def add_to_favorites(self, movie):
        self.favorite_list.add_movie(movie)

    def add_to_watchlist(self, movie):
        self.watchlist.add_movie(movie)

    def comment_on_movie(self, movie, text):
        comment = Comment(self, text)
        movie.add_comment(comment)

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "favorite_list": [movie.title for movie in self.favorite_list.favorites],
            "watchlist": [movie.title for movie in self.watchlist.watchlist]
        }

    def to_xml(self):
        user_elem = ET.Element("User", username=self.username, email=self.email)

        fav_elem = ET.SubElement(user_elem, "FavoriteList")
        for movie in self.favorite_list.favorites:
            ET.SubElement(fav_elem, "Movie", title=movie.title)

        watchlist_elem = ET.SubElement(user_elem, "Watchlist")
        for movie in self.watchlist.watchlist:
            ET.SubElement(watchlist_elem, "Movie", title=movie.title)

        return user_elem


class Actor:
    def __init__(self, name, biography):
        self.name = name
        self.biography = biography

    def to_dict(self):
        return {
            "name": self.name,
            "biography": self.biography
        }

    def to_xml(self):
        actor_elem = ET.Element("Actor", name=self.name)
        ET.SubElement(actor_elem, "Biography").text = self.biography
        return actor_elem


class Director:
    def __init__(self, name, biography):
        self.name = name
        self.biography = biography

    def to_dict(self):
        return {
            "name": self.name,
            "biography": self.biography
        }

    def to_xml(self):
        director_elem = ET.Element("Director", name=self.name)
        ET.SubElement(director_elem, "Biography").text = self.biography
        return director_elem


class FavoriteList:
    def __init__(self):
        self.favorites = []

    def add_movie(self, movie):
        if movie not in self.favorites:
            self.favorites.append(movie)


class Watchlist:
    def __init__(self):
        self.watchlist = []

    def add_movie(self, movie):
        if movie not in self.watchlist:
            self.watchlist.append(movie)


class Comment:
    def __init__(self, user, text):
        self.user = user
        self.text = text

    def to_dict(self):
        return {
            "user": self.user.username,
            "text": self.text
        }

    def to_xml(self):
        comment_elem = ET.Element("Comment", user=self.user.username)
        comment_elem.text = self.text
        return comment_elem


# Пример использования
cinema = Cinema("Online Cinema")
director1 = Director("Nicolas Winding Refn", "Director of the film Drive")
movie1 = Movie("Drive", "Criminal", 100, "cool movie", 2011, director1)
actor1 = Actor("Ryan Gosling",  "Canadian actor")
user1 = User("Pashtet", "pasha7788hh@gmail.com")
user2 = User("Ne Pashtet", "NEpasha7788hh@gmail.com")

movie1.add_actor(actor1)
cinema.add_movie(movie1)
cinema.add_user(user1)

user1.add_to_favorites(movie1)
user1.comment_on_movie(movie1, "Main character literally me")
user2.comment_on_movie(movie1, "Boring")

cinema.to_json("cinema_data.json")
cinema.to_xml("cinema_data.xml")
