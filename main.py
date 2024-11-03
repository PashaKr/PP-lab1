class Cinema:
    def __init__(self, name):
        self.name = name
        self.catalog = []
        self.users = []

    def add_movie(self, movie):
        self.catalog.append(movie)

    def add_user(self, user):
        self.users.append(user)


class Movie:
    def __init__(self, title, genre, description, release):
        self.title = title
        self.genre = genre
        self.description = description
        self.release = release
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def review(self, movie, text):
        review = Review(self, text)
        movie.add_review(review)

class Review:
    def __init(self, user, text):
        self.user = user
        self.text = text

class Category:
    def __init__(self, name):
        self.name = name
        self.movies = []

    def add_movie(self, movie):
        self.movies.append(movie)
