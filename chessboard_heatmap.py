import chess as ch
import chess.pgn as chpgn

class Heatmap():
	"The class to store a chess game heatmap"

	#in chess library piece type are numbers (p = 1, n = 2, b = 3, r = 4, q = 5 and k = 6)
	piece_weight = {1: 1, 2: 3, 3: 3, 4: 5, 5: 9, 6: 9}

	def __init__(self, pgn_path):
		self.game = chpgn.read_game(open(pgn_path))
		self.heatmap = [0 for sq in range(64)]
		self.board = ch.Board()
		self.calculate_heat()

	def calculate_heat(self):
		self.evaluate_board()
		for move in self.game.mainline_moves():
			self.board.push(move)
			self.evaluate_board()
		self.normalize_map()

	def evaluate_board(self):
		for sq in range(64):
			piece = self.board.piece_at(sq)
			if not piece == None:
				if piece.color:
					w = self.get_piece_weight(piece.piece_type)
				else:
					w = -self.get_piece_weight(piece.piece_type)
				self.heatmap[sq] += w

	def get_piece_weight(self, piece):
		return self.piece_weight[piece]

	def normalize_map(self):
		max_w = max(self.heatmap)
		min_w = min(self.heatmap)
		n = max(abs(max_w), abs(min_w))
		for i in range(64):
			self.heatmap[i] = round(self.heatmap[i] / n, 2)

	def save(self, file_path):
		file = open(file_path, "a")
		line = self.game.headers["White"] + ";"
		line += self.game.headers["Black"] + ";"
		line += self.game.headers["Date"].split(".")[0] + ";"
		line += self.heatmap_to_string() + "\n"
		file.write(line)
		file.close()

	def heatmap_to_string(self):
		s = str(self.heatmap[0])
		for w in self.heatmap[1:]:
			s += ","
			s += str(w)
		return s

	def __str__(self):
		return "Hi, I am an the class to make a heatmap from " + self.game.headers["White"] + " vs. " + \
				self.game.headers["Black"] + " (" + self.game.headers["Date"].split(".")[0] + ") " + "\n" + \
				"Here is de heat map: " + self.heatmap_to_string()
