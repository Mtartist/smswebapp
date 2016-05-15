import logging
from flask import Flask
from flask.ext.appbuilder import SQLA, AppBuilder
from app.index import LandingView

"""
 Logging configuration
"""

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)
appbuilder = AppBuilder(app, db.session, indexview=LandingView)


from app import views


