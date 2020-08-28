import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api import create_api, db

config_name = os.getenv('FLASK_CONFIG')
api = create_api(config_name)

migrate = Migrate(app=api, db=db)

manager = Manager(app=api)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()