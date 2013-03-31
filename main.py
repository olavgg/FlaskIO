import os
import sys
from flask import Flask, request, redirect, url_for, render_template, Response
from flask import send_from_directory
import base64
from hashlib import sha256
from service.dbhandler import DBHandler
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
                file = request.files['files']
                if file:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                    return redirect(url_for('uploaded_file',
                                            filename=file.filename))
            return render_template('sample_upload.html')

        @app.route('/create/metadata', methods=["GET"])
        def create_metadata_as_get():
            return render_template('create_metadata.html')

        @app.route('/create/metadata', methods=["PUT"])
        def create_metadata():
            try:
                body = json.loads(request.data)
            except ValueError, e:
                return str(e)+"\n", 500
            if all(k in body for k in ('name','path','size','hash')):
                c = FlaskIOMain.db.getCursor()
                if FlaskIOMain.db.exists("file", "hash", body['hash']):
                    return Response(
                        'File exists\n',
                        status=200, mimetype='text/plain')
                else:
                    try:
                        sql = """
                        INSERT INTO file(name, path, size, hash, complete)
                        VALUES('{name}','{path}', '{hash}', {size},0)
                        """.format(
                            name = body['name'],
                            path = body['path'],
                            hash = body['hash'],
                            size = body['size'])
                        print sql
                        c.execute(sql)
                        FlaskIOMain.db.commit()
                    except Exception, e:
                        errormsg = u"Unsuccessful database insert transaction:"\
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

        @app.route('/complete/metadata/', methods=["GET"])
        def complete_metadata():
            body = json.loads(request.data)
            print body['path']
            if FlaskIOMain.db.exists("file", "name", body['name']):
                return "file exists", 200
            else:
                try:
                    sql = """
                        INSERT INTO file(name, path, size, hash, complete)
                        VALUES('{name}','{path}', '{hash}', {size},0)
                        """.format(
                        name = body['name'],
                        path = body['path'],
                        hash = body['hash'],
                        size = body['size'])
                    print sql
                    FlaskIOMain.cursor.execute(sql)
                    FlaskIOMain.db.commit()
                except Exception, e:
                    errormsg = u"Unsuccessful database insert transaction:" + str(e)
                    print errormsg
                    #log.exception(errormsg, self.__class__.__name__)
                    return "Unsuccessful database insert transaction", 500
            return "", 201

        @app.route('/upload/chunk', methods=['PUT'])
        def upload_chunk():
            data_blob = request.files['chunk'].read()
            fhash = request.headers['Filehash']
            rows = None
            try:
                sql = """
                        SELECT name, path FROM file
                        WHERE hash LIKE '{hash}'
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
            print rows
            b2hash = sha256(data_blob).hexdigest()
            #b2hash = blake2.blake2s(request.data, hashSize=32, key="")
            #byte_array = base64.b64decode(request.data)
            print b2hash
            chunk = open('/tmp/flaskIO.{name}'.format(name=b2hash), 'a')
            chunk.write(data_blob)
            chunk.close()
            return '', 201
                    
        app.run(app.config["HOST"], app.config["PORT"])

if __name__ == '__main__':
    FlaskIOMain.start()