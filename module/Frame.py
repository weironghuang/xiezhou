import time

import scipy.signal as signal
from skimage import measure
import numpy as np


class Frame(object):
	'''单个帧的对象
	属性分别是:
		img: 修正了平场和本底的图片
		center_list: 图片中的星的亮度中心坐标集
		radius_list: 图片中的星的等价半径坐标集
		norm_list": 每颗星相对于其他星的距离坐标集
	center_list, radius_list, norm_list 这三个集合的长度一致, 对应的星一致
	'''

	def __init__(self, img):
		'''Frame的初始化
		Para:
				img: 图片
		'''
		self.id = 0
		self.img = img
		self.img_label = []
		self.center_list = []
		self.radius_list = []
		self.norm_list = []
		self.radian = 0
		self.vector = (0, 0)
		self.rotation_center = (0, 0)
		self.islands = []

	def set_islands(self, sigma, threshold=100):
		img = self.img
		img_med = signal.medfilt(img, (3, 3))
		diff = threshold + 1
		while diff > threshold:
			img_binary = 1 * (img_med > np.median(img) + sigma)
			img_label, label_count = measure.label(
				img_binary, connectivity=1, return_num=1)
			sigma_now = np.std(img[np.where(img_label == 0)])
			diff = np.abs((sigma - sigma_now)/sigma)
			sigma = sigma_now
		self.img_label = img_label
		print('found label:', label_count, end=' ')
		self.islands = [[] for i in range(label_count)]
		h, w = img_label.shape
		for x in range(h):
			for y in range(w):
				if img_label[x, y]:
					self.islands[img_label[x, y]-1].append([x, y])

	def set_center_radius(self, threshold):
		for island in self.islands:
			if len(island) <= (threshold * 2 + 1) ** 2:
				continue
			island = np.array(island)
			x_idx = island[:, 0]
			y_idx = island[:, 1]
			values = self.img[[x_idx, y_idx]]
			x = np.average(x_idx, weights=values)
			y = np.average(y_idx, weights=values)
			self.center_list.append((x, y))
			self.radius_list.append(np.sqrt(len(island)/np.pi))
		print('found island:', len(self.center_list))
		return len(self.center_list)

	def set_norm(self):
		for center in self.center_list:
			norm_list = []
			for other in self.center_list:
				if center is other:
					continue
				vector = np.array(center) - other
				norm = np.linalg.norm(vector)
				norm_list.append(norm)
			self.norm_list.append(norm_list)

	def sort_para(self):
		arg = np.argsort(self.radius_list)[::-1]
		self.center_list = np.array(self.center_list)[arg]
		self.radius_list = np.array(self.radius_list)[arg]
		self.norm_list = np.array(self.norm_list)[arg]