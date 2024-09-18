import pytest

from flaskblog import bcrypt, create_app, db
from flaskblog.config import TestingConfig
from flaskblog.models import Post, User


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app(TestingConfig)

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(
        username="patkennedy", email="patkennedy79@gmail.com", password=bcrypt.generate_password_hash("FlaskIsAwesome")
    )
    user2 = User(username="kennedypat", email="kennedypat@gmail.com", password=bcrypt.generate_password_hash("PaSsWoRd123"))
    db.session.add(user1)
    db.session.add(user2)

    # Insert post data
    post1 = Post(title="First Post", content="Content for the first post", author=user1)
    post2 = Post(title="Second Post", content="Content for the second post", author=user2)
    db.session.add(post1)
    db.session.add(post2)

    # Commit the changes for the users
    db.session.commit()
    assert len(user1.posts) == 1
    assert len(user2.posts) == 1

    post1.author = user1
    post2.author = user2
    db.session.commit()

    assert post1.author == user1
    assert post2.author == user2

    yield db  # this is where the testing happens!

    db.drop_all()
