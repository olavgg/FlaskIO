#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
License: Apache License, Version 2.0
Copyright (C) <2013> <BackupBay>
Created on 4/9/13
@Author: Olav Groenaas Gjerde
"""


class FileHandler(object):

    """
    This class takes care of appending chunks to the specified file that
    is being uploaded. When the upload is complete, the file is then moved
    to its specified path.
    """

    def __init__(self, file_path):
        """
        Constructor that needs a file path
        """
        self.file_path = file_path

    def write_chunk(self):
        """
        Find the file hash in SQLite, append the chunk to the returned file.
        Each chunk will be checksummed to ensure file/data integrity.
        """
        pass

    def create_file_metadata(self):
        """
        Create the file metadata.
        """
        pass

    def move_file(self):
        """
        When upload is complete, move the specified file to its final path.
        """
        pass

    def complete_upload(self):
        """
        Delete entry from the database table in SQLite, and move the file.
        """
        pass