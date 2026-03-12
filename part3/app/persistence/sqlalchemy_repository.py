"""
SQLAlchemy repository implementation for database persistence.
"""

from abc import ABC, abstractmethod
from app.persistence.repository import Repository
from app.extensions import db


class SQLAlchemyRepository(Repository):
    """
    SQLAlchemy implementation of the Repository interface.
    This repository will be used for database persistence.
    """

    def __init__(self, model):
        """
        Initialize the repository with a specific model.
        
        Args:
            model: The SQLAlchemy model class this repository handles
        """
        self.model = model
        print(f"Initialized SQLAlchemyRepository for model: {model.__name__}")

    def add(self, obj):
        """
        Add an object to the database.
        
        Args:
            obj: The model instance to add
        """
        try:
            db.session.add(obj)
            db.session.commit()
            print(f"Added {self.model.__name__} with id: {obj.id}")
            return obj
        except Exception as e:
            db.session.rollback()
            print(f"Error adding {self.model.__name__}: {e}")
            raise e

    def get(self, obj_id):
        """
        Get an object by its ID.
        
        Args:
            obj_id: The ID of the object to retrieve
            
        Returns:
            The object if found, None otherwise
        """
        try:
            return self.model.query.get(obj_id)
        except Exception as e:
            print(f"Error getting {self.model.__name__} with id {obj_id}: {e}")
            return None

    def get_all(self):
        """
        Get all objects of this model type.
        
        Returns:
            List of all objects
        """
        try:
            return self.model.query.all()
        except Exception as e:
            print(f"Error getting all {self.model.__name__}: {e}")
            return []

    def update(self, obj_id, data):
        """
        Update an object with new data.
        
        Args:
            obj_id: The ID of the object to update
            data: Dictionary of attributes to update
            
        Returns:
            The updated object if successful, None otherwise
        """
        try:
            obj = self.get(obj_id)
            if obj:
                for key, value in data.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                db.session.commit()
                return obj
            return None
        except Exception as e:
            db.session.rollback()
            print(f"Error updating {self.model.__name__} with id {obj_id}: {e}")
            return None

    def delete(self, obj_id):
        """
        Delete an object by its ID.
        
        Args:
            obj_id: The ID of the object to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            obj = self.get(obj_id)
            if obj:
                db.session.delete(obj)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting {self.model.__name__} with id {obj_id}: {e}")
            return False

    def get_by_attribute(self, attr_name, attr_value):
        """
        Get an object by a specific attribute.
        
        Args:
            attr_name: The attribute name to filter by
            attr_value: The attribute value to match
            
        Returns:
            The first matching object or None
        """
        try:
            return self.model.query.filter(
                getattr(self.model, attr_name) == attr_value
            ).first()
        except Exception as e:
            print(f"Error getting {self.model.__name__} by {attr_name}: {e}")
            return None
