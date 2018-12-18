import sys
import http.server
import socketserver
from urllib.parse import parse_qs
import json


PORT = int(sys.argv[1])


class ServerHandler(http.server.CGIHTTPRequestHandler):

    known_actions = ["start", "status", "play"]

    def set_headers(self, code, json_data=None):
        if json_data is not None:
            data = json.dumps(json_data)
            self.send_response(code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(bytes(data, 'UTF-8'))
        else:
            self.send_response(code)
            self.end_headers()

    def do_GET(self):
        self.deal_with_request()

    def do_HEAD(self):
        self.set_headers(405)

    def do_POST(self):
        self.set_headers(405)

    def deal_with_request(self):
        relative_path = self.path[1:]
        action, params = self.get_request_params(relative_path)
        if action not in self.known_actions:
            self.set_headers(403)
        else:
            if action == self.known_actions[0]:
                self.start_new_game(params)
            elif action == self.known_actions[1]:
                self.status_of_game(params)
            else:
                self.play_game(params)

    def get_request_params(self, relative_path):
        splitted = relative_path.split("?")
        if len(splitted) == 1:
            return splitted[0], None
        else:
            return splitted[0], splitted[1]

    def start_new_game(self, params):
        param_name = parse_qs(params).get('name')
        if param_name is None:
            game = ttt_container.new_game('')
        else:
            game = ttt_container.new_game(param_name[0])
        self.set_headers(200, {'id': game.id})

    def status_of_game(self, params):
        game = parse_qs(params).get('game')
        if game is None:
            self.set_headers(400, self.create_response_json("bad", "Game ID not present"))
            return
        try:
            game = int(game[0])
        except (TypeError, ValueError):
            self.set_headers(400, self.create_response_json("bad", "Game ID is not a number"))
            return
        try:
            status = ttt_container.get_game_status_with_id(game)
            self.set_headers(200, status)
        except TicTacToesContainerException as e:
            self.set_headers(400, self.create_response_json("bad", str(e)))
            return
        except TicTacToeException as e:
            self.set_headers(200, self.create_response_json("bad", str(e)))
            return

    def play_game(self, params):
        qs_params = parse_qs(params)
        game, player, x, y = self.parse_params(qs_params)
        if game is None or player is None or x is None or y is None:
            self.set_headers(400, self.create_response_json("bad", "parameters are invalid"))
            return
        try:
            game = int(game[0])
            player = int(player[0])
            x = int(x[0])
            y = int(y[0])
        except (TypeError, ValueError):
            self.set_headers(400, self.create_response_json("bad", "Some of params ain't a number"))
            return
        try:
            game = ttt_container.get_game_with_id(game)
            game.move(player, x, y)
            self.set_headers(200, self.create_response_json("ok"))
        except TicTacToesContainerException as e:
            self.set_headers(400, self.create_response_json("bad", str(e)))
            return
        except TicTacToeException as e:
            self.set_headers(200, self.create_response_json("bad", str(e)))
            return

    def parse_params(self, params):
        return params.get("game"), params.get("player"), params.get("x"), params.get("y")

    def create_response_json(self, status, message=None):
        d = {"status": status}
        if message is not None:
            d["message"] = message
        return d


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass


class TicTacToe:
    def __init__(self, ttt_id, name):
        self.id = ttt_id
        self.name = name
        self.board = self.set_new_board()
        self.active_player = 1
        self.game_status = 0
        self.winner = None

    def set_new_board(self):
        return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def move(self, player_id, x, y):
        if self.game_status == 1:
            raise TicTacToeException('Game finished')
        elif not self.is_move_within_board(x, y):
            raise TicTacToeException('Move out of board')
        elif not self.valid_player_turn(player_id):
            raise TicTacToeException('Invalid players turn')
        elif not self.is_place_empty(x, y):
            raise TicTacToeException('Tile is occupied')
        else:
            self.board[y][x] = self.active_player
            if self.is_move_victory(x, y):
                self.game_status = 1
                self.winner = self.active_player
            elif self.is_draw():
                self.game_status = 1
                self.winner = 0
            else:
                self.switch_active_player()

    def valid_player_turn(self, player):
        return self.active_player == player

    def is_move_within_board(self, x, y):
        return 0 <= x < 3 and 0 <= y < 3

    def is_place_empty(self, x, y):
        return self.board[y][x] == 0

    def is_move_victory(self, x, y):
        return (self.board[0][0] == self.board[1][1] == self.board[2][2] and x == y) or \
               (self.board[0][x] == self.board[1][x] == self.board[2][x]) or \
               (self.board[y][0] == self.board[y][1] == self.board[y][2]) or\
               (self.board[0][2] == self.board[1][1] == self.board[2][0] and x + y == 2)

    def is_draw(self):
        for r in self.board:
            for c in r:
                if c == 0:
                    return False
        return True

    def switch_active_player(self):
        if self.active_player == 1:
            self.active_player = 2
        else:
            self.active_player = 1

    def get_next_player(self):
        return self.active_player

    def get_winner(self):
        return self.winner

    def get_status(self):
        return self.game_status


class TicTacToesContainer:
    def __init__(self):
        self.last_used_id = -1
        self.games = {}

    def new_game(self, name):
        self.last_used_id += 1
        game = TicTacToe(self.last_used_id, name)
        self.games[self.last_used_id] = game
        return game

    def get_game_status_with_id(self, game_id):
        game = self.get_game_with_id(game_id)
        if game.get_status() == 1:
            return {'winner': int(game.get_winner())}
        else:
            return {
                'next': game.get_next_player(),
                'board': game.board
            }

    def get_game_with_id(self, ttt_id):
        if ttt_id in self.games.keys():
            return self.games[ttt_id]
        else:
            raise TicTacToesContainerException("Invalid game ID")


class TicTacToesContainerException(Exception):
    pass


class TicTacToeException(Exception):
    pass


ttt_container = TicTacToesContainer()
server = Server(("", PORT), ServerHandler)
print("serving at port", PORT)
server.serve_forever()
