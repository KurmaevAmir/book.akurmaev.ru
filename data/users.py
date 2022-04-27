import datetime
import sqlalchemy
from sqlalchemy import orm

from werkzeug.security import generate_password_hash, \
    check_password_hash
from data.db_session import SqlAlchemyBase
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    parallel_number_student = sqlalchemy.Column(sqlalchemy.Integer,
                                                nullable=True)
    letter = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    rights = sqlalchemy.Column(sqlalchemy.String, default="User")
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    security_code = sqlalchemy.Column(sqlalchemy.String,
                                      nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String,
                                        nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.date.today)
    books = orm.relation("Books", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
