import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'category'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)



