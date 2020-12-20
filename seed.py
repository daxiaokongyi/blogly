""" Seed file to make sample data for db."""

from models import User, Post, db
from app import app

db.drop_all()
db.create_all()

u1 = User(first_name = "Alex", last_name = "Pato", img_url = "https://i2-prod.birminghammail.co.uk/sport/football/football-news/article10417994.ece/ALTERNATES/s615/alex.jpg")
u2 = User(first_name = "Ronaldo", last_name = "Christiano", img_url = "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg")

u3 = User(first_name = "James", last_name = "Blunt", img_url = "https://i.guim.co.uk/img/media/41881eac6daff0d98b8e2b125bbe80866cd91c2c/77_1_2742_1645/master/2742.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=26ed1301b51140b5ad6f2c4d4f4d59bf")

u4 = User(first_name = "Norah", last_name = "Jones", img_url = "https://media.npr.org/assets/img/2019/06/05/norah-jones-1-credit-clay-patrick-mcbride_wide-956580b4a824e76d25b3e9a53d50007b78a8b9a2.jpg")



p1 = Post(title = "First Post", content = "This is the first post", user_id = 1)
p2 = Post(title = "Second Post", content = "This is the second post", user_id = 1)
p3 = Post(title = "CR", content = "This is CR", user_id = 2)
p4 = Post(title = "James Blunt's songs", content = "His song is amazing", user_id = 3)
p5 = Post(title = "Norah", content = "This is Norah Jones", user_id = 4)
p6 = Post(title = "Norah's concert", content = "On tomorrow", user_id = 4)


db.session.add(u1)
db.session.add(u2)
db.session.add(u3)
db.session.add(u4)

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)
db.session.add(p5)
db.session.add(p6)


db.session.commit()
