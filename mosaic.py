import os
import cv2
from PIL import Image


#ORIGIN_DIR = 'jiangyue/'
#NEW_DIR = 'jiangyue_new/'
#TEST_DIR = 'jiangyue_test/'

#ORIGIN_DIR = 'youyou/'
#NEW_DIR = 'youyou_new/'
#TEST_DIR = 'youyou_test/'

ORIGIN_DIR = 'niu/'
NEW_DIR = 'niu_new/'
TEST_DIR = 'niu_test/'


def load_origin_images(dirname, new_dirname):
	filenames = os.listdir(dirname)
	print('filenames:', len(filenames))
	for i in range(len(filenames)):
	#for i in range(2): # dev
		filename = os.path.join(dirname, filenames[i])
		new_filename = os.path.join(new_dirname, str(i)+'.jpg')
		print('filename:', filename)
		print('new_filename:', new_filename)
		img = cv2.imread(filename)
		print(img.shape)
		length = min(img.shape[0], img.shape[1])
		if length == img.shape[0]:
			start = int((img.shape[1]-img.shape[0])/2)
			img = img[:, start:start+length]
		else:
			start = int((img.shape[0]-img.shape[1])/2)
			img = img[start:start+length, :]
		print(img.shape)
		img = cv2.resize(img, (200, 200), interpolation=cv2.INTER_AREA)
		print(img.shape)
		cv2.imwrite(new_filename, img)
		#img = Image.open(filename)
		#img.crop((0, 0, 199, 199))
		#img.save(new_filename)


def basic_mosaic(filename):
	from skimage.io import imread
	image = imread(filename)
	import photomosaic as pm
	# Generate a collection of solid-color square images.
	pm.rainbow_of_squares('pool/')
	# Analyze the collection (the "pool") of images.
	pool = pm.make_pool('pool/*.png')
	mos = pm.basic_mosaic(image, pool, (30, 30), depth=1)
	from skimage.io import imsave
	imsave(filename[:-4]+'_basic_mosaic'+filename[-4:], mos)


def mosaic(filename, dirname):
	from skimage.io import imread
	image = imread(filename)
	import photomosaic as pm
	# Analyze the collection (the "pool") of images.
	pool = pm.make_pool(dirname+'/*.jpg')
	print(image.shape)
	mos = pm.basic_mosaic(image, pool, (30, 30), depth=1)
	from skimage.io import imsave
	imsave(filename[:-4]+'_mosaic'+filename[-4:], mos)

	
def mosaic_batch(test_dirname, dirname):
	from skimage.io import imread
	from skimage.io import imsave
	import photomosaic as pm
	# Analyze the collection (the "pool") of images.
	pool = pm.make_pool(dirname+'/*.jpg')
	filenames = os.listdir(test_dirname)
	for filename in filenames:
		if 'mosaic' not in filename and filename.endswith('.jpg'):
			filename = os.path.join(test_dirname, filename)
			image = imread(filename)
			mos = pm.basic_mosaic(image, pool, (int(image.shape[0]/50), int(image.shape[1]/50)), depth=1)
			imsave(filename[:-4]+'_mosaic'+filename[-4:], mos)


def detail_mosaic(filename, dirname):
	from skimage.io import imread
	image = imread(filename)
	# Size the image to be evenly divisible by the tiles.
	from skimage import img_as_float
	image = img_as_float(image)
	# Use perceptually uniform colorspace for all analysis.
	import photomosaic as pm
	converted_img = pm.perceptual(image)
	pool = pm.make_pool(dirname+'/*.jpg')
	# Adapt the color palette of the image to resemble the palette of the pool.
	adapted_img = pm.adapt_to_pool(converted_img, pool)
	scaled_img = pm.rescale_commensurate(adapted_img, grid_dims=(30, 30), depth=1)
	tiles = pm.partition(scaled_img, grid_dims=(30, 30), depth=1)
	annotated_img = pm.draw_tile_layout(pm.rgb(scaled_img), tiles)
	from skimage.io import imsave
	imsave(filename[:-4]+'_detail_mosaic'+filename[-4:], annotated_img)


if __name__ == '__main__':
	#load_origin_images(ORIGIN_DIR, NEW_DIR)
	#basic_mosaic(TEST_DIR+'test1.jpg')
	#mosaic(TEST_DIR+'test3.jpg', NEW_DIR)
	mosaic_batch(TEST_DIR, NEW_DIR)
	#detail_mosaic(TEST_DIR+'test1.jpg', NEW_DIR)
