from marshmallow import fields, Schema
import datetime
from . import db

class MessageModel(db.Model):

    # table name 
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.String(140), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # def __init__(self):
    #     """Constructor."""
    #     self.message = data.get('message')
    #     self.sender_id = data.get('sender_id')
    #     self.recipient_id =  data.get('recipient_id')
    #     self.created_at = datetime.datetime.utcnow()
    #     self.modified_at = datetime.datetime.utcnow()


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_messages():
        return MessageModel.query.all()

    @staticmethod
    def get_one_message(id):
        return MessageModel.query.get(id)

    @staticmethod
    def get_all_messages():
        return MessageModel.query.all()

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return MessageModel.query.filter_by(messages_received=self).filter(
            MessageModel.timestamp > last_read_time).count()

    def __repr__(self):
        return '<Message {}>'.format(self.message)

class MessageSchema(Schema):
    id = fields.Int(dump_only=True)
    sender_id = fields.Int(dump_only=True)
    recipient_id=fields.Int(dump_only=True)
    message = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)


