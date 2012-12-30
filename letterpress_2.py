from collections import Counter, defaultdict
import itertools
from termcolor import colored

class Board:
	# 
	def __init__(self, height=5, width=5):
		self.height = height
		self.width = width
		self.tilegrid = [[Tile(self, i, j) for j in range(width)] for i in range(height)]
		self.tileset = Counter()

	def parse(self, board_as_string):
		rows = board_as_string.lower().split(".")
		for i, row in enumerate(rows):
			self.tileset.update(row)
			for j, letter in enumerate(row):
				self.tilegrid[i][j].value = letter

	def contains(self, word):
		return all(self.tileset[l] >= word.counter[l] for l in word.counter)

	def play(self, tiles, player):
		locked = []
		prev_locked = 0
		while True:
			for tile in tiles:
				if not tile.locked():
					tile.owner = player
				else:
					locked.append(tile)
			if len(locked) == prev_locked:
				break
			else:
				prev_locked = len(locked)
				locked = []

	def preview(self, tiles, player):
		saved = [t.owner for t in tiles]
		self.play(tiles, player)
		string = str(self)
		for prev_owner, tile in zip(saved, tiles):
			tile.owner = prev_owner
		return string
		
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
	def __init__(self, word):
		self.word = word.strip().lower()
		self.counter = Counter(self.word)


class Cheater:
	def __init__(self, board, dictionary):
		self.board = board
		self.dictionary = dictionary

		tiledict = defaultdict(list)
		for row in self.board.tilegrid:
			for tile in row:
				tiledict[tile.value].append(tile)

		self.moves = []
		for word in self.dictionary:
			if self.board.contains(word):
				for move in itertools.product(
											*(itertools.combinations(tiledict[l], word.counter[l])
											  for l in word.counter)):
					tiles = list(itertools.chain(*move))
					move = (word, tiles)
					self.moves.append(move)

	def score(self, board, move, player):
		return len(move) + 2 * sum(1 if tile.owner != player else 0 for tile in move)

	def best(self, player, n=10):
		mymoves = [(word, tiles, self.score(self.board, tiles, player)) for (word, tiles) in self.moves]
		mymoves.sort(key=lambda move: move[2], reverse=True)
		return mymoves[:n]


def main():
	player = 'blue'

	letters = raw_input("tiles > ")
	board = Board(5, 5)
	board.parse(letters)
	print board

	print "loading words..."
	words = [Word(w) for w in open("/usr/share/dict/words") if 8 > len(w) > 6]
	print len(words), "words loaded"

	cheater = Cheater(board, words)
	while True:
		moves = cheater.best(player, 5)
		for i, (word, tiles, score) in enumerate(moves):
			print "[", i + 1, "]"
			print "word:", word.word
			print board.preview(tiles, player)
			print "score:", score
			print
		choice = input("choose move > ")
		chosen_move = moves[choice - 1]
		board.play(chosen_move[1], player)
		print "result:"
		print board
		print


if __name__ == '__main__':
	main()



