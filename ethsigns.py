from app.api.helpers.celery import celery_task_state
from flask_script import Manager, Shell
from flask import jsonify

from app import app, db, celery_app
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
def init_year_sign():
    with app.app_context():
        from app.api.fixtures import YEAR_FIXTURES
        from app.api.models import Zodiacs
        for i in YEAR_FIXTURES:
            if not Zodiacs.query.filter_by(name=i['name']).first():
                i = {k: str(v) for k, v in i.items() if v != 'base_index'}
                sign = Zodiacs(i)
                sign.save()


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


@app.route('/celery/health')
def celery_stats():
    """Checks tasks queued by celery.
    if celery is up the response should have `sample_scheduler` task
    """

    msg = None

    ins = celery_app.control.inspect()

    try:
        tasks = ins.registered_tasks()
        msg = {"tasks": tasks, "status": "Celery up"}
    except ConnectionError:
        msg = {"status": "Redis server down"}
    except Exception:
        msg = {"status": "Celery down"}

    return jsonify(dict(message=msg)), 200


@app.route('/celery-beat/health')
def celery_beat_stats():
    """Checks tasks scheduled by celery-beat."""

    import shelve

    down_tasks = {}
    ok_tasks = {}

    file_data = shelve.open(
        'celerybeat-schedule'
    )
    # Name of the file used by PersistentScheduler to store the
    # last run times of periodic tasks.

    entries = file_data.get('entries')

    if not entries:
        return jsonify(dict(error="celery-beat service not available")), 503

    for task_name, task in entries.items():

        try:
            celery_task_state(
                task, task_name, ok_tasks, down_tasks, is_cron_task=False)

        except AttributeError:

            celery_task_state(task, task_name, ok_tasks, down_tasks)

    if down_tasks:
        return jsonify(dict(message={
            'Down tasks': down_tasks,
        })), 503

    return jsonify(dict(message={'Okay tasks': ok_tasks})), 200


if __name__ == "__main__":
    manager.run()
