from flask import render_template, flash
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder import AppBuilder, expose, BaseView, has_access
from flask.ext.appbuilder import ModelView
from app import appbuilder, db
from flask_appbuilder import SimpleFormView
from flask.ext.babelpkg import lazy_gettext as _
from forms import TextAlertForm

"""
    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(MyModelView, "My View", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
"""


class Alert(BaseView):

    default_view = 'text_alert'

    @expose('/text_alert/')
    @has_access
    def text_alert(self):
        # do something with param1
        # and return it
        message="Hello Peter"
        self.update_redirect()
        return self.render_template('text_alert.html',
                           message=message)

    @expose('/multimedia_alert/')
    @has_access
    def multimedia_alert(self):
        # do something with param1
        # and render it
        _user = "Peter"
        message = 'Goodbye %s' % (_user)
        self.update_redirect()
        return self.render_template('text_alert.html',
                           message=message)

appbuilder.add_view(Alert, "Create Text Alert", category="Text Alerts")
appbuilder.add_link("Create Multimedia Alert", href="alert/multimedia_alert/",
     category="Content Alerts")


class AlertFormView(SimpleFormView):
    form = TextAlertForm
    form_title = 'This is alerts form view'
    message = 'My form submitted'

    def form_get(self, form):
        form.text_msg.data = 'This was prefilled'

    def form_post(self, form):
        # post process form
        flash(self.message, 'info')

appbuilder.add_view(AlertFormView, "Alert form View", icon="fa-group", label=_('Alert form View'),
                     category="Alert Forms", category_icon="fa-cogs")

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()