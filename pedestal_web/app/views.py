from flask import render_template, flash
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder import AppBuilder, expose, BaseView, has_access
from flask.ext.appbuilder import ModelView
from app import appbuilder, db
from models import Service, Alert, ShortCode, Content


class ServiceModelView(ModelView):
    datamodel = SQLAInterface(Service)


class ContentModelView(ModelView):
    datamodel = SQLAInterface(Content)


class ShortcodeModelView(ModelView):
    datamodel = SQLAInterface(ShortCode)


class AlertModelView(ModelView):
    datamodel = SQLAInterface(Alert)
    related_views = [ServiceModelView, ContentModelView, ShortcodeModelView]
    edit_exclude_columns = ['created_by', 'modified', 'time_sent']
    add_exclude_columns = ['created_by', 'sent', 'modified', 'time_sent']

"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template,
         appbuilder=appbuilder), 404

db.create_all()
appbuilder.add_view(AlertModelView, "List Alerts", icon="fa-folder-open-o",
     category="Alerts",
                category_icon="fa-envelope")
appbuilder.add_view(ServiceModelView, "List Services", icon="fa-envelope",
     category="Services")