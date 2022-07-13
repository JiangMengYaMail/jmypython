import numpy as np
import matplotlib
import matplotlib.patches
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from matplotlib.patches import FancyArrowPatch
from math import sqrt, pi, ceil, floor

from colors import *
from markers import *

class Polygon2D():
	def __init__(self, *vertices, color=blue, fill=None, alpha=0.4):
		self.vertices = vertices
		self.color = color
		self.fill = fill
		self.alpha = alpha

	def draw(self):
		if self.color:
			count = len(self.vertices)
			for i in range(0, count):
				x1, y1 = self.vertices[i]
				x2, y2 = self.vertices[(i+1)%count]
				plt.plot([x1,x2], [y1,y2], color=self.color)
		if self.fill:
			pc = PatchCollection([Polygon(self.vertices)], color=self.fill, alpha=self.alpha)
			plt.gca().add_collection(pc)


class Points2D():
	def __init__(self, *vectors, color=black):
		self.vectors = list(vectors)
		self.color = color

	def draw(self):
		xs = [v[0] for v in self.vectors]
		ys = [v[1] for v in self.vectors]
		plt.scatter(xs, ys, color=self.color)


class Arrow2D():
	def __init__(self, tip, tail=(0,0), color=red):
		self.tip = tip
		self.tail = tail
		self.color = color

	def draw(self):
		arrow = FancyArrowPatch((self.tail[0], self.tail[1]), (self.tip[0], self.tip[1]), 
			mutation_scale=15, color=self.color)
		plt.gca().add_patch(arrow)


class Segment2D():
	def __init__(self, s_point, e_point, color=blue):
		self.s_point = s_point
		self.e_point = e_point
		self.color = color

	def draw(self):
		plt.plot((self.s_point[0], self.e_point[0]), (self.s_point[1], self.e_point[1]), color=self.color)


def draw2d(*objects, origin=True, axes=True, grid=(1,1), raw_aspect_ratio=True, width=6, save_as=None):
	vectors = list(extract_vector_2d(objects))
	xs, ys = zip(*vectors)
	max_x, max_y, min_x, min_y = max(0,*xs), max(0,*ys), min(0,*xs), min(0,*ys)

	if grid:
		# draw the range of the axes and leave appropriate white edge
		x_padding = max(grid[0], ceil(0.05*(max_x-min_x)))
		y_padding = max(grid[1], ceil(0.05*(max_y-min_y)))
		plt.xlim(grid[0] * floor((min_x-x_padding)/grid[0]), grid[0] * ceil((max_x+x_padding)/grid[0]))
		plt.ylim(grid[1] * floor((min_y-y_padding)/grid[1]), grid[1] * ceil((max_y+y_padding)/grid[1]))
		
		# draw grid lines. parameters means: min_value, max_value, step_length
		plt.gca().set_xticks(np.arange(plt.xlim()[0], plt.xlim()[1], grid[0]))
		plt.gca().set_yticks(np.arange(plt.ylim()[0], plt.ylim()[1], grid[1]))
		plt.gca().set_axisbelow(True)
		plt.grid(True)
	else:
		x_padding = 0.05*(max_x-min_x)
		y_padding = 0.05*(max_y-min_y)
		plt.xlim(min_x-x_padding, max_x+x_padding)
		plt.ylim(min_y-y_padding, max_y+y_padding)
	
	# draw orgin
	if origin:
		plt.scatter([0], [0], color=black, marker=marker_cross)

	# draw axes
	if axes:
		plt.gca().axhline(linewidth=2, color=black)
		plt.gca().axvline(linewidth=2, color=black)

	# by default, raw_aspect_ratio is true. matplotlib displays the axes in raw ratio, that is 1:1 
	if raw_aspect_ratio:
		height = width * ((plt.ylim()[1]-plt.ylim()[0]) / (plt.xlim()[1]-plt.xlim()[0]))
		plt.gcf().set_size_inches(width, height)

	# draw objects
	for object in objects:
		if type(object) == Polygon2D \
		or type(object) == Points2D \
		or type(object) == Arrow2D \
		or type(object) == Segment2D:
			object.draw()
		else:
			raise TypeError("Unrecognized object: {}".format(object))
	
	# save to file
	if save_as:
		plt.savefig(save_as)
	plt.show()


# helper function to extract all the vectors from a list of objects
def extract_vector_2d(objects):
	for object in objects:
		if type(object) == Polygon2D:
			for vertice in object.vertices:
				yield vertice
		elif type(object) == Points2D:
			for vector in object.vectors:
				yield vector
		elif type(object) == Arrow2D:
			yield object.tip
			yield object.tail
		elif type(object) == Segment2D:
			yield object.s_point
			yield object.e_point
		else:
			raise TypeError("Unrecognized object: {}".format(object))

