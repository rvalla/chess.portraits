import os
import time as tm
import json as js
import numpy as np
import random as rd
from PIL import Image as im
from chessboard_source import Source
from chessboard_heatmap import Heatmap

class Portrait():
	"The class to build a chessboard portrait"

	def __init__(self, config_file):
		print("Working with configuration store in " + config_file, end="\n")
		self.start_time = tm.time()
		self.config = js.load(open(config_file))
		self.sq_size = self.config["sq_size"]
		self.size = self.sq_size * 8
		self.noise_width = self.load_noise_weight(self.config["noise"], self.config["noise_width"])
		self.output_data = np.full((self.size, self.size, 3), (0,0,0))
		self.input_data = self.build_input_data(self.config["input_path"])
		self.first_sq = self.is_first_square_negative() #0 if false, 1 if true
		print("Source images were loaded...", end="\n")
		self.heatmap = Heatmap(self.config["game_path"], self.get_float_list(self.config["piece_weight"]))
		print("Ready to start painting...", end="\n")
		self.paint_output()
		self.save()
		print("Portraits were saved!", end="\n")
		print("They took me  " + str(self.get_time(self.start_time, tm.time())), end="\n")

	def paint_output(self):
		for s in range(64):
			in_img = rd.choice(self.input_data)
			c, f = divmod(s, 8)
			negative = self.check_negative(c, f)
			start_x = self.sq_size * c
			start_y = self.sq_size * (7 - f) #To iterate following the heatmap squares order...
			for i in range(self.sq_size):
				for j in range(self.sq_size):
					x = start_x + i
					y = start_y + j
					if negative:
						pixel = self.get_pixel(in_img.get_inverted_pixel(x, y), self.heatmap.heatmap[s])
					else:
						pixel = self.get_pixel(in_img.get_pixel(x, y), self.heatmap.heatmap[s])
					self.output_data[x][y] = pixel

	def get_pixel(self, color, sq_weight):
		r = color[0] - round(rd.randint(0,self.noise_width) * sq_weight)
		g = color[1] - round(rd.randint(0,self.noise_width) * sq_weight)
		b = color[2] - round(rd.randint(0,self.noise_width) * sq_weight)
		return (r, g, b)

	def check_negative(self, c, f):
		if (c + f)%2 == self.first_sq:
			return True
		else:
			return False

	def save(self):
		game_data = self.heatmap.get_players_and_date()
		file_name = self.config["output_file"] + "_" + game_data[0] + "_" + game_data[1] + "_" + game_data[2]
		image = im.fromarray(np.array(np.round(self.output_data), dtype="uint8"))
		image.save(self.config["output_path"] + "/" + file_name + ".jpg")
		gray_image = image.convert("L")
		gray_image.save(self.config["output_path"] + "/" + file_name + "_G.jpg")

	def build_input_data(self, input_path):
		ls = []
		input_files = [f for f in os.listdir(input_path) if not f.startswith(".")]
		for img in input_files:
			ls.append(Source(self.sq_size, self.size, im.open(input_path + "/" + img)))
		return ls

	#To decide if the first square is negative (to match a real chessboard)
	def is_first_square_negative(self):
		print("Deciding if first square is negative...", end="\r")
		images_count = len(self.input_data)
		lightness = 0
		for s in self.input_data:
			lightness += s.get_lightness_average()
		if lightness / images_count < 128:
			print("The first square is negative!             ", end="\n")
			return 1
		else:
			print("The first square is not negative!             ", end="\n")
			return 0

	def get_float_list(self, source):
		ls = []
		for v in source.split(","):
			ls.append(float(v))
		return ls

	def load_noise_weight(self, is_noisy, width):
		if is_noisy:
			return width
		else:
			return 0

	#Calculating time needed to processed the portrait..
	def get_time(self, start_time, end_time):
		time = end_time - start_time
		formated_time = self.format_time(time)
		return formated_time

	def format_time(self, time):
		ms = ""
		minutes = time // 60
		seconds = time - minutes * 60
		seconds = round(seconds, 2)
		ms = "{:02d}".format(int(minutes))
		ms += ":"
		ms += "{:05.2f}".format(seconds)
		return ms

	def __str__(self):
		return "Hi, I am a chessboard portrait instance..." + "\n" + \
				"I have a sq_size of " + str(self.sq_size) + "... \n" + \
				"So my output size width is " + str(self.size) + "... \n" + \
				"I have " + str(len(self.input_data)) + " images as my input."
