from flask import Flask
import logging
from main.routes import bp
from main.models import db
import config as cfg
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.secret_key = cfg.app_secret_key
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=10)

    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)
    logging.info("App is started")

    engine = cfg.engine
    username = cfg.username
    password = cfg.password
    dbname = cfg.dbname
    host = cfg.host
    port = cfg.port

    app.config["SQLALCHEMY_DATABASE_URI"] = f"{engine}://{username}:{password}@{host}:{port}/{dbname}"
    db.init_app(app)
    logging.info("DB is started")

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)



