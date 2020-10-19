from marshmallow import fields, Schema
import datetime
from . import db

class AppointmentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    details = db.Column(db.String(50), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_appointments():
        return MessageModel.query.all()

    @staticmethod
    def get_one_appointment(id):
        return MessageModel.query.get(id)

    def __repr__(self):
        return '<Appointment {}>'.format(self.id)

class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    start = fields.DateTime(dump_only=True)
    end =fields.DateTime(dump_only=True)
    details = fields.Str(required=True)
    facility_id = fields.Int(dump_only=True)
    patient_id = fields.Int(dump_only=True)
    provider_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
