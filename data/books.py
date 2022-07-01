import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Books(SqlAlchemyBase, UserMixin):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    publishing_house = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    year_publishing = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    number_of_pages = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
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
