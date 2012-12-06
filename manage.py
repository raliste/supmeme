from flask.ext.script import Manager

from frontend.views import app


manager = Manager(app)

if __name__ == "__main__":
    manager.run()
