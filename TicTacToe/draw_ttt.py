from PIL import Image, ImageDraw
import numpy as np
import pickle

def grid():
	im = Image.new('RGB', (width, width), color_2)
	draw = ImageDraw.Draw(im)
	draw.line([(int(width/3),0),(int(width/3),width)],fill=color_1,width=1)
	draw.line([(int(width/3*2),0),(int(width/3*2),width)],fill=color_1,width=1)
	draw.line([(0,int(width/3)),(width,int(width/3))],fill=color_1,width=1)
	draw.line([(0,int(width/3*2)),(width,int(width/3*2))],fill=color_1,width=1)
	return im, draw

def create_collage(width, height, images):
	cols = 9
	rows = 2
	space = 10
	thumbnail_width = (width-space*(cols-1))//cols
	thumbnail_height = (height-space*(rows-1))//rows
	size = thumbnail_width, thumbnail_height
	new_im = Image.new('RGB', (width, height),'white')
	ims = []

	for p in images:
		p.thumbnail(size)
		ims.append(p)
	i = 0
	x = 0
	y = 0
	for col in range(cols):
		for row in range(rows):
			print(i, x, y)
			new_im.paste(ims[i], (x, y))
			i += 1
			y += thumbnail_height+space
		x += thumbnail_width+space
		y = 0

	new_im.save("/Users/admin/Desktop/Collage.png")

width = 180
color_1 = (0, 0, 0)
color_2 = (255, 255, 255)
side = int(width/12)
for l in range(0,1):
	fr1 = open('/Users/admin/Desktop/moves{}'.format(str(l)), 'rb')
	# fr1 = open('/Users/admin/Desktop/RandomML-master/perfect_minimax/v9/moves5000_all_same_diff_from_6000/moves_0'.format(str(l)), 'rb')
	fr2 = open('/Users/admin/Desktop/moves2'.format(str(l)), 'rb')
	moves1 = pickle.load(fr1)
	moves2 = pickle.load(fr2)
	fr1.close()
	fr2.close()

	idx = moves1
	idx2 = moves2
	images = []
	steps = 0
	for j in range(len(idx)):
		steps += 1
		im, draw = grid()
		im2, draw2 = grid()
		for i in range(steps):
			# print(board[idx[0][i],idx[1][i]])
			x1 = (idx[i][1]*4+1)*side
			y1 = ((idx[i][0])*4+1)*side
			x2 = (idx[i][1]*4+3)*side
			y2 = ((idx[i][0])*4+3)*side
			if i%2==0:
				draw.line([(x1,y1),(x2,y2)],fill=color_1,width=1)
				draw.line([(x1,y2),(x2,y1)],fill=color_1,width=1)
			else:
				draw.ellipse([(x1,y1),(x2,y2)],fill=color_2,outline=color_1)
			x1 = (idx2[i][1]*4+1)*side
			y1 = ((idx2[i][0])*4+1)*side
			x2 = (idx2[i][1]*4+3)*side
			y2 = ((idx2[i][0])*4+3)*side
			if i%2==0:
				draw2.line([(x1,y1),(x2,y2)],fill=color_1,width=1)
				draw2.line([(x1,y2),(x2,y1)],fill=color_1,width=1)
			else:
				draw2.ellipse([(x1,y1),(x2,y2)],fill=color_2,outline=color_1)
		images.append(im)
		images.append(im2)
	# images[0].save('/Users/admin/Desktop/moves_{}.gif'.format(str(l)),
	# 			   save_all=True, append_images=images[1:], optimize=False, duration=750, loop=0)

	# for k in range(len(moves1)):
	# 	idx = moves1[k]
	# 	images = []
	# 	steps = 0
	# 	for j in range(len(idx)):
	# 		steps += 1
	# 		im, draw = grid()
	# 		for i in range(steps):
	# 			# print(board[idx[0][i],idx[1][i]])
	# 			x1 = (idx[i][1]*4+1)*side
	# 			y1 = ((idx[i][0])*4+1)*side
	# 			x2 = (idx[i][1]*4+3)*side
	# 			y2 = ((idx[i][0])*4+3)*side
	# 			if i%2==0:
	# 				draw.line([(x1,y1),(x2,y2)],fill=color_1,width=1)
	# 				draw.line([(x1,y2),(x2,y1)],fill=color_1,width=1)
	# 			else:
	# 				draw.ellipse([(x1,y1),(x2,y2)],fill=color_2,outline=color_1)
	# 		images.append(im)
		# images[0].save('/Users/admin/Desktop/moves_{}.gif'.format(str(l)),
		# 			   save_all=True, append_images=images[1:], optimize=False, duration=750, loop=0)

create_collage(980, 210, images)