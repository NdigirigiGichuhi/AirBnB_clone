#!/usr/bin/python3
"""
Module that instanctiates object class of FileStorage
"""


from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
