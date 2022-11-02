from models import Movie, Actor

# Sample Data for Test Database

movies = [
  Movie(title="Star Wars: Episode 1 - The Phantom Menace", release_date=1999),
  Movie(title="Star Wars: Episode 2 - Attack of the Clones", release_date=2002),
  Movie(title="Star Wars: Episode 3 - Revenge of the Sith", release_date=2005),
  Movie(title="Star Wars: Episode 4 - A New Hope", release_date=1977),
  Movie(title="Star Wars: Episode 5 - The Empire Strikes Back", release_date=1980),
  Movie(title="Star Wars: Episode 6 - Return of the Jedi", release_date=1983),
]

actors = [
  Actor(name="Ewan Mcgregor", age=51, gender="male"),
  Actor(name="Hayden Christensen", age=41, gender="male"),
  Actor(name="Natalie Portman", age=41, gender="female"),
  Actor(name="Mark Hamill", age=71, gender="male"),
  Actor(name="Harrison Ford", age=80, gender="male"),
]

# Sample Data for Create tests

new_movie = Movie(title="Star Wars: Episode 7 - The Force Awakens", release_date=2015)
new_actor = Actor(name="Daisy Ridley", age=30, gender="female")

new_movie_non_existent_actor_id = new_movie.format()
new_movie_non_existent_actor_id["actors"] = [10000]

new_actor_non_existent_movie_id = new_actor.format()
new_actor_non_existent_movie_id["movies"] = [10000]


# Sample data for Update tests
update_movie = {"title": "Star Wars: Return of the Jediii", "release_date": 1982,"actors": [4, 5]}

update_actor = {"name": "Harrison Fordi", "age": 61, "gender": "male", "movies": [5,6]}