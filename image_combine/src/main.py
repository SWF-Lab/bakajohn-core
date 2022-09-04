#-*- coding: utf-8 -*-

import cv2 as cv
import cvzone
import sys
import time
import copy
import numpy as np
import utils
import glob
import os
import json
import base64
from tqdm import trange
from random import randint


import BAKA


# Create 2D list to store parts
list_image_hash = []
basic_files = []
special_files = []

# Create image hash for opencv
hsh = cv.img_hash.BlockMeanHash_create()
# hsh.compute(a_1)
# remove anything from the list that is not a file (directories, symlinks)
# thanks to J.F. Sebastion for pointing out that the requirement was a list 
# of files (presumably not including directories)  

# sort file by modify time
# normal parts
for subDir in utils.PARTS:
	subfiles = list(filter(os.path.isfile, glob.glob(utils.SEARCH_DIR + subDir + "*")))
	subfiles.sort(key=lambda x: os.path.getmtime(x))
	basic_files.append(subfiles)

#special parts
for subDir in utils.SPECIAL_PARTS:
	subfiles = list(filter(os.path.isfile, glob.glob(utils.SEARCH_DIR + subDir + "*")))
	subfiles.sort(key=lambda x: os.path.getmtime(x))
	special_files.append(subfiles)



def produce_image(current_image, current_part, prev_part):
	# remove element by list.pop(INDEX)
	# Change those require by current_part (undone)

	

	# initialize background
	is_duplicate = True
	while(is_duplicate == True):
		
		part_backup = copy.deepcopy(current_part)

		# set if body is special
		if(current_part.mode89 == False and randint(0, 10) < 2):
			# print('special!!')
			current_part.special = True
		else:
			current_part.special = False
	
		b, g, r = randint(0, 256), randint(0, 256), randint(0, 256)
		current_image[:] = (b, g, r)
		image_for_hash = np.zeros((utils.HEIGHT, utils.WIDTH, 3), np.uint8)

		def get_name(fullname):
			result = fullname.split('/')[-1]
			result = result[:-4]
			return result


		# get random file parts if body special
		if(current_part.special):
			current_index = [1, 3, 5, 7, 9]
			# choose body			
			rand_num = randint(0, len(special_files[0])-1)
			part = cv.imread(special_files[0][rand_num], cv.IMREAD_UNCHANGED)
			current_part.part[1] = special_files[0][rand_num]
			current_part.partname[0] = get_name(special_files[0][rand_num])
			current_image = cvzone.overlayPNG(current_image, part, [0, 0])
			image_for_hash = cvzone.overlayPNG(image_for_hash, part, [0, 0])
			
			# get transparent hand
			part = cv.imread(special_files[1][0], cv.IMREAD_UNCHANGED)
			current_part.part[9] = special_files[1][0]
			current_part.partname[4] = get_name(special_files[1][0])
			current_image = cvzone.overlayPNG(current_image, part, [0, 0])
			image_for_hash = cvzone.overlayPNG(image_for_hash, part, [0, 0])
		elif(current_part.mode89):
			current_index = [0, 2, 4, 6, 8]
		else:
			current_index = [1, 3, 5, 7, 9]

		# set else parts
		for i in current_index:
			if(current_part.part[i] != ''):
				part = cv.imread(current_part.part[i], cv.IMREAD_UNCHANGED)
			else:
				rand_num = randint(0, len(basic_files[i])-1)
				while(basic_files[i][rand_num] == prev_part.part[i]):
					# print('rechoose')
					rand_num = randint(0, len(basic_files[i])-1)
				part = cv.imread(basic_files[i][rand_num], cv.IMREAD_UNCHANGED)
				current_part.part[i] = basic_files[i][rand_num]
				current_part.partname[i//2] = get_name(basic_files[i][rand_num])
			# print(i, current_part.part[i])
			current_image = cvzone.overlayPNG(current_image, part, [0, 0])
			image_for_hash = cvzone.overlayPNG(image_for_hash, part, [0, 0])
		
		hash_value = hsh.compute(image_for_hash)
		hash_value = list(hash_value[0])
		# print(hash_value, list_image_hash)
		# print(type(hash_value), type(list_image_hash))
		if(hash_value in list_image_hash):
			current_part = copy.deepcopy(part_backup)
			print('duplicate happen!!')
			is_duplicate = True
		else:
			list_image_hash.append(list(hash_value))
			is_duplicate = False
		# is_duplicate = False

	return current_image, current_part


def pack_to_json(current_num, current_baka):
	# name, id: name or hash, description: maybe fix string, url_ipfs: remain empty, base64: img to base64, part attribute
	
	def generate_base64(img):
		img_encode = cv.imencode('.png', img)[1]
		result = base64.b64encode(img_encode)
		return result
	
	d_1 = {
		'description': 'This is John. He is from Taiwan.',
		'external_url': '',
		'image': 'https://ipfs.io/ipfs/QmcatcXYNN7Vqsnf4aUBDRxo5QyReSvKKVfLESAz3jJ3Hn/BAKAJOHN#' + format(current_num, '03d') + '.png',	# ipfs url
		'image_data': generate_base64(current_baka.image1).decode('utf-8'),	# encode by cv2, decode to str for json
		'name' : 'JOHN #' + format(current_num, '03d'),
		'attributes': [
			{
				'trait_type': 'body', 
				'value': current_baka.type1.partname[0],
			},
			{
				'trait_type': 'expression', 
				'value': current_baka.type1.partname[1],
			},
			{
				'trait_type': 'hair', 
				'value': current_baka.type1.partname[2],
			},
			{
				'trait_type': 'eye', 
				'value': current_baka.type1.partname[3],
			},
			{
				'trait_type': 'hand', 
				'value': current_baka.type1.partname[4],
			},
		],
	}
	d_2 = {
		'description': 'This is John. He is mad.',
		'external_url': '',
		'image': 'https://ipfs.io/ipfs/QmPmS1ve1hZxuZdCQdT71kDRDwuW7aCCwjLAYc6hXDSkzN/BAKAJOHN#' + format(current_num, '03d') + '.png',	# ipfs url
		'image_data': generate_base64(current_baka.image2).decode('utf-8'),
		'name' : 'JOHN #' + format(current_num, '03d'),
		'attributes': [
			{
				'trait_type': 'body', 
				'value': current_baka.type2.partname[0],
			},
			{
				'trait_type': 'expression', 
				'value': current_baka.type2.partname[1],
			},
			{
				'trait_type': 'hair', 
				'value': current_baka.type2.partname[2],
			},
			{
				'trait_type': 'eye', 
				'value': current_baka.type2.partname[3],
			},
			{
				'trait_type': 'hand', 
				'value': current_baka.type2.partname[4],
			},
		],
	}
	d_3 = {
		'description': 'This is BAKJOHN!',
		'external_url': '',
		'image': 'https://ipfs.io/ipfs/QmSo5gd2kYyGTwybtrDu8ipfAzcuPhTbKhy6QwCxz7NgeU/BAKAJOHN#'+ format(current_num, '03d') +'.png',	# ipfs url
		'image_data': generate_base64(current_baka.image3).decode('utf-8'),
		'name' : 'BAKAJOHN #' + format(current_num, '03d'),
		'attributes': [
			{
				'trait_type': 'body', 
				'value': current_baka.type3.partname[0],
			},
			{
				'trait_type': 'expression', 
				'value': current_baka.type3.partname[1],
			},
			{
				'trait_type': 'hair', 
				'value': current_baka.type3.partname[2],
			},
			{
				'trait_type': 'eye', 
				'value': current_baka.type3.partname[3],
			},
			{
				'trait_type': 'hand', 
				'value': current_baka.type3.partname[4],
			},
		],
	}
	return d_1, d_2, d_3


baka = []
for num_img in range(utils.NUM_DISTRIB):
	baka.append(BAKA.baka_struct())

print('baka init finish.')

for num_img in trange(utils.NUM_DISTRIB):
	baka[num_img].image1, baka[num_img].type1 = produce_image(baka[num_img].image1, baka[num_img].type1, baka[num_img].typePrev)
	# cv.imwrite(utils.OUTPUT_PATH + str(num_img) + 'A' + utils.OUTPUT_IMGTYPE, baka[num_img].image1)
	cv.imwrite(utils.OUTPUT_PATH + utils.PROJ_NAME + format(num_img, '03d') + 'A' + utils.OUTPUT_IMGTYPE, baka[num_img].image1)

	baka[num_img].typePrev = copy.deepcopy(baka[num_img].type1)
	baka[num_img].type2.part[0] = baka[num_img].type1.part[1]
	baka[num_img].type2.part[8] = baka[num_img].type1.part[9]
	baka[num_img].type2.partname[0] = baka[num_img].type1.partname[0]
	baka[num_img].type2.partname[4] = baka[num_img].type1.partname[4]	
	baka[num_img].type2.mode89 = True
	baka[num_img].image2, baka[num_img].type2 = produce_image(baka[num_img].image2, baka[num_img].type2, baka[num_img].typePrev)
	# cv.imwrite(utils.OUTPUT_PATH + str(num_img) + 'B' + utils.OUTPUT_IMGTYPE, baka[num_img].image2)
	cv.imwrite(utils.OUTPUT_PATH + utils.PROJ_NAME + format(num_img, '03d') + 'B' + utils.OUTPUT_IMGTYPE, baka[num_img].image2)
	
	baka[num_img].typePrev = copy.deepcopy(baka[num_img].type2)
	baka[num_img].type3.part[2] = baka[num_img].type2.part[2]
	baka[num_img].type3.part[4] = baka[num_img].type2.part[4]
	baka[num_img].type3.part[6] = baka[num_img].type2.part[6]
	baka[num_img].type3.partname[1] = baka[num_img].type2.partname[1]
	baka[num_img].type3.partname[2] = baka[num_img].type2.partname[2]
	baka[num_img].type3.partname[3] = baka[num_img].type2.partname[3]
	# baka[num_img].type3.special = False
	baka[num_img].type3.mode89 = True
	baka[num_img].image3, baka[num_img].type3 = produce_image(baka[num_img].image3, baka[num_img].type3, baka[num_img].typePrev)
	# cv.imwrite(utils.OUTPUT_PATH + str(num_img) + 'C' + utils.OUTPUT_IMGTYPE, baka[num_img].image3)
	cv.imwrite(utils.OUTPUT_PATH + utils.PROJ_NAME + format(num_img, '03d') + 'C' + utils.OUTPUT_IMGTYPE, baka[num_img].image3)
	
	# print(baka[num_img].type1.partname)
	# print(baka[num_img].type2.partname)
	# print(baka[num_img].type3.partname)

	dic = pack_to_json(num_img, baka[num_img])
	# Serializing json
	json_list = [0]*3
	num_to_word = ['A', 'B', 'C']
	for i in range(3):
		json_list[i] = json.dumps(dic[i], indent=4)
		
		# Writing to sample.json
		with open(utils.OUTPUT_PATH + utils.PROJ_NAME + format(num_img, '03d') + num_to_word[i] + '.json', 'w') as outfile:
			outfile.write(json_list[i])
