import os
import sys
from flask import Flask, request, redirect, url_for, render_template
from flask import send_from_directory
import base64
import pylzma
import blake2

class FlaskIOMain(object):
    
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
        
        @app.route('/', methods=['GET', 'POST'])
        def upload_file():
            if request.method == 'POST':
                file = request.files['files']
                if file:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                    return redirect(url_for('uploaded_file',
                                            filename=file.filename))
            return render_template('sample_upload.html')

        @app.route('/uploads/<filename>')
        def uploaded_file(filename):
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

        @app.route('/upload/chunk/', methods=['POST'])
        def upload_chunk():
            b2hash = blake2.blake2s(request.data, hashSize=32, key="")
            print request.data
            byte_array = base64.b64decode(request.data)
            print byte_array

            b64data = pylzma.decompress(byte_array)
            raw_data = base64.b64decode(b64data)
            open('/tmp/{name}'.format(name=b2hash), 'wb')
                    
        app.run(app.config["HOST"], app.config["PORT"])

if __name__ == '__main__':
    FlaskIOMain.start()