import os
import sys
from flask import Flask, request, redirect, url_for, render_template, Response
from hashlib import sha256
from service.dbhandler import DBHandler
from service.file_handler import FileHandler

import json

class FlaskIOMain(object):

    @staticmethod
    def initDB(app):
        FlaskIOMain.db = DBHandler(app.config["DBFILE"])
        FlaskIOMain.cursor = FlaskIOMain.db.getCursor()
    
    @staticmethod
    def start():
        UPLOAD_FOLDER = '/tmp'
        ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
        
        config_type='DevelopmentConfig'
        if len(sys.argv) == 2:
            if sys.argv[1] == "dev":
                config_type='DevelopmentConfig'
            elif sys.argv[1] == "test":
                config_type='TestConfig'
            elif sys.argv[1] == "prod":
                config_type='ProductionConfig'
        app = Flask(__name__)
        app.config.from_object('conf.config.{0:>s}'.format(config_type))
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        FlaskIOMain.initDB(app)
        
        @app.route('/', methods=['GET', 'POST'])
        def upload_file():
            if request.method == 'POST':
                file_obj = request.files['files']
                if file_obj:
                    file_obj.save(os.path.join(app.config['UPLOAD_FOLDER'], file_obj.filename))
                    return redirect(url_for('uploaded_file',
                                            filename=file_obj.filename))
            return render_template('sample_upload.html')

        @app.route('/create/metadata', methods=["GET"])
        def create_metadata_as_get():
            return render_template('create_metadata.html')

        @app.route('/create/metadata', methods=["PUT"])
        def create_metadata():
            try:
                body = json.loads(request.data)
            except ValueError, e:
                return Response((e)+"\n", status=500, mimetype='text/plain')
            fh = FileHandler()


        @app.route('/complete/upload', methods=["POST"])
        def complete_upload():
            body = json.loads(request.data)
            print body
            try:
                sql = "DELETE FROM file WHERE file_hash LIKE '{hash}'".format(
                    hash = body['hash'])
                print sql
                FlaskIOMain.cursor.execute(sql)
                FlaskIOMain.db.commit()
            except Exception, e:
                description = u"Unsuccessful database delete transaction:"
                errormsg =  description + str(e)
                print errormsg
                #log.exception(errormsg, self.__class__.__name__)
                return Response(description, status=500, mimetype='text/plain')
            return Response('', status=202, mimetype='text/plain')

        @app.route('/upload/chunk', methods=['PUT'])
        def upload_chunk():
            data_blob = request.files['chunk'].read()
            fhash = request.headers['Filehash']
            chash = request.headers['Chunkhash']
            rows = None
            try:
                sql = """
                        SELECT name, path FROM file
                        WHERE file_hash LIKE '{hash}'
                        """.format(hash=fhash)
                print sql
                rows = list(FlaskIOMain.cursor.execute(sql))
            except Exception, e:
                errormsg = u"Unsuccessful database insert transaction:" + str(e)
                print errormsg
                #log.exception(errormsg, self.__class__.__name__)
                return Response(
                    "Unsuccessful database insert transaction",
                    status=500, mimetype='text/plain')
            if len(rows) > 0 and chash == sha256(data_blob).hexdigest():
                chunk = open('/tmp/{name}'.format(name=rows[0][0]), 'a')
                chunk.write(data_blob)
                chunk.close()
            else:
                return render_error("Chunk is invalid")
            return '', 201

        def render_error(msg):
            return Response(msg+'\n', status=500, mimetype='text/plain')
                    
        app.run(app.config["HOST"], app.config["PORT"])

if __name__ == '__main__':
    FlaskIOMain.start()