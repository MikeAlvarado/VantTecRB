import json
import re # modulo de regex
from server import app

@app.route("/", methods=["GET"])
def hello():
    '''Funcion de testing para servidor'''
    return "Hello Vantec!"

@app.route("/followLeader/<course>/<teamCode>", methods=["GET"])
def follow_leader(course, teamCode):
    '''Funcion para iniciar follow de leader challenge'''
    return json.dumps({"success":True, "course": course}), 200, {"ContentType":"application/json"}

@app.route("/heartbeat/<course>/<teamCode>", methods=['POST'])
def heartbeat(course, teamCode):
    '''Funcion heartbeat para log de estatus de bote'''
    return json.dumps({"success":True}), 200, {"ContentType":"application/json"}

@app.route("/run/start/<course>/<teamCode>", methods=['POST'])
def run_start(course, teamCode):
    '''Funcion para empezar el run del bote'''
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/run/end/<course>/<teamCode>", methods=['POST'])
def run_end(course, teamCode):
    '''Funcion para detener el bote'''
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/docking/image/<course>/<teamCode>")
def docking(course, teamCode):
    '''Funcion para mandar docking al bote'''
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}



