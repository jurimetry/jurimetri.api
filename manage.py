import os
from app import blueprint
from flask_script import Manager
from app.main import create_app

app = create_app(os.getenv('BOILERPLATE_ENV') or 'prod')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

@manager.command
def run():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    manager.run()