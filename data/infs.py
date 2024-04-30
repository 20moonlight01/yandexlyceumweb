import sqlalchemy

from .db_session import SqlAlchemyBase


class Infs(SqlAlchemyBase):
    __tablename__ = 'infs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    summary = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genres = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    mood = sqlalchemy.Column(sqlalchemy.String, nullable=True)