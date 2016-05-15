from flask import render_template
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder import AppBuilder, expose, BaseView, has_access
from flask.ext.appbuilder import ModelView, CompactCRUDMixin
from app import appbuilder, db
from models import Service, Alert, ShortCode, Content, MediaFile, Artist, Keyword


class KeywordModelView(ModelView):
    datamodel = SQLAInterface(Keyword)


class ArtistModelView(ModelView):
    datamodel = SQLAInterface(Artist)


class ServiceModelView(ModelView):
    datamodel = SQLAInterface(Service)


class MediaFilesModelView(ModelView):
    datamodel = SQLAInterface(MediaFile)
    label_columns = {'file_name': 'File Name', 'download': 'Download'}
    add_columns = ['file_name', 'content', 'created']
    edit_columns = ['file_name', 'content', 'created']
    list_columns = ['media_file_name', 'download']
    show_columns = ['media_file_name', 'download']


class ContentModelView(CompactCRUDMixin, ModelView):
    datamodel = SQLAInterface(Content)

    related_views = [MediaFilesModelView]

    show_template = 'appbuilder/general/model/show_cascade.html'
    edit_template = 'appbuilder/general/model/edit_cascade.html'

    add_columns = ['name','artist_id', 'created']
    edit_columns = ['name','artist_id', 'created']
    show_fieldsets = [
        ('Info', {'fields': ['name','artist_id', 'created']}),
        ('Audit', {'fields': ['modified'], 'expanded': False})
    ]


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
appbuilder.add_view(AlertModelView, "Alerts", icon="fa-table",
     category="Alerts",
                category_icon="fa-envelope")
appbuilder.add_view(ServiceModelView, "Services", icon="fa-table",
     category="Services")
appbuilder.add_view(ContentModelView, "Contents", icon="fa-folder-open-o",
     category="Multimedia",
                category_icon="fa-envelope")
appbuilder.add_view_no_menu(MediaFilesModelView)
appbuilder.add_view(ArtistModelView, "Artists", icon="fa-table",
     category="Multimedia",
                category_icon="fa-envelope")
appbuilder.add_view(KeywordModelView, "Keywords", icon="fa-table",
     category="Multimedia",
                category_icon="fa-envelope")
