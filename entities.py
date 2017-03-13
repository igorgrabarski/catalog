"""
This file provides the mapping for catalog database tables
"""


from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Category(Base):

    """
    Category class is mapping the category table
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """
        Method serializes the values from the database into
        dictionary of records

        Args:

        Returns:
            dictionary: Dictionary of the record
        """
        return {
            'id':   self.id,
            'name':   self.name
        }


class User(Base):

    """
    User class is mapping the users table
    """
    __tablename__ = 'users'

    id = Column(String(100), primary_key=True)
    user_name = Column(String(100), nullable=False)
    image_url = Column(String(300))
    email = Column(String(100))
    provider = Column(String(50), nullable=False)

    @property
    def serialize(self):
        """
        Method serializes the values from the database into
        dictionary of records

        Args:

        Returns:
            dictionary: Dictionary of the record
        """
        return {
            'id':   self.id,
            'name':   self.user_name,
            'image_url':   self.image_url,
            'email':   self.email
        }


class Item(Base):

    """
    Item class is mapping the item table
    """
    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(String(100), ForeignKey('users.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """
        Method serializes the values from the database into
        dictionary of records

        Args:

        Returns:
            dictionary: Dictionary of the record
        """
        return {
            'id':   self.id,
            'title':   self.name,
            'description':   self.description,
            'cat_id':   self.category_id
        }
