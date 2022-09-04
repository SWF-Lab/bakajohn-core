import utils
import numpy as np


class part_struct:
	def __init__(self):
		self.part = ['']*len(utils.PARTS)
		self.partname = ['']*(len(utils.PARTS)//2)
		self.special = False
		self.mode89 = False
class baka_struct:
	def __init__(self):
		self.type1 = part_struct()
		self.type2 = part_struct()
		self.type3 = part_struct()
		self.typePrev = part_struct()
		self.image1 = np.zeros((utils.HEIGHT, utils.WIDTH, 3), np.uint8)
		self.image2 = np.zeros((utils.HEIGHT, utils.WIDTH, 3), np.uint8)
		self.image3 = np.zeros((utils.HEIGHT, utils.WIDTH, 3), np.uint8)
		