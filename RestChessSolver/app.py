from flask import Flask, request, abort
from Rest_chess_solver import ApiFields, GameOfChess, Msg
import sys

C_POST = "POST"
C_GET = "GET"
C_CHECK_API = "/api/v1/check/<current_field>"
C_MOVE_API = "/api/v1/<current_field>/<dest_field>"

chess_solver = GameOfChess()
app = Flask(__name__)


@app.route(C_CHECK_API, methods=[C_GET, C_POST])
def check(current_field):
    if request.method == C_POST or request.method == C_GET:
        data = chess_solver.list_available_moves(current_field)

        match data[ApiFields.ERROR]:
            case Msg.ON_EMPTY_FIELD_SELECTED:
                return abort(404, data)
            case Msg.NONEMSG:
                return data


@app.route(C_MOVE_API, methods=[C_GET, C_POST])
def index(current_field, dest_field):
    if request.method == C_POST or request.method == C_GET:

        data = chess_solver.move(current_field, dest_field)

        match data[ApiFields.ERROR]:
            case Msg.ON_ERROR_NO_FIGURE_ON_FIELD:
                return abort(404, data)
            case Msg.NONEMSG:
                return data
            case Msg.NOT_PERMITTED:
                return abort(409, data)


if __name__ == "__main__":
    selectedport = 0
    if len(sys.argv) > 1:
        selectedport = sys.argv[1]
    if selectedport:
        app.run(debug=True, port=sys.argv[1])
    else:
        app.run(debug=True)
