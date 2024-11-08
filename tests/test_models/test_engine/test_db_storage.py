#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pycodestyle
import pep8
import unittest

DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))
    
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_existing_object(self):
        """Test get method retrieves an existing object by class and ID"""
        for class_name, cls in classes.items():
            with self.subTest(class_name=class_name):
                obj = cls()  # Create an instance of the current class
                models.storage.new(obj)
                models.storage.save()
                obj_id = obj.id
                retrieved_obj = models.storage.get(cls, obj_id)
                self.assertEqual(retrieved_obj, obj)
                # Clean up by deleting the object if needed

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_nonexistent_object(self):
        """Test get method returns None for a non-existent object"""
        for class_name, cls in classes.items():
            with self.subTest(class_name=class_name):
                obj = models.storage.get(cls, "nonexistent_id")
                self.assertIsNone(obj)
    
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_all_objects(self):
        """Test count method returns the number of all objects"""
        initial_count = models.storage.count()
        for class_name, cls in classes.items():
            with self.subTest(class_name=class_name):
                obj = cls()
                models.storage.new(obj)
                models.storage.save()
                self.assertEqual(models.storage.count(), initial_count + 1)
                # Increment initial_count by 1 for each class instance added

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_class_specific_objects(self):
        """Test count method returns number of objects for specific class"""
        for class_name, cls in classes.items():
            with self.subTest(class_name=class_name):
                initial_count = models.storage.count(cls)
                obj = cls()
                models.storage.new(obj)
                models.storage.save()
                self.assertEqual(models.storage.count(cls), initial_count + 1)
                # Clean up by deleting the object if needed

class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
