import numpy as np
import matplotlib
import matplotlib.patches
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from matplotlib.patches import FancyArrowPatch
from math import sqrt, pi, ceil, floor
from mpl_toolkits.mplot3d import Axes3D, proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from colors import *
from markers import *


class Points3D():
	def __init__(self, *vectors, color=black):
		self.vectors = vectors
		self.color = color

	def draw(self, cur_ax):
		xs, ys, zs = zip(*self.vectors)
		cur_ax.scatter(xs, ys, zs, color=self.color)

	# end class Points3D


class Polygon3D():
	def __init__(self, *vertices, color=blue):
		self.vertices = vertices
		self.color = color

	def draw(self, cur_ax):
		cnt = len(self.vertices)
		for i in range(0, cnt):
			draw_segment(cur_ax, self.vertices[i], self.vertices[(i+1)%cnt], color=self.color)

	# end class Polygon3D


## https://stackoverflow.com/a/22867877/1704140
class FancyArrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)


class Arrow3D():
	def __init__(self, head, tail=(0,0,0), color=red):
		self.head = head
		self.tail = tail
		self.color = color

	def draw(self, cur_ax):
		xs, ys, zs = zip(self.tail, self.head)
		a = FancyArrow3D(xs,ys,zs, mutation_scale=20,arrowstyle='-|>', color=self.color)
		cur_ax.add_artist(a)
	# end class Arrow3D


class Segment3D():
	def __init__(self, start_p, end_p, color=blue, linestyle='solid'):
		self.start_p = start_p
		self.end_p = end_p
		self.color = color
		self.linestyle = linestyle

	def draw(self, cur_ax):
		draw_segment(cur_ax, self.start_p, self.end_p, color=self.color, linestyle=self.linestyle)

	# end class Segment3D 


class Box3D():
	def __init__(self, vector):
		self.vector = vector

	def draw(self, cur_ax):
		x,y,z = self.vector
		kwargs = {'linestyle':'dashed', 'color':'gray'}
		draw_segment(cur_ax, (0,y,0),(x,y,0),**kwargs)
		draw_segment(cur_ax, (0,0,z),(0,y,z),**kwargs)
		draw_segment(cur_ax, (0,0,z),(x,0,z),**kwargs)
		draw_segment(cur_ax, (0,y,0),(0,y,z),**kwargs)
		draw_segment(cur_ax, (x,0,0),(x,y,0),**kwargs)
		draw_segment(cur_ax, (x,0,0),(x,0,z),**kwargs)
		draw_segment(cur_ax, (0,y,z),(x,y,z),**kwargs)
		draw_segment(cur_ax, (x,0,z),(x,y,z),**kwargs)
		draw_segment(cur_ax, (x,y,0),(x,y,z),**kwargs)

	# end class Box3D


def draw3d(*objects, origin=True, axes=True, width=6, save_as=None, 
	azim=None, elev=None, xlim=None, ylim=None, zlim=None,
	xticks=None, yticks=None, zticks=None, depth_shade=False):
	
	cur_ax = plt.gcf().add_subplot(111, projection='3d')
	cur_ax.view_init(elev=elev, azim=azim) # use default elevation and azimuth
	draw_axes(cur_ax, objects, origin, axes)

	for object in objects:
		if type(object) == Points3D \
		or type(object) == Polygon3D \
		or type(object) == Segment3D \
		or type(object) == Arrow3D \
		or type(object) == Box3D:
			object.draw(cur_ax)
		else:
			raise TypeError("Unrecognized type error: {}".format(object))
	if save_as:
		plt.savefig(save_as)
	plt.show()

	# end draw3d function


def draw_axes(cur_ax, objects, origin=True, axes=True, 
	xlim=None, ylim=None, zlim=None, xticks=None, yticks=None, zticks=None,):

	vectors = list(extract_vectors_3D(objects))
	if origin:
		vectors.append((0,0,0))
	xs, ys, zs = zip(*vectors)
	
	min_x, max_x = min(0, *xs), max(0, *xs)
	min_y, max_y = min(0, *ys), max(0, *ys)
	min_z, max_z = min(0, *zs), max(0, *zs)
	
	x_size = max_x - min_x
	y_size = max_y - min_y
	z_size = max_z - min_z
	
	x_padding = 0.05 * x_size if x_size else 1
	y_padding = 0.05 * y_size if y_size else 1
	z_padding = 0.05 * z_size if z_size else 1

	plot_x_range = (min(min_x - x_padding, -2), max(max_x + x_padding, 2))
	plot_y_range = (min(min_y - y_padding, -2), max(max_y + y_padding, 2))
	plot_z_range = (min(min_z - z_padding, -2), max(max_z + z_padding, 2))

	cur_ax.set_xlabel('x')
	cur_ax.set_ylabel('y')
	cur_ax.set_zlabel('z')

	if axes:
		draw_segment(cur_ax, (plot_x_range[0], 0, 0), (plot_x_range[1], 0, 0), color=black)
		draw_segment(cur_ax, (0, plot_y_range[0], 0), (0, plot_y_range[1], 0), color=black)
		draw_segment(cur_ax, (0, 0, plot_z_range[0]), (0, 0, plot_z_range[1]), color=black)

	if origin:
		cur_ax.scatter([0], [0], [0], color=black, marker=marker_cross)

	if xlim and ylim and zlim:
		plt.xlim(*xlim)
		plt.ylim(*ylim)
		plt.zlim(*zlim)

	if xticks and yticks and zticks:
		plt.xticks(xticks)
		plt.yticks(yticks)
		plt.zticks(zticks)

	# end draw_axes function


def draw_segment(axes, start_p, end_p, color=black, linestyle='solid'):
	xs, ys, zs = [[start_p[i], end_p[i]] for i in range(0,3)]
	axes.plot(xs, ys, zs, color=color, linestyle=linestyle)


# helper function to extract all the vectors from a list of objects
def extract_vectors_3D(objects):
	for object in objects:
		if type(object) == Points3D:
			for v in object.vectors:
				yield v
		elif type(object) == Polygon3D:
			for v in object.vertices:
				yield v
		elif type(object) == Arrow3D:
			yield object.head
			yield object.tail
		elif type(object) == Segment3D:
			yield object.start_p
			yield object.end_p
		elif type(object) == Box3D:
			yield object.vector
		else:
			raise TypeError("Unrecognized object: {}".format(object))

	# end function extract_vectors_3D
