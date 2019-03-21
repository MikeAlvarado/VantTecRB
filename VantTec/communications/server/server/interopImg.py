from server import app, upload_file, eprint, COURSES, TEAM_PATTERN # app para las rutas
from flask import request, make_response, after_this_request, jsonify, flash # ver requests recibidas en flask


@app.route("/interop/image/<course>/<teamCode>", methods=["POST"])
def interopImg(course=None, teamCode=None):
    '''Funcion para subir imagen'''
    # validar llamada
    if course is None or teamCode is None:
        return make_response(jsonify(success=False, msg="Request is malformed"), 400)

    if 'file' not in request.files:
        flash('No incluye archivo')
        return make_response(jsonify(succes=False, msg="No incluye archivo"), 400)

    file = request.files['file']

    # validar curso
    if course in COURSES:
        # validar team
        if TEAM_PATTERN.match(teamCode):
            # status 200
            return upload_file(file)
    return make_response(jsonify(success=False, msg="Cannot find team or course"), 404)

@app.route("/interop/report/<course>/<teamCode>", methods=["POST"])
def reportImg(course=None, teamCode=None):
    '''Funcion para reportar forma de imagen'''
    if course is None or teamCode is None:
        return jsonify(status=400, message="Request is malformed")

    if course in COURSES:
        if TEAM_PATTERN.match(teamCode):
            eprint(request.data["shape"])
            return make_response(jsonify(success=True), 200)
    return make_response(jsonify(success=False, msg="Cannot find course or team"), 404)
