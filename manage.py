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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    manager.run()