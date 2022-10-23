from chess import parse_square, PIECE_NAMES, \
    RANK_NAMES, FILE_NAMES, Move, Board


class Msg:
    ON_EMPTY_FIELD_SELECTED = "There is no figure on field chosen by you."
    ON_ERROR_NO_FIGURE_ON_FIELD = "there is no figure on chosen field, field is empty"
    NONEMSG = "none"
    NO_MOVES = "no moves avaliable"
    EMPTY_FIELD = "empty_field"
    VALID = "valid"
    INVALID = "invalid"
    NOT_PERMITTED = "Current move is not permitted."


class ApiFields:
    CURRENT_FIELD = "currentField"
    ERROR = "error"
    FIGURE = "figure"
    DEST_FIELD = "destField"
    MOVE = "move"
    AVALIABLE_MOVES = "availableMoves"


class GameOfChess:
    last_move = ""
    figure_name = ""
    exceptions = ""
    emptyfield_flag = False

    answerdict = {
        ApiFields.MOVE: Msg.INVALID,
        ApiFields.FIGURE: "rook",
        ApiFields.ERROR: "",
        ApiFields.CURRENT_FIELD: "H2",
        ApiFields.DEST_FIELD: "H3",
    }

    av_mov_res = {
        ApiFields.AVALIABLE_MOVES: ["a1b2"],
        ApiFields.FIGURE: "rook",
        ApiFields.ERROR: Msg.NOT_PERMITTED,
        ApiFields.CURRENT_FIELD: "H2",
    }
    board = 0

    def __init__(self):
        self.board = Board()

    def get_legal_move(self):
        return self.board.legal_moves

    def get_figure_name_at_field(self, current_position):
        try:
            f_ind = parse_square(str(current_position))
            figure_name = PIECE_NAMES[self.board.piece_type_at(f_ind)]
            self.emptyfield_flag = False
        except Exception as e:
            print("field is empty")
            figure_name = Msg.EMPTY_FIELD
            self.emptyfield_flag = True
            self.exceptions = e.__class__

        return figure_name

    def printboard(self):
        print(self.board)

    def check_possible_moves(self, field):
        p_mov = []
        for name in FILE_NAMES:
            for number in RANK_NAMES:
                if (name + number) != field:
                    move = Move.from_uci(field + name + number)
                    if move in self.board.legal_moves:
                        p_mov.append(field+"->"+name + number)
        return p_mov

    def get_last_move(self):
        return self.last_move

    def list_available_moves(self, field_to_check):

        list_of_avaliable_moves = self.check_possible_moves(field_to_check)

        if list_of_avaliable_moves:
            self.av_mov_res[ApiFields.AVALIABLE_MOVES] = list_of_avaliable_moves
            self.av_mov_res[ApiFields.FIGURE] = self.get_figure_name_at_field(
                field_to_check
            )
            self.av_mov_res[ApiFields.CURRENT_FIELD] = field_to_check
            if self.emptyfield_flag:
                self.av_mov_res[
                    ApiFields.ERROR
                ] = Msg.ON_EMPTY_FIELD_SELECTED
            else:
                self.av_mov_res[ApiFields.ERROR] = Msg.NONEMSG
        else:
            self.av_mov_res[ApiFields.AVALIABLE_MOVES] = Msg.NO_MOVES
            self.av_mov_res[ApiFields.FIGURE] = self.get_figure_name_at_field(
                field_to_check
            )
            self.av_mov_res[ApiFields.CURRENT_FIELD] = field_to_check
            if self.emptyfield_flag:
                self.av_mov_res[
                    ApiFields.ERROR
                ] = Msg.ON_EMPTY_FIELD_SELECTED
            else:
                self.av_mov_res[ApiFields.ERROR] = Msg.NONEMSG
        return self.av_mov_res

    def move(self, movefrom, moveto):
        figure_to_move = self.get_figure_name_at_field(movefrom)
        match self.emptyfield_flag:
            case False:
                move = Move.from_uci(movefrom + moveto)
                self.last_move = movefrom + moveto

                if move in self.board.legal_moves:
                    self.answerdict[ApiFields.FIGURE] = figure_to_move
                    self.answerdict[ApiFields.MOVE] = Msg.VALID
                    self.answerdict[ApiFields.ERROR] = Msg.NONEMSG
                    self.answerdict[ApiFields.DEST_FIELD] = moveto
                    self.answerdict[ApiFields.CURRENT_FIELD] = movefrom
                    self.board.push(move)  # Make the move
                    print("valid move")

                else:
                    self.answerdict[ApiFields.FIGURE] = figure_to_move
                    self.answerdict[ApiFields.MOVE] = Msg.INVALID
                    self.answerdict[ApiFields.ERROR] = Msg.NOT_PERMITTED
                    self.answerdict[ApiFields.DEST_FIELD] = moveto
                    self.answerdict[ApiFields.CURRENT_FIELD] = movefrom
                    print("illegal move")

            case True:
                self.answerdict[ApiFields.FIGURE] = figure_to_move
                self.answerdict[ApiFields.MOVE] = Msg.INVALID
                self.answerdict[ApiFields.ERROR] = Msg.ON_ERROR_NO_FIGURE_ON_FIELD
                self.answerdict[ApiFields.DEST_FIELD] = moveto
                self.answerdict[ApiFields.CURRENT_FIELD] = movefrom
                print(Msg.ON_ERROR_NO_FIGURE_ON_FIELD)

        self.printboard()
        return self.answerdict
