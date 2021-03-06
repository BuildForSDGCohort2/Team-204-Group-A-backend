"""
This class holds user model to store user details.
"""

from marshmallow import fields, Schema
from flask_jwt_extended import get_jwt_identity
import datetime
from . import db, bcrypt
from api.model.facility import FacilityModel
from api.model.message import MessageModel
from api.model.notification import NotificationModel

class UserModel(db.Model):

    # table name 
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_provider = db.Column(db.Boolean, nullable=False, default=False)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'))
    message_sent = db.relationship('MessageModel', foreign_keys='MessageModel.sender_id',backref='author',
                                     lazy='dynamic')
    messages_received = db.relationship('MessageModel', 
                                        foreign_keys='MessageModel.recipient_id',backref='recipient',
                                         lazy='dynamic')

    appointed_provider = db.relationship('AppointmentModel', foreign_keys='Appointment.provider_id',backref='provider',
                                     lazy='dynamic')
    appointed_patient = db.relationship('AppointmentModel', 
                                        foreign_keys='Appointment.patient_id',backref='patient',
                                         lazy='dynamic')
                                         
    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship('NotificationModel', backref='users',
                                    lazy=True)

    def __init__(self, data):
        """Constructor."""
        self.username = data.get('username')
        self.firstname = data.get('firstname')
        self.lastname = data.get('lastname')
        self.email = data.get('email')
        self.is_admin = data.get('is_admin')
        self.is_provider = data.get('is_provider')
        self.password = self.__generate_hash(data.get('password'))
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        self.last_message_read_time = datetime.datetime.utcnow()


    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, value in data.items():
            if key == 'password':
                self.password = self.__generate_hash(value)
            setattr(self, key, value)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_password_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)

    @staticmethod
    def get_user_by_email(value):
        return UserModel.query.filter_by(email=value).first()

    @staticmethod
    def get_user_by_username(value):
        return UserModel.query.filter_by(username=value).first()

    @staticmethod
    def get_providers(value):
        return UserModel.query.join(UserModel.facility).filter(FacilityModel.id == value).all()


    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        notification = NotificationModel(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(notification)
        return notification

    def __repr__(self):
        return '<id {}>'.format(self.username)

class UserSchema(Schema):

    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Email(required=True)
    is_provider = fields.Bool(required=False)
    password = fields.Str(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    facility_id = fields.Int()   
    message = fields.Nested(MessageModel, many=True) 
