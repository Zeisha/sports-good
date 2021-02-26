from main import app
import os
import pytest

@pytest.fixture
def client():
    # Prepare before your test
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            db=app.init_db()
        yield client
    os.close(db)
    os.unlink(app.config['SQLALCHEMY_DATABASE_URI'])

def test_get_good():
    rv = client.get('/goods/1')
    assert rv.status_code == 200
