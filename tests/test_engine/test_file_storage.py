#!/usr/bin/python3
"""Defines Unittests for FileStorage class"""

import unittest
import json
from models.user import User
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Test cases for the FileStorage class"""

    def setUp(self):
        """Set up method to initialize instances before tests"""
        self.storage = FileStorage()

    def tearDown(self):
        """Clean up method after each test"""
        del self.storage

    def test__filepath_method(self):
        """Test the '__filepath' method"""
        file_path = self.storage._FileStorage__file_path
        self.assertEqual(file_path, "file.json")

    def test__objects_method(self):
        """Test the '__objects' method"""
        objects = self.storage._FileStorage__objects
        self.assertEqual(objects, {})

    def test_all_method(self):
        """Test the 'all' method"""
        user = User()
        user.name = "Charlie"
        self.storage.new(user)
        all_objects = self.storage.all()
        self.assertIn(f"User.{user.id}", all_objects)

    def test_init_method_with_args(self):
        """Test the '__init__' method with arguments"""
        user = User(id="123", name="David", created_at="2023-01-01T00:00:00")
        self.storage.new(user)
        self.assertIn("User.123", self.storage._FileStorage__objects)

    def test_new_method(self):
        """Test the 'new' method"""
        user = User()
        self.storage.new(user)
        self.assertIn(f"User.{user.id}", self.storage._FileStorage__objects)

    def test_save_method_saves_to_file(self):
        """Test if the 'save' method saves data to a file"""
        user = User()
        user.name = "Alice"
        self.storage.new(user)
        self.storage.save()

        with open(self.storage._FileStorage__file_path, "r") as file:
            data = json.load(file)
            self.assertIn(f"User.{user.id}", data)
            self.assertEqual(data[f"User.{user.id}"]["name"], "Alice")

    def test_reload_method_loads_from_file(self):
        """Test if the 'reload' method loads data from a file"""
        user = User()
        user.name = "Bob"
        self.storage.new(user)
        self.storage.save()

        del self.storage

        new_storage = FileStorage()
        new_storage.reload()

        self.assertEqual(len(new_storage.all()), 1)
        self.assertIn(f"User.{user.id}", new_storage.all())
        self.assertEqual(new_storage.all()[f"User.{user.id}"].name, "Bob")

    def test_save_method_updates_updated_at(self):
        """Test if the 'save' method updates updated_at attribute"""
        user = User()
        self.storage.new(user)
        old_updated_at = user.updated_at
        self.storage.save()

        # Simulate a time delay
        user.name = "New Name"
        self.storage.save()

        new_updated_at = user.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)

    def test_init_method_without_args(self):
        """Test the '__init__' method without arguments"""
        user = User()
        self.storage.new(user)
        obj_id = f"User.{user.id}"
        obj = self.storage.all().get(obj_id)
        self.assertIsInstance(obj, User)

    def test_save_method_does_not_write_to_file(self):
        """Test if the 'save' method updates objects without writing to file"""
        user = User()
        user.name = "Alice"
        self.storage.new(user)
        self.storage.save()

        objects_before_save = self.storage._FileStorage__objects.copy()
        user.name = "Updated Alice"
        self.storage.save()
        objects_after_save = self.storage._FileStorage__objects

        # Ensure that objects don't change after saving without file write
        self.assertEqual(objects_before_save, objects_after_save)

    def test_save_method(self):
        """Test the 'save' method to update objects and not save to file"""
        user = User()
        user.name = "Alice"
        self.storage.new(user)
        self.storage.save()

        objects_before_save = self.storage._FileStorage__objects.copy()
        user.name = "Updated Alice"
        self.storage.save()
        objects_after_save = self.storage._FileStorage__objects

        # Ensure that objects don't change after saving without file write
        self.assertEqual(objects_before_save, objects_after_save)


if __name__ == '__main__':
    unittest.main()
