from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///user_test'
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

        user = User(first_name = 'Andres', last_name = 'Iniesta', img_url = 'https://i2-prod.birminghammail.co.uk/sport/football/football-news/article10417994.ece/ALTERNATES/s810/alex.jpg')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()

    def test_list_name(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Andres', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li>Andres Iniesta</li>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {'first': 'Kaka', 'last': 'Ko'}
            resp = client.post('/users', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li>Kaka Ko</li>', html)

    def test_nonexisting_user(self):
        with app.test_client() as client:
            resp = client.get(f'/users/100', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 404)
