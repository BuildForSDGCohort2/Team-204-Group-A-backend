from flask import request
import datetime
from . import db


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens.
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, jti):
        self.jti = jti
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.jti)

    def add(self):

        # insert blacklisted token
        db.session.add(self)
        db.session.commit()

    @classmethod
    def check_blacklist(cls, auth_token):
        # check whether auth token has been blacklisted
        res = cls.query.filter_by(jti=str(auth_token)).first()
        return bool(res)
