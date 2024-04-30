import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Recs(SqlAlchemyBase):
    __tablename__ = 'recs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genres = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    mood = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    user = orm.relationship('User')