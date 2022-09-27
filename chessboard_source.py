import numpy as np

class Source():
	"The class to store input data for a portrait"

	def __init__(self, sq_size, size, image):
		self.sq_size = sq_size
		self.size = size
		self.img_data = np.array(image)
		print("A new source image is ready...", "\r")

	def get_pixel(self, x, y):
		return self.img_data[x][y]

	def get_inverted_pixel(self, x, y):
		r = 255 - self.img_data[x][y][0]
		g = 255 - self.img_data[x][y][1]
		b = 255 - self.img_data[x][y][2]
		return (r, g, b)

	def get_lightness_average(self):
		pixels = self.sq_size * self.sq_size
		lightness = 0
		for f in range(self.sq_size):
			for c in range(self.sq_size):
				r = int(self.img_data[f][c][0])
				g = int(self.img_data[f][c][0])
				b = int(self.img_data[f][c][0])
				lightness += (r + g + b) / 3
		return lightness / pixels

	def __str__(self):
		return "Hi, I am an image source for a chessboard portrait instance..." + "\n" + \
				"That's all!"
