from flask import render_template
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder import ModelView, CompactCRUDMixin
from app import appbuilder, db
from models import Service, Alert, ShortCode, Content, MediaFile, Artist,\
 Keyword, Client, ModelType


class KeywordModelView(ModelView):
    datamodel = SQLAInterface(Keyword)
    list_columns = ['name', 'model', 'status', 'created']


class ArtistModelView(ModelView):
    datamodel = SQLAInterface(Artist)
    list_columns = ['name', 'keyword.name', 'created']


class ServiceModelView(ModelView):
    datamodel = SQLAInterface(Service)
    list_columns = ['name', 'client.name', 'keyword.name', 'status', 'created']


class MediaFilesModelView(ModelView):
    datamodel = SQLAInterface(MediaFile)
    label_columns = {'file_name': 'File Name', 'download': 'Download'}
    add_columns = ['file_name', 'content', 'created']
    edit_columns = ['file_name', 'content', 'created']
    list_columns = ['content.name', 'media_file_name', 'download']
    show_columns = ['media_file_name', 'download']


class ContentModelView(CompactCRUDMixin, ModelView):
    datamodel = SQLAInterface(Content)

    related_views = [MediaFilesModelView]

    add_columns = ['name', 'artist', 'created']
    edit_columns = ['name', 'artist', 'created']
    list_columns = ['name', 'artist.name', 'created']
    show_fieldsets = [
        ('Info', {'fields': ['name', 'artist_id', 'created']}),
        ('Audit', {'fields': ['modified'], 'expanded': False})
    ]


class ShortcodeModelView(ModelView):
    datamodel = SQLAInterface(ShortCode)
    edit_exclude_columns = ['modified', 'status']
    add_exclude_columns = ['modified', 'status']
    list_columns = ['short_code', 'client.name', 'keyword.name', 'status',
         'created']


class AlertModelView(ModelView):
    datamodel = SQLAInterface(Alert)
    #related_views = [ServiceModelView, ContentModelView, ShortcodeModelView]
    #message,msisdn,shortcode,content_id ,service_id ,sent ,scheduled_time,
     #alert_type_id,time_sent ,created_by ,created
    edit_exclude_columns = ['created_by', 'sent', 'modified', 'created',
         'time_sent']
    add_exclude_columns = ['created_by', 'sent', 'created', 'modified',
         'time_sent']
    list_columns = ['content_id', 'shortcode', 'message', 'service_id',
    'alert_type_id', 'scheduled_time']


class ClientModelView(ModelView):
    datamodel = SQLAInterface(Client)
    list_columns = ['name', 'callback_url', 'subscription_url', 'active',
    'credit_units', 'created']


class ModelTypeModelView(ModelView):
    datamodel = SQLAInterface(ModelType)
    list_columns = ['name', 'model', 'status', 'created']


"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template,
         appbuilder=appbuilder), 404

db.create_all()
appbuilder.add_view(AlertModelView, "Alerts", icon="fa-table",
     category="Content Management",
                category_icon="fa-envelope")
appbuilder.add_view(ServiceModelView, "Services", icon="fa-table",
     category="Content Management")
appbuilder.add_view(ClientModelView, "Clients", icon="fa-table",
     category="Content Management")
appbuilder.add_view(ModelTypeModelView, "ModelTypes", icon="fa-table",
     category="Content Management")
appbuilder.add_view(ShortcodeModelView, "Shortcode", icon="fa-table",
     category="Content Management")
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
