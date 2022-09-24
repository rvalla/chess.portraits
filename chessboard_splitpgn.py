import os

files = [f for f in os.listdir("input/pgn") if not f.startswith(".")]
name = "pgn_source_"
game = 0
for file in files:
	print(file)
	lines = open("input/pgn/" + file).readlines()
	line_number = 0
	s = ""
	while line_number < len(lines):
		while lines[line_number].startswith("["):
			s += lines[line_number]
			line_number += 1
		while not lines[line_number].startswith("["):
			s += lines[line_number]
			line_number += 1
			if line_number == len(lines):
				break
		output = open("input/pgn/" + name + str(game).zfill(5) + ".pgn", "w")
		output.write(s)
		output.close()
		game += 1
		s = ""
