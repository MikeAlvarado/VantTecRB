from flask import Flask, Response, make_response
from werkzeug.utils import secure_filename
from flask import jsonify, flash # modulo para regresar jsons
import os # acceso al sistema
import uuid # modulo para ids unicos
import sys # usar system path
import re # modulo para regex
# http://flask.pocoo.org/docs/0.12/quickstart/

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static\\uploads')
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jpeg'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

COURSES = set(['courseA', 'courseB', 'openTest'])
TEAM_PATTERN = re.compile("[a-zA-Z]{2,5}$")

def eprint(*args, **kwargs):
    '''Funcion de ayuda para hacer print a consola'''
    print(*args, file=sys.stderr, **kwargs)

def allowed_file(filename):
    '''Checar si la extension del archivo es valida'''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(file):
    '''Funcion para subir archivo'''
    # validar que la llamada tiene archivo
    if file.filename == '':
        flash("No se selecciono archivo")
        return jsonify(error="No se selecciono archivo")

    # validar extension de archivo
    if file and allowed_file(file.filename):
        # crear id para filename
        filename = str(uuid.uuid4())
        extension = '.' + file.filename.rsplit('.', 1)[1].lower()
        # cambiar filename
        file.filename = filename + extension
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        response = make_response(jsonify(id=filename))
        response.headers['Content-Type'] = 'application/json'
        response.headers['Content-Length'] = os.stat(file_path).st_size
        return response
    return make_response(jsonify(success=False, msg="Falta archivo o nombre valido"), 503)

from server.automatedDocking import automatedDocking
from server.obstacleAvoidance import obstacleAvoidance
from server.interopImg import interopImg, reportImg
from server.heartbeat import logHeart
from server.pinger import pingLoc
from server.run import start, end
