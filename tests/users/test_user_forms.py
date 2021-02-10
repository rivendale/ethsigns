"""
Module of tests for user forms
"""
from ..mocks.users import VALID_USER
from ..mocks.signs import VALID_SIGN_OBJ, VALID_SIGN_REQUEST


class TestUserForms:
    """
    Tests form for signup/login
    """

    def test_fetch_signup_form_succeeds(self, client, init_db):
        """
        Should return an 200 status code when registration form is fetched
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        response = client.get('/register')
        assert response.status_code == 200
        assert "Register" in response.data.decode("utf-8")

    def test_signup_user_with_valid_data_succeeds(self, client, init_db):
        """
        Should return an 201 status code when registration form is fetched
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        response = client.post('/register', data=VALID_USER)
        assert response.status_code == 302
        assert '<a href="/login">/login</a>' in response.data.decode("utf-8")

    def test_fetch_login_form_succeeds(self, client, init_db):
        """
        Should return an 200 status code when login form is fetched
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        response = client.get('/login')
        assert response.status_code == 200
        assert "ETH Signs" in response.data.decode("utf-8")

    def test_login_user_with_valid_data_succeeds(self, client, init_db):
        """
        Should return an 302 status code when login is successful
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        client.post('/register', data=VALID_USER)
        response = client.post('/login', data=VALID_USER)
        assert response.status_code == 302
        assert '<a href="/index">/index</a>' in response.data.decode("utf-8")

    def test_login_user_with_invalid_data_fails(self, client, init_db):
        """
        Should return an 302 status code when login is unsuccessful
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        client.post('/register', data=VALID_USER)
        invalid_user = VALID_USER.copy()
        invalid_user['username'] = "Invalid"
        response = client.post('/login', data=invalid_user)
        assert response.status_code == 302
        assert '<a href="/login">/login</a>' in response.data.decode("utf-8")

    def test_signup_user_with_login_session_redirect_succeeds(self, client, init_db):
        """
        Should return an 302 status code when registration form is fetched
        while a session already exists
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        client.post('/register', data=VALID_USER)
        client.post('/login', data=VALID_USER)
        response = client.post('/register', data=VALID_USER)
        assert response.status_code == 302
        assert '<a href="/index">/index</a>' in response.data.decode("utf-8")

    def test_login_user_with_login_session_redirect_succeeds(self, client, init_db):
        """
        Should return an 302 status code when login form is fetched
        while a login session already exists
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        client.post('/register', data=VALID_USER)
        client.post('/login', data=VALID_USER)
        response = client.post('/login', data=VALID_USER)
        assert response.status_code == 302
        assert '<a href="/index">/index</a>' in response.data.decode("utf-8")

    def test_logout_user_succeeds(self, client, init_db):
        """
        Should return an 302 status code when logout is successful
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        client.post('/register', data=VALID_USER)
        client.post('/login', data=VALID_USER)
        response = client.get('/logout')
        assert response.status_code == 302
        assert '<a href="/index">/index</a>' in response.data.decode("utf-8")

    def test_fetch_index_form_succeeds(self, client, init_db):
        """
        Should return an 200 status code when index form is fetched
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        response = client.get('/index')
        assert response.status_code == 200
        assert 'ETH Signs' in response.data.decode("utf-8")

    def test_request_sign_succeeds(self, client, init_db, new_sign):
        """
        Should return an 302 status code when sign request is successful
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        client.post('/register', data=VALID_USER)
        client.post('/login', data=VALID_USER)
        response = client.post('/index', data=VALID_SIGN_REQUEST)
        assert response.status_code == 302
        assert '<a href="/index/wood/pig/">/' in response.data.decode("utf-8")

    def test_request_sign_two_succeeds(self, client, init_db, test_sign_two):
        """
        Should return an 302 status code when sign request successful
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        client.post('/register', data=VALID_USER)
        client.post('/login', data=VALID_USER)
        data = VALID_SIGN_REQUEST.copy()
        data['birthyear'] = 1996
        response = client.post('/index', data=data)
        assert response.status_code == 302
        assert '<a href="/index/fire/dog/">' in response.data.decode("utf-8")

    def test_request_sign_three_succeeds(self, client, init_db, test_sign_two):
        """
        Should return an 302 status code when sign request successful
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        client.post('/register', data=VALID_USER)
        client.post('/login', data=VALID_USER)
        data = VALID_SIGN_REQUEST.copy()
        data['birthyear'] = 1996
        data['birthday'] = 2
        data['birthmonth'] = 2
        response = client.post('/index', data=data)
        assert response.status_code == 302
        assert '<a href="/index/fire/pig/">' in response.data.decode("utf-8")

    def test_fetch_sign_form_succeeds(self, client, init_db, new_sign):
        """
        Should return an 200 status code when sign form is fetched
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            new_sign(SQLAlchemy): fixture to initialize a new sign
        """
        response = client.get('/index/wood/pig/')
        assert response.status_code == 200

    def test_create_sign_succeeds(self, client, init_db):
        """
        Should return an 302 status code when sign is created
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        client.post('/register', data=VALID_USER)
        client.post('/login', data=VALID_USER)
        response = client.post('/manage', data=VALID_SIGN_OBJ)
        assert response.status_code == 302
        assert '<a href="/manage">/manage</a>' in response.data.decode("utf-8")

    def test_update_sign_succeeds(self, client, init_db):
        """
        Should return an 302 status code when sign is updated
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        client.post('/register', data=VALID_USER)
        client.post('/login', data=VALID_USER)
        response = client.post('/manage', data=VALID_SIGN_OBJ)
        client.post('/manage', data=VALID_SIGN_OBJ)
        assert response.status_code == 302
        assert '<a href="/manage">/manage</a>' in response.data.decode("utf-8")

    def test_fetch_manage_form_succeeds(self, client, init_db):
        """
        Should return an 200 when manage form is fetched
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        client.post('/register', data=VALID_USER)
        client.post('/login', data=VALID_USER)
        client.post('/manage', data=VALID_SIGN_OBJ)
        response = client.get('/manage')
        assert response.status_code == 200
        assert 'ETH Signs ' in response.data.decode("utf-8")

    def test_delete_sign_succeeds(self, client, init_db):
        """
        Should return an 302 status code when sign is removed
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        client.post('/register', data=VALID_USER)
        client.post('/login', data=VALID_USER)
        client.post('/manage', data=VALID_SIGN_OBJ)
        response = client.get('/rmsym/1997')
        assert response.status_code == 302
        assert '<a href="/manage">/manage</a>' in response.data.decode("utf-8")

    def test_delete__non_existing_sign_fails(self, client, init_db):
        """
        Should return an 302 status code when non existing sign is removed
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        client.post('/register', data=VALID_USER)
        client.post('/login', data=VALID_USER)
        response = client.get('/rmsym/1997')
        assert response.status_code == 302
        assert '<a href="/manage">/manage</a>' in response.data.decode("utf-8")
