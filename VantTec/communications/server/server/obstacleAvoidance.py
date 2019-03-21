from server import app, COURSES, TEAM_PATTERN # app para agregar rutas
from flask import jsonify, make_response
from random import randint

NUMS = ["1", "2", "3"]
LETTERS = ["X", "Y", "Z"]
NUMS_LEN = len(NUMS) - 1
LETTERS_LEN = len(LETTERS) - 1

@app.route("/obstacleAvoidance/<course>/<teamCode>", methods=["GET"])
def obstacleAvoidance(course=None, teamCode=None):
    '''Funcion para evadir obstaculo por un gate'''
    # validar llamada
    if course is None or teamCode is None:
        return make_response(jsonify(success=False, msg="Request is malformed"), 400)

    # validar curso
    if course in COURSES:
        # validate team
        if TEAM_PATTERN.match(teamCode):
            # status 200
            num = NUMS[randint(0, NUMS_LEN)]
            letter = LETTERS[randint(0, LETTERS_LEN)]
            gate_code = "(" + num + "," + letter + ")"
            return make_response(jsonify(gateCode=gate_code), 200)
    return make_response(jsonify(success=False, msg="Cannot find team or course"), 404)
