from flask.cli import FlaskGroup
from api import create_app, db
from api.models import User

cli = FlaskGroup(create_app=create_app)

@cli.command("create_db")
def create_db():
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    cli()
