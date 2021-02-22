from flask_script import Manager, Shell

from app import app, db
from app.models import User

manager = Manager(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': app.db, 'User': User}


manager.add_command(
    "shell", Shell(
        make_context=make_shell_context))

db_manager = Manager("Perform database operations")


def init_db():
    """For use on command line for setting up
    the database.
    """
    db.drop_all()
    db.create_all()


@db_manager.command
def init_day_sign():
    with app.app_context():
        from app.api.fixtures import DAY_FIXTURES
        from app.api.models import DaySign
        for i in DAY_FIXTURES:
            if not DaySign.query.filter_by(day=i['day']).first():
                day = DaySign(i)
                day.save()


@db_manager.command
def init_month_sign():
    with app.app_context():
        from app.api.fixtures import MONTH_FIXTURE
        from app.api.models import MonthSign
        for i in MONTH_FIXTURE:
            if not MonthSign.query.filter_by(month=i['month']).first():
                month = MonthSign(i)
                month.save()


manager.add_command("database", db_manager)

if __name__ == "__main__":
    manager.run()
