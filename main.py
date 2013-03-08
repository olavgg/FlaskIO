import os
import sys
from flask import Flask, request, redirect, url_for
from flask import send_from_directory

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
        app.config.from_object('conf.config.%s'%(config_type))
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        
        @app.route('/', methods=['GET', 'POST'])
        def upload_file():
            if request.method == 'POST':
                file = request.files['files']
                if file:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                    return redirect(url_for('uploaded_file',
                                            filename=file.filename))
            return '''
                <!doctype html>
                <title>Upload new File</title>
                <h1>Upload new File</h1>
                <form action="" method=post enctype=multipart/form-data>
                  <p><input id='uploader' type='file' name='files' />
                     <input type='submit' value='Upload' />
                </form>
                <output id="list"></output>
                <script>
  function handleFileSelect(evt) {
    var files = evt.target.files; // FileList object

    // files is a FileList of File objects. List some properties.
    var output = [];
    for (var i = 0, f; f = files[i]; i++) {
      output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
                  f.size, ' bytes, last modified: ',
                  f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
                  '</li>');
    }
    document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';
    var bufferSize = 1024*128;
    for (var i = 0, f; f = files[i]; i++) {
        if(f.size <= bufferSize){
            console.log("smaller than buffer size");
            console.log(readChunk(f, 0, f.size));
        } else {
            console.log("larger than buffer size");
            var y = 0;
            for (y=0; (y+bufferSize) < f.size; y+=bufferSize) {
                console.log(y);
                console.log(readChunk(f, y, y+bufferSize));
            }
            console.log(readChunk(f, y, f.size));
        }
    }
  }
  
  function readChunk(file, offset, length) {
    return file.slice(offset, length);
  }

  document.getElementById('uploader').addEventListener('change', handleFileSelect, false);
</script>
                '''
        @app.route('/uploads/<filename>')
        def uploaded_file(filename):
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
                    
        app.run(app.config["HOST"], app.config["PORT"])

if __name__ == '__main__':
    FlaskIOMain.start()