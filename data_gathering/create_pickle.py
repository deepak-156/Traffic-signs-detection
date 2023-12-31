'''
Create raw data pickle file
data_raw is a dict mapping image_filename -> [{'class': class_int, 'box_coords': (x1, y1, x2, y2)}, {...}, ...]
'''
import numpy as np
import pickle
import re
import os
from PIL import Image


RESIZE_IMAGE = True 
GRAYSCALE = True 
TARGET_W, TARGET_H = 400, 260 

sign_map = {'stop': 1, 'pedestrianCrossing': 2} 
'''
sign_map = {}  # sign_name -> integer_label
with open('signnames.csv', 'r') as f:
	for line in f:
		line = line[:-1]  # strip newline at the end
		integer_label, sign_name = line.split(',')
		sign_map[sign_name] = int(integer_label)
'''


data_raw = {}


merged_annotations = []
with open('mergedAnnotations.csv', 'r') as f:
	for line in f:
		line = line[:-1]  # strip trailing newline
		merged_annotations.append(line)


image_files = os.listdir('annotations')
for image_file in image_files:
	
	class_list = []
	box_coords_list = []
	for line in merged_annotations:
		if re.search(image_file, line):
			fields = line.split(';')

			
			sign_name = fields[1]
			if sign_name != 'stop' and sign_name != 'pedestrianCrossing':
				continue
			sign_class = sign_map[sign_name]
			class_list.append(sign_class)

			
			box_coords = np.array([int(x) for x in fields[2:6]])

			if RESIZE_IMAGE:
				
				image = Image.open('annotations/' + image_file)
				orig_w, orig_h = image.size

				if GRAYSCALE:
					image = image.convert('L')  # 8-bit grayscale
				image = image.resize((TARGET_W, TARGET_H), Image.LANCZOS)  # high-quality downsampling filter

				resized_dir = 'resized_images_%dx%d/' % (TARGET_W, TARGET_H)
				if not os.path.exists(resized_dir):
					os.makedirs(resized_dir)

				image.save(os.path.join(resized_dir, image_file))

				# Rescale box coordinates
				x_scale = TARGET_W / orig_w
				y_scale = TARGET_H / orig_h

				ulc_x, ulc_y, lrc_x, lrc_y = box_coords
				new_box_coords = (ulc_x * x_scale, ulc_y * y_scale, lrc_x * x_scale, lrc_y * y_scale)
				new_box_coords = [round(x) for x in new_box_coords]
				box_coords = np.array(new_box_coords)

			box_coords_list.append(box_coords)

	if len(class_list) == 0:
		continue 
	class_list = np.array(class_list)
	box_coords_list = np.array(box_coords_list)

	# Create the list of dicts
	the_list = []
	for i in range(len(box_coords_list)):
		d = {'class': class_list[i], 'box_coords': box_coords_list[i]}
		the_list.append(d)

	data_raw[image_file] = the_list

with open('data_raw_%dx%d.p' % (TARGET_W, TARGET_H), 'wb') as f:
	pickle.dump(data_raw, f)
