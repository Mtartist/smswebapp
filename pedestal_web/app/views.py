from flask import render_template
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder import ModelView, CompactCRUDMixin
from app import appbuilder, db
from models import Service, Alert, ShortCode, Content, MediaFile, Artist,\
 Keyword, Client, ModelType, Subscriber, Inbox, Outbox,SdpProduct,UserClient,Profile,ContentService,ArtistRevShare,BulkSender,BulkSenderClient,Client,ContactGroup,ContactGroup,ContactGroupProfile


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


class SubscriberModelView(ModelView):
    datamodel = SQLAInterface(Subscriber)
    list_columns = ['profile_id', 'service_id', 'status','created', 'modified']


class InboxModelView(ModelView):
    datamodel = SQLAInterface(Inbox)
    list_columns = ['message','msisdn','short_code_id','link_id','service_id','profile_id','created','modified']


class OutboxModelView(ModelView):
    datamodel = SQLAInterface(Outbox)
    list_columns = ['alert_id', 'text', 'msisdn', 'content_id_hash', 'ref_number', 'dlr_status', 'processed', 'sends', 'time_sent', 'created', 'modified']

class SdpProductModelView(ModelView):
    datamodel = SQLAInterface(SdpProduct)
    list_columns = ['service','product','shortcode_id','keyword_id','status','created','modified']

class UserClientModelView(ModelView):
    datamodel = SQLAInterface(UserClient)
    list_columns = ['user_id','client_id']

class ProfileModelView(ModelView):
    datamodel = SQLAInterface(Profile)
    list_columns = ['msisdn','network_id','created','modified']

class ContentServiceModelView(ModelView):
    datamodel = SQLAInterface(ContentService)
    list_columns = ['content_id','service_id']

class ArtistRevShareModelView(ModelView):
    datamodel = SQLAInterface(ArtistRevShare)
    list_columns = ['artist_id' ,'contract_id','rev_share','status','created','modified']

class BulkSenderModelView(ModelView):
    datamodel = SQLAInterface(BulkSender)
    list_columns = ['name','sdp_service_id','sdp_access_code','status','created','modified']

class BulkSenderClientModelView(ModelView):
    datamodel = SQLAInterface(BulkSenderClient)
    list_columns = ['bulksender_id','client_id']

class ContactGroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    list_columns = ['name','client_id','status','created','modified']

class ContactGroupProfileModelView(ModelView):
    datamodel = SQLAInterface(ContactGroupProfile)
    list_columns = ['contactgroup_id','profile_id']




"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template,
         appbuilder=appbuilder), 404

db.create_all()
appbuilder.add_view(AlertModelView, "Alerts", icon="fa-table",
     category="Messaging",
                category_icon="fa-envelope")
appbuilder.add_view(ServiceModelView, "Services", icon="fa-table",
     category="Settings")
appbuilder.add_view(ClientModelView, "Clients", icon="fa-table",
     category="Content Management")
appbuilder.add_view(ModelTypeModelView, "ModelTypes", icon="fa-table",
     category="Settings")
appbuilder.add_view(ShortcodeModelView, "Shortcode", icon="fa-table",
     category="Settings")
appbuilder.add_view(SubscriberModelView, "Subscriber", icon="fa-table",
     category="Content Management")
appbuilder.add_view(ContentModelView, "Contents", icon="fa-folder-open-o",
     category="Content",
                category_icon="fa-envelope")
appbuilder.add_view_no_menu(MediaFilesModelView)
appbuilder.add_view(ArtistModelView, "Artists", icon="fa-table",
     category="Content",
                category_icon="fa-envelope")
appbuilder.add_view(KeywordModelView, "Keywords", icon="fa-table",
     category="Settings",
                category_icon="fa-envelope")
appbuilder.add_view(InboxModelView, "Inbox", icon="fa-table",
     category="Messaging",
                category_icon="fa-envelope")
appbuilder.add_view(OutboxModelView, "Outbox", icon="fa-table",
     category="Messaging",
                category_icon="fa-envelope")
appbuilder.add_view(SdpProductModelView, "SdpProducts", icon="fa-table",
     category="Settings",
                category_icon="fa-envelope")
appbuilder.add_view(UserClientModelView, "UserClientMap", icon="fa-table",
     category="Settings",
                category_icon="fa-envelope")
appbuilder.add_view(ProfileModelView, "Profiles", icon="fa-table",
     category="Content Management",
                category_icon="fa-envelope")
appbuilder.add_view(ContentServiceModelView, "ContentServiceMap", icon="fa-table",
     category="Content",
                category_icon="fa-envelope")
appbuilder.add_view(ArtistRevShareModelView, "ArtistRevShares", icon="fa-table",
     category="Content Management",
                category_icon="fa-envelope")
appbuilder.add_view(BulkSenderModelView, "BulkSenders", icon="fa-table",
     category="Bulk SMS",
                category_icon="fa-envelope")
appbuilder.add_view(BulkSenderClientModelView, "BulkSenderClientMap", icon="fa-table",
     category="Bulk SMS",
                category_icon="fa-envelope")
appbuilder.add_view(ContactGroupModelView, "ContactGroups", icon="fa-table",
     category="Bulk SMS",
                category_icon="fa-envelope")
appbuilder.add_view(ContactGroupProfileModelView, "ContactGroupProfileMap", icon="fa-table",
     category="Bulk SMS",
                category_icon="fa-envelope")
