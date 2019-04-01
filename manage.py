# Intended use is along the lines of:
# > python manage.py db init
# > python manage.py db migrate
# > python manage.py db upgrade

import os
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app import models

app = create_app(config_name=os.environ.get('FLASK_CONFIG'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
