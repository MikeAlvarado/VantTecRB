from server import app, COURSES, TEAM_PATTERN
import json
from flask import jsonify, make_response
from random import randint

COLORS = ["red", "green", "blue"]
SYMBOLS = ["cruciform", "triangle", "circle"]
COLORS_LEN = len(COLORS) - 1
SYM_LEN = len(SYMBOLS) - 1

@app.route("/automatedDocking/<course>/<teamCode>", methods=["GET"])
def automatedDocking(course=None, teamCode=None):
    '''Funcion con curso para automated docking'''
    # validar llamada
    if course is None or teamCode is None:
        return make_response(jsonify(success=False, msg="Request is malformed"), 400)

    # validar curso
    if course in COURSES:
        # validate team
        if TEAM_PATTERN.match(teamCode):
            return json.dumps({
                "dockingBaySequence": [
                    {
                        "symbol": SYMBOLS[randint(0, SYM_LEN)],
                        "color": COLORS[randint(0, COLORS_LEN)]
                    },
                    {
                        "symbol": SYMBOLS[randint(0, SYM_LEN)],
                        "color": COLORS[randint(0, COLORS_LEN)]
                    }
                ]
            }), 200, {"ContentType":"application/json"}
    return make_response(jsonify(success=False, msg="Cannot find team or course"), 404)
