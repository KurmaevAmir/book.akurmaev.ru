import datetime
import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Books(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    limitation = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    rating = sqlalchemy.Column(sqlalchemy.Float, default=0.5,
                               nullable=True)
    reviews = sqlalchemy.Column(sqlalchemy.Integer, default=0,
                                nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.date.today)
    status = sqlalchemy.Column(sqlalchemy.String, default=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
