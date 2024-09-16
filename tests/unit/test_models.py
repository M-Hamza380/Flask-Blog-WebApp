from flaskblog.models import Post, User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password_hashed, authenticated, and active fields are defined correctly
    """
    user = User(username="patkennedy", email="patkennedy79@gmail.com", password="FlaskIsAwesome")
    assert user.email == "patkennedy79@gmail.com"
    assert user.username == "patkennedy"
    assert user.password_hashed != "FlaskIsAwesome"
    assert not user.authenticated
    assert user.active


def test_new_post():
    """
    GIVEN a Post model
    WHEN a new Post is created
    THEN check the title, content, and author fields are defined correctly
    """
    user = User(username="patkennedy", email="patkennedy79@gmail.com", password="FlaskIsAwesome")
    post = Post(title="First Post", content="Content for the first post", author=user)
    assert post.title == "First Post"
    assert post.content == "Content for the first post"
    assert post.author == user
