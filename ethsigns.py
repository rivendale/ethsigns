from app import app, db
from app.models import User


@app.shell_context_processor
def make_shell_context():
    return {'db': app.db, 'User': User}


def init_db():
    """For use on command line for setting up
    the database.
    """
    db.drop_all()
    db.create_all()
