def test_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_valid_login_logout(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post(
        "/login", data=dict(email="patkennedy79@gmail.com", password="FlaskIsAwesome"), follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Login Successful" in response.data

    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"You have been logged out" in response.data
