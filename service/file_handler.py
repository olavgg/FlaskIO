#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
License: Apache License, Version 2.0
Copyright (C) <2013> <BackupBay>
Created on 4/9/13
@Author: Olav Groenaas Gjerde
"""

from flask import Response
from flask import current_app
from dbhandler import DBHandler


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
        self.db = DBHandler(current_app.config["DBFILE"])
        self.cursor = self.db.getCursor()

    def write_chunk(self):
        """
        Find the file hash in SQLite, append the chunk to the returned file.
        Each chunk will be checksummed to ensure file/data integrity.
        """
        pass

    def create_file_metadata(self, body):
        """
        Create the file metadata.
        """
        if all(k in body for k in ('name','path','size','hash')):
            c = self.db.getCursor()
            if self.db.exists("file", "hash", body['hash']):
                return Response(
                    'File exists\n',
                    status=200, mimetype='text/plain')
            else:
                try:
                    sql = """
                        INSERT INTO file(name, path, size, file_hash)
                        VALUES('{name}','{path}', {size}, '{hash}')
                        """.format(
                        name = body['name'],
                        path = body['path'],
                        hash = body['hash'],
                        size = body['size'])
                    print sql
                    c.execute(sql)
                    self.db.commit()
                except Exception, e:
                    errormsg = \
                        u"Unsuccessful database insert transaction:" \
                        + str(e)
                    print errormsg
                    #log.exception(errormsg, self.__class__.__name__)
                    return Response(
                        'Unsuccessful database insert transaction\n',
                        status=500, mimetype='text/plain')
            return Response('', status=201, mimetype='text/plain')
        return Response(
            'Missing data in JSON\n',
            status=500, mimetype='text/plain')

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