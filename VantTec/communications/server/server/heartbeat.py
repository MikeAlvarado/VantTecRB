from server import app, eprint, COURSES, TEAM_PATTERN # app para agregar rutas
from flask import jsonify, request, make_response
import json

@app.route("/heartbeat/<course>/<teamCode>", methods=["POST"])
def logHeart(course, teamCode):
    '''Funcion para hacer log de heartbeat'''
    if course is None or teamCode is None:
        return make_response(jsonify(success=False, msg="Request malformed"), 400)

    if course in COURSES:
        if TEAM_PATTERN.match(teamCode):
            # data = request.data
            # dataDict = json.loads(data)
            print('--------- HEARTBEAT ---------')
            print(request.form)
            print('-----------------------------')
            return make_response(jsonify(success=True), 200)
    return make_response(jsonify(success=False, msg="Cannot find team or course"), 404)
