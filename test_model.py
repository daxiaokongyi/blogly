from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask error be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# don't use Flask DebugToolBar while testing
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users. """
    def setUp(self):
        """Add sample user"""
        User.query.delete()

        user = User(first_name = 'Pato', last_name = 'Alex', img_url = 'https://i2-prod.birminghammail.co.uk/sport/football/football-news/article10417994.ece/ALTERNATES/s810/alex.jpg')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()

    def test_full_name(self):
        user = User(first_name = 'Iniesta', last_name = 'Andres')
        self.assertEquals(User.query.first().full_name, 'Alex, Pato')

