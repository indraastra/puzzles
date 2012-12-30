"""
The following code models the board and some gameplay features of the 
Letterpress iOS game in order to suggest moves efficiently.

Word games are fun until I start feeling like an inefficient algorithm. This
is an attempt to stave off that feeling by writing an efficient solver, not 
to cheat other players of that fun or the developers out of players.

Sample commands:
  * Load a board:
    > parse C.T.C[red].D.E;A.H.C[red].D.E;A.B.C[red].D.E;A.B.C[red].D.E;A.B.C.D.E
  * Display current board:
    > show
  * Make a move:
    > move blue C(0,0).H(1,1).E(0,4).A(1,0).T(0,1)
  * Cheat:
    > cheat blue

Requires python>=2.7 and termcolor module.
"""

from collections import Counter, defaultdict
import itertools
from termcolor import colored

class Board:
	# 
	def __init__(self, height=5, width=5):
		self.height = height
		self.width = width
		# Matrix-style indexing.
		self.tilegrid = [[Tile(self, i, j) for j in range(width)] for i in range(height)]
		self.tileset = Counter()

	def parse(self, board_text):
		rows = board_text.lower().split(";")
		for i, row in enumerate(rows):
			letters = row.split(".")
			for j, letter in enumerate(letters):
				tile = self.tilegrid[i][j]
				value = letter[0]
				tile.value = value
				self.tileset.update(value)
				# Handle ownership.
				if len(letter) > 1:
					owner = letter[2:-1]
					tile.owner = owner
				else:
					tile.owner = None

	def contains(self, word):
		return all(self.tileset[l] >= word.counter[l] for l in word.counter)

	def play(self, move, player):
		locked = []
		prev_locked = 0
		while True:
			for tile in move.tiles:
				if not tile.locked():
					tile.owner = player
				else:
					locked.append(tile)
			if len(locked) == prev_locked:
				break
			else:
				prev_locked = len(locked)
				locked = []

	def preview(self, move, player):
		saved = [t.owner for t in move.tiles]
		self.play(move, player)
		scores = self.score()
		string = str(self)
		for prev_owner, tile in zip(saved, move.tiles):
			tile.owner = prev_owner
		return (string, scores)

	def score(self):
		scores = Counter()
		for row in self.tilegrid:
			scores.update([tile.owner for tile in row if tile.owner])
		return scores
		
	def tile(self, i, j):
		return self.tilegrid[i][j]

	def __str__(self):
		return "\n".join(["".join([colored(letter.value.upper(), letter.owner or 'white') for letter in row])
										  for row in self.tilegrid])


class Tile:
	def __init__(self, board, i, j, value=None, owner=None):
		self.board = board
		self.i = i
		self.j = j
		self.value = value
		self.owner = owner

	def locked(self):
		if not self.owner: return False
		i = self.i
		j = self.j
		if (i - 1 >= 0) and self.board.tile(i - 1, j).owner != self.owner:
			return False
		if (j - 1 >= 0) and self.board.tile(i, j - 1).owner != self.owner:
			return False
		if (i + 1 < self.board.height) and self.board.tile(i + 1, j).owner != self.owner:
			return False
		if (j + 1 < self.board.width) and self.board.tile(i, j + 1).owner != self.owner:
			return False
		return True

	def __str__(self):
		return "Tile(%d, %d, %s, %s)" % (self.i, self.j, self.value, self.owner)

	def __repr__(self):
		return str(self)


class Word:
	"""A simple representation of a dictionary word."""
	def __init__(self, word_text):
		self.word = word_text.strip().lower()
		self.counter = Counter(self.word)


class Move:
	"""A formation of a Word using Tiles on the board."""
	def __init__(self, word, tiles):
		self.word = word
		self.tiles = tiles

	@classmethod
	def parseFrom(self, tiles_text, board):
		letters = tiles_text.split(".") if "." in tiles_text else [tiles_text]
		values = []
		tiles = []
		for letter in letters:
			values.append(letter[0])
			i, j = letter[2:-1].split(",")
			i = int(i)
			j = int(j)
			tiles.append(board.tilegrid[i][j])
		return Move(Word("".join(values)), tiles)


class Cheater:
	def __init__(self, board, dictionary):
		self.board = board
		self.dictionary = dictionary

		self.tiledict = defaultdict(list)
		for row in self.board.tilegrid:
			for tile in row:
				self.tiledict[tile.value].append(tile)

		# Each word may be formed in multiple ways using the tiles on
		# the board if there are identical tiles. For example, "aa" can be made
		# using "aaa" in (3 choose 2) ways, and "aabb" can be made using "aaabbb"
		# in (3 choose 2) * (3 choose 2) ways. In other words, to find all ways
		# of forming a word, one can take the Cartesian product of combinations
		# of tiles that fulfill the number of required letters.
		self.moves = []
		for word in self.dictionary:
			if self.board.contains(word):
				all_moves = self.genmoves(word)
				for move in all_moves:
					# Flatten tile combinations into list of tiles.
					move = Move(word, list(itertools.chain(*move)))
					self.moves.append(move)

	def genmoves(self, word):
		return itertools.product(
			*(itertools.combinations(self.tiledict[l], word.counter[l])
				for l in word.counter))

	def score(self, move, player):
		# Favors maximizing player's number of tiles possessed while 
		# minimizing opponent's tiles.
		scores = self.board.preview(move, player)[1]
		total = sum(scores.values())
		return scores[player] / float(total)

	def best(self, player, n=10):
		# Sorts the precomputed moves by what works best for the current player
		# and board.
		mymoves = [(move, self.score(move, player)) for move in self.moves]
		mymoves.sort(key=lambda move: move[1], reverse=True)
		return mymoves[:n]


def main():
	player = 'blue'

	print "loading words..."
	words = [Word(w) for w in open("/usr/share/dict/words") if 8 > len(w) > 6]
	print len(words), "words loaded"

	board = Board(5, 5)
	board.parse("A[red].B[red].C[red].D.E;A[red].B[red].C[red].D.E;A.B.C[red].D.E;A.B.C[red].D.E;A.B.C.D.E")
	cheater = Cheater(board, words)

	while True:
		# Handle player move or board update.
		command = raw_input("command > ")
		if command.startswith("cheat"):
			_, player = command.split(" ")
			scored_moves = cheater.best(player)
			for i, (move, score) in enumerate(scored_moves):
				print
				print "[ Move", i + 1, "]"
				print "word:", move.word.word
				print board.preview(move, player)[0]
				print "score:", score

			choice = input("enter move # > ")
			if choice == 0: continue
			chosen_move = scored_moves[choice - 1][0]
			board.play(chosen_move, player)
		elif command.startswith("parse"):
			letters = command.split(" ", 1)[1]
			board.parse(letters)
			cheater = Cheater(board, words)
		elif command.startswith("move"):
			_, player, tiles_text = command.split(" ", 2)
			move = Move.parseFrom(tiles_text, board)
			board.play(move, player)
		elif command.startswith("show"):
			pass
		else:
			continue

		print
		print "[[ Current Board ]]"
		print "#" * 5
		print board
		print "#" * 5
		print


if __name__ == '__main__':
	main()



