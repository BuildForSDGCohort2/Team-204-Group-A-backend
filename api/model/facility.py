"""
This class holds facility model to store facility details.
"""

from marshmallow import fields, Schema
import datetime
from . import db, bcrypt

class FacilityModel(db.Model):

    # table name 
    __tablename__ = 'facility'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    facilityname = db.Column(db.String(128), nullable=False)
    country = db.Column(db.String(128), nullable=False)
    county = db.Column(db.String(128), nullable=False)
    county = db.Column(db.String(128), nullable=False)
    ward = db.Column(db.String(128), unique=True, nullable=False)
    sublocation = db.Column(db.String(128), nullable=True)
    town = db.Column(db.String(128), nullable=True)
    landmark = db.Column(db.String(128), nullable=True)
    description = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    users = db.relationship('UserModel', backref='facility', lazy='dynamic')

    def __init__(self, data):
        """Constructor."""
        self.facilityname = data.get('facilityname')
        self.country = data.get('country')
        self.county = data.get('county')
        self.subcounty = data.get('subcounty')
        self.ward = data.get('ward')
        self.sublocation = data.get('sublocation')
        self.town = data.get('town')
        self.landmark = data.get('landmark')
        self.description = data.get('description')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_facilities():
        return FacilityModel.query.all()

    @staticmethod
    def get_one_facility(id):
        return FacilityModel.query.get(id)

    @staticmethod
    def get_user_by_facility_name(value):
        return FacilityModel.query.filter_by(facilityname=value).first()

    def __repr__(self):
        return '<Facility: {}>'.format(self.id)

class FacilitySchema(Schema):

    id = fields.Int(dump_only=True)
    facilityname = fields.Str(required=True)
    country = fields.Str(required=True)
    county = fields.Str(required=True)
    subcounty = fields.Str(required=True)
    ward = fields.Str(required=True)
    sublocation = fields.Str(required=True)
    town = fields.Str(required=True)
    landmark = fields.Str(required=True)
    description = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
