from flask.ext.appbuilder import Model
from flask.ext.appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Index, \
Integer, String, text
from sqlalchemy.orm import relationship
from flask_appbuilder.filemanager import get_file_original_name
from flask import Markup, url_for


class AbPermission(Model):
    __tablename__ = 'ab_permission'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)


class AbPermissionView(Model):
    __tablename__ = 'ab_permission_view'

    id = Column(Integer, primary_key=True)
    permission_id = Column(ForeignKey(u'ab_permission.id'), index=True)
    view_menu_id = Column(ForeignKey(u'ab_view_menu.id'), index=True)

    permission = relationship(u'AbPermission')
    view_menu = relationship(u'AbViewMenu')


class AbPermissionViewRole(Model):
    __tablename__ = 'ab_permission_view_role'

    id = Column(Integer, primary_key=True)
    permission_view_id = Column(ForeignKey(u'ab_permission_view.id'), index=True)
    role_id = Column(ForeignKey(u'ab_role.id'), index=True)

    permission_view = relationship(u'AbPermissionView')
    role = relationship(u'AbRole')


class AbRegisterUser(Model):
    __tablename__ = 'ab_register_user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(256))
    email = Column(String(64), nullable=False)
    registration_date = Column(DateTime)
    registration_hash = Column(String(256))


class AbRole(Model):
    __tablename__ = 'ab_role'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)


class AbUser(Model):
    __tablename__ = 'ab_user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(256))
    active = Column(Integer)
    email = Column(String(64), nullable=False, unique=True)
    last_login = Column(DateTime)
    login_count = Column(Integer)
    fail_login_count = Column(Integer)
    created_on = Column(DateTime)
    changed_on = Column(DateTime)
    created_by_fk = Column(ForeignKey(u'ab_user.id'), index=True)
    changed_by_fk = Column(ForeignKey(u'ab_user.id'), index=True)

    parent = relationship(u'AbUser', remote_side=[id], primaryjoin='AbUser.changed_by_fk == AbUser.id')
    parent1 = relationship(u'AbUser', remote_side=[id], primaryjoin='AbUser.created_by_fk == AbUser.id')


class AbUserRole(Model):
    __tablename__ = 'ab_user_role'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(u'ab_user.id'), index=True)
    role_id = Column(ForeignKey(u'ab_role.id'), index=True)

    role = relationship(u'AbRole')
    user = relationship(u'AbUser')


class AbViewMenu(Model):
    __tablename__ = 'ab_view_menu'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)


class Alert(Model):
    __tablename__ = 'alert'

    id = Column(Integer, primary_key=True)
    message = Column(String)
    msisdn = Column(String(200))
    shortcode = Column(String(50))
    content_id = Column(Integer, index=True)
    service_id = Column(ForeignKey(u'service.id'), index=True)
    sent = Column(Integer, nullable=False, index=True)
    scheduled_time = Column(DateTime, nullable=False, index=True)
    alert_type_id = Column(ForeignKey(u'model_type.id'), nullable=False, index=True)
    time_sent = Column(DateTime, index=True)
    created_by = Column(String(100), nullable=False, index=True)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime, index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    alert_type = relationship(u'ModelType')
    service = relationship(u'Service')


class Artist(Model):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    keyword_id = Column(ForeignKey(u'keyword.id'), nullable=False, index=True)
    email = Column(String(254))
    contact = Column(String(50))
    status = Column(Integer, nullable=False, index=True)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime, index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    keyword = relationship(u'Keyword')


class ArtistRevShare(Model):
    __tablename__ = 'artist_rev_share'
    __table_args__ = (
        Index('artist_id', 'artist_id', 'contract_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    artist_id = Column(ForeignKey(u'artist.id'), nullable=False, index=True)
    contract_id = Column(ForeignKey(u'contract.id'), nullable=False, unique=True)
    rev_share = Column(String(30), nullable=False, index=True)
    status = Column(Integer, nullable=False, index=True)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime, index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    artist = relationship(u'Artist')
    contract = relationship(u'Contract')


class BulkSender(Model):
    __tablename__ = 'bulk_sender'
    __table_args__ = (
        Index('name', 'name', 'sdp_access_code', unique=True),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    sdp_service_id = Column(String(150))
    sdp_access_code = Column(String(50), nullable=False)
    status = Column(Integer, nullable=False, index=True)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime,  index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class BulkSenderClient(Model):
    __tablename__ = 'bulk_sender_client'
    __table_args__ = (
        Index('bulksender_id', 'bulksender_id', 'client_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    bulksender_id = Column(ForeignKey(u'bulk_sender.id'), nullable=False, index=True)
    client_id = Column(ForeignKey(u'client.id'), nullable=False, index=True)

    bulksender = relationship(u'BulkSender')
    client = relationship(u'Client')


class Client(Model):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, unique=True)
    callback_url = Column(String(200))
    subscription_url = Column(String(200))
    active = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    credit_units = Column(String(30), nullable=False)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime,  index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class ContactGroup(Model):
    __tablename__ = 'contact_group'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    client_id = Column(ForeignKey(u'client.id'), nullable=False, index=True)
    status = Column(Integer, nullable=False, index=True)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime,  index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    client = relationship(u'Client')


class ContactGroupProfile(Model):
    __tablename__ = 'contact_group_profile'
    __table_args__ = (
        Index('contactgroup_id', 'contactgroup_id', 'profile_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    contactgroup_id = Column(ForeignKey(u'contact_group.id'), nullable=False, index=True)
    profile_id = Column(ForeignKey(u'profile.id'), nullable=False, index=True)

    contactgroup = relationship(u'ContactGroup')
    profile = relationship(u'Profile')


class Content(Model):
    __tablename__ = 'content'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    artist_id = Column(ForeignKey(u'artist.id'), nullable=False, index=True)
    status = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime,  index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    artist = relationship(u'Artist')


class ContentService(Model):
    __tablename__ = 'content_service'
    __table_args__ = (
        Index('content_id', 'content_id', 'service_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    content_id = Column(ForeignKey(u'content.id'), nullable=False, index=True)
    service_id = Column(ForeignKey(u'service.id'), nullable=False, index=True)

    content = relationship(u'Content')
    service = relationship(u'Service')


class Contract(Model):
    __tablename__ = 'contract'

    id = Column(Integer, primary_key=True)
    artist_id = Column(ForeignKey(u'artist.id'), nullable=False, unique=True)
    start_date = Column(DateTime, nullable=False, index=True)
    termination = Column(DateTime, index=True)
    end_date = Column(DateTime, nullable=False, index=True)
    status = Column(Integer, nullable=False, index=True)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime,  index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    artist = relationship(u'Artist')


class Inbox(Model):
    __tablename__ = 'inbox'

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    msisdn = Column(String(50), nullable=False)
    short_code_id = Column(ForeignKey(u'short_code.id'), nullable=False, index=True)
    link_id = Column(String(250))
    service_id = Column(ForeignKey(u'service.id'), index=True)
    transaction_id = Column(ForeignKey(u'transaction.id'), nullable=False, index=True)
    profile_id = Column(ForeignKey(u'profile.id'), nullable=False, index=True)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime,  index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    profile = relationship(u'Profile')
    service = relationship(u'Service')
    short_code = relationship(u'ShortCode')
    transaction = relationship(u'Transaction')


class Keyword(Model):
    __tablename__ = 'keyword'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    model = Column(String(100), nullable=False, index=True)
    status = Column(Integer, nullable=False, index=True)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime,  index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class MediaFile(Model):
    __tablename__ = 'media_file'

    id = Column(Integer, primary_key=True)
    content_id = Column(ForeignKey(u'content.id'), nullable=False, unique=True)
    file_name = Column(FileColumn, nullable=False)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime,  index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    content = relationship(u'Content')

    def download(self):
        return Markup(
            '<a href="' + url_for('MediaFilesModelView.download',
                 filename=str(self.file_name)) + '">Download</a>')

    def media_file_name(self):
        return get_file_original_name(str(self.file_name))


class ModelType(Model):
    __tablename__ = 'model_type'
    __table_args__ = (
        Index('name', 'name', 'model', unique=True),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    model = Column(String(150), nullable=False, index=True)
    status = Column(Integer, nullable=False, index=True)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime,  index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Network(Model):
    __tablename__ = 'network'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    status = Column(Integer, nullable=False, index=True)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime,  index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Outbox(Model):
    __tablename__ = 'outbox'

    id = Column(Integer, primary_key=True)
    alert_id = Column(ForeignKey(u'alert.id'), nullable=False, index=True)
    text = Column(String, nullable=False)
    msisdn = Column(String(200), index=True)
    content_id_hash = Column(String(100), index=True)
    ref_number = Column(BigInteger)
    transaction_id = Column(ForeignKey(u'transaction.id'), nullable=False, index=True)
    dlr_status = Column(Integer, nullable=False, index=True)
    processed = Column(Integer, nullable=False, index=True)
    instance_id = Column(Integer, nullable=False, index=True)
    sends = Column(Integer, nullable=False, index=True)
    time_sent = Column(DateTime, index=True)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime, nullable=False, index=True)

    alert = relationship(u'Alert')
    transaction = relationship(u'Transaction')


class Profile(Model):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True)
    msisdn = Column(String(50), nullable=False, unique=True)
    network_id = Column(ForeignKey(u'network.id'), nullable=False, index=True)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime,  index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    network = relationship(u'Network')


class SdpProduct(Model):
    __tablename__ = 'sdp_product'
    __table_args__ = (
        Index('service', 'service', 'product', unique=True),
    )

    id = Column(Integer, primary_key=True)
    service = Column(String(100), nullable=False)
    product = Column(String(100), nullable=False)
    shortcode_id = Column(ForeignKey(u'short_code.id'), nullable=False, index=True)
    keyword_id = Column(ForeignKey(u'keyword.id'), nullable=False, index=True)
    status = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime,  index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    keyword = relationship(u'Keyword')
    shortcode = relationship(u'ShortCode')


class Service(Model):
    __tablename__ = 'service'
    __table_args__ = (
        Index('name_2', 'name', 'service_type_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    client_id = Column(ForeignKey(u'client.id'), nullable=False, index=True)
    keyword_id = Column(ForeignKey(u'keyword.id'), nullable=False, index=True)
    service_type_id = Column(ForeignKey(u'model_type.id'), nullable=False, index=True)
    status = Column(Integer, nullable=False, index=True)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime,  index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    client = relationship(u'Client')
    keyword = relationship(u'Keyword')
    service_type = relationship(u'ModelType')


class ShortCode(Model):
    __tablename__ = 'short_code'

    id = Column(Integer, primary_key=True)
    short_code = Column(String(50), nullable=False, index=True)
    keyword_id = Column(ForeignKey(u'keyword.id'), nullable=False, index=True)
    status = Column(Integer, nullable=False, index=True)
    client_id = Column(ForeignKey(u'client.id'), nullable=False, index=True)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime,  index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    client = relationship(u'Client')
    keyword = relationship(u'Keyword')


class Subscriber(Model):
    __tablename__ = 'subscriber'
    __table_args__ = (
        Index('service_id', 'service_id', 'profile_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    profile_id = Column(ForeignKey(u'profile.id'), nullable=False, index=True)
    service_id = Column(ForeignKey(u'service.id'), nullable=False, index=True)
    status = Column(Integer, nullable=False, index=True)
    transaction_id = Column(ForeignKey(u'transaction.id'), nullable=False, index=True)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime,  index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    profile = relationship(u'Profile')
    service = relationship(u'Service')
    transaction = relationship(u'Transaction')


class Ticket(Model):
    __tablename__ = 'ticket'

    id = Column(Integer, primary_key=True)
    profile_id = Column(ForeignKey(u'profile.id'), nullable=False, unique=True)
    status = Column(Integer, nullable=False, index=True)
    remarks = Column(String(200), nullable=False)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime,  index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    profile = relationship(u'Profile')


class Transaction(Model):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    model = Column(String(50), nullable=False)
    foreign_key = Column(Integer, index=True)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime,  index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class UserClient(Model):
    __tablename__ = 'user_client'

    user_client_id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey(u'ab_user.id'), nullable=False, index=True)
    client_id = Column(ForeignKey(u'client.id'), nullable=False, index=True)

    client = relationship(u'Client')
    user = relationship(u'AbUser')