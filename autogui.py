import pyautogui
import cv2
import numpy as np
import PIL
import pretty_midi
from PIL import Image, ImageChops, ImageDraw

MAX_NOTE = 40

def compare_images(path_one, path_two, diff_save_location):
    """
    Compares to images and saves a diff image, if there
    is a difference
 
    @param: path_one: The path to the first image
    @param: path_two: The path to the second image
    """
    image_one = Image.open(path_one)
    image_two = Image.open(path_two)
 
    diff = ImageChops.difference(image_one, image_two)
 
    if diff.getbbox():
        diff.save(diff_save_location)

def draw_rec(file_name,out_file,x1,x2,y1,y2):
	source_img = Image.open(file_name).convert("RGBA")

	draw = ImageDraw.Draw(source_img)
	draw.rectangle(((x1, y1), (x2, y2)), outline='black')
	draw.text((20, 70), "something123", font=ImageFont.truetype("font_path123"))

	source_img.save(out_file, "JPEG")

class autoGUI():

	def __init__(self):
		super().__init__()
		self.init_gen()

	def init_gen(self):
		self.window_size = pyautogui.size()
		self.area_sample = 'area_sample.png'
		self.time2len = 100
		self.screenshot = None #the temp screen_shot
		self.screenshot1 = None #used to compare with self.screenshot2
		self.screenshot2 = None #used to compare with self.screenshot1
		
		#the left/right/top/bottom coordinate for the current selct note
		self.left = 0
		self.right = 0
		self.top = 0
		self.bottom = 0
		
		self.start_pos = [0,0] #the width/height of the first note, used for pitch_reset
		self.zero_pos = [0,0] #the width/height of time 0, used for sep_operation
		self.interval = 18 #the length of 1 pitch
		self.note_num = MAX_NOTE #total number of note in the source audio
		self.midi = None
		self.pitch_list = [] #pitch list from midi file
		self.time_list = [] #time list from midi file
		self.sep_point = [] #the seperation point from source audio
		self.beat = 121 #the length of 1 beat (1/4 bar)
		self.init_func_pos()

	def init_func_pos(self):
		self.blank = [121,376]
		self.edit = [193,12]
		self.undo = [193,34]
		self.sep_tool = [218,282]
		self.pitch_tool = [126,282]
		self.select_tool = [102,282]

	#count the total number of note in the source audio and store the position of each note
	def note_count(self):
		pyautogui.click(x=self.start_pos[0],y=self.start_pos[1])
		ct = 0
		while self.right != 0 and self.bottom != 0 and ct <= MAX_NOTE:
			self.find_select_area2()
			self.sep_point.append([self.left,self.right,self.top,self.bottom])
			ct += 1
		self.note_num = ct
		print(ct)
		print(self.sep_point)
		return

	#get the length of one block. Used for auto pitch shift
	def note_duration(self, pic):
		img = Image.open(pic)
		self.beat = img.width
		self.interval = img.height
		return width

	#move a single note to the pitch of the first note
	def single_pitch_reset(self,note_index):
		#self.find_select_area2() #select next note and update the note position
		#self.sep_point.append([self.left,self.right]) #store the seperation point
		#pyautogui.click(x=self.pitch_tool[0],y=self.pitch_tool[1]) #select the pitch tool
		pyautogui.press('right') #move to next note
		self.left = self.sep_point[note_index][0]
		self.right = self.sep_point[note_index][1]
		self.top = self.sep_point[note_index][2]
		self.bottom = self.sep_point[note_index][3]
		y = int((self.top + self.bottom)/2)
		y_shift = int(round((y - self.start_pos[1])/self.interval))
		print(y,y_shift)
		if y_shift >= 0:
			for i in range(y_shift):
				pyautogui.hotkey('command','up')
		else:
			y_shift = abs(y_shift)
			for i in range(y_shift):
				pyautogui.hotkey('command','down')
		return

	#move all note to the pitch of the first note
	def pitch_reset(self):
		pyautogui.click(x=self.blank[0],y=self.blank[1])
		pyautogui.click(x=self.start_pos[0],y=self.start_pos[1])
		pyautogui.keyDown('shift')
		for i in range(self.note_num):
			pyautogui.keyDown('right')
			pyautogui.keyUp('right')
		pyautogui.keyUp('shift')
		pyautogui.click(x=self.pitch_tool[0],y=self.pitch_tool[1])
		pyautogui.doubleClick(x=self.start_pos[0],y=self.start_pos[1]) #auto pitch correction
		pyautogui.click(x=self.blank[0],y=self.blank[1])
		pyautogui.click(x=self.start_pos[0],y=self.start_pos[1])
		for i in range(self.note_num-1):
			self.single_pitch_reset(i)
		return


	#C -- 60 (pitch_list centered at C)
	#start -- index of start note; end -- index of end note
	def pitch_modulation(self,start,end):
		pyautogui.click(x=self.blank[0],y=self.blank[1])
		pitch_list = []
		duration = end - start + 1
		for i in range(duration):
			pitch_list.append(self.pitch_list[start+i]-self.pitch_list[start])
		for i in range(len(pitch_list)):
			if pitch_list[i] >= 0:
				for j in range(pitch_list[i]):
					pyautogui.press('ctrlup')
			else:
				for j in range(abs(pitch_list[i])):
					pyautogui.press('ctrldown')
			pyautogui.press('right')
		return

	#use cv2 to find the contour. return the minimum square cover of the select area
	def find_select_area(self):
		candidate = []
		self.screenshot = pyautogui.screenshot()
		#img = cv2.imread('sample9.png') #should be replaced by the temp screenshot 
		img = self.screenshot
		print(type(img))
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		ret,binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
		contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		print(len(contours))
		for i in range(len(contours)):
			draw_img0 = cv2.drawContours(img.copy(),contours,i,(0,255,255),1)
			x, y, w, h = cv2.boundingRect(contours[i])
			if w>=30 and w <= 150 and h>=20 and h<=50:
				print(w,h,i)
				candidate.append([x, y, w, h])
				cv2.rectangle(draw_img0, (x,y), (x+w,y+h), (153,153,0), 1)
				cv2.imwrite("draw_img_"+str(i)+'.jpg', draw_img0)
		# draw_img0 = cv2.drawContours(img.copy(),contours,130,(0,255,255),3)
		# x, y, w, h = cv2.boundingRect(contours[i])
		# cv2.rectangle(draw_img0, (x,y), (x+w,y+h), (153,153,0), 1)
		# cv2.imwrite("draw_img"+str(i)+'.jpg', draw_img0)
		cv2.imwrite("img.jpg", img)
		#x, y, w, h = cv2.boundingRect(cnt)
		#cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
		return candidate #return the candidate rectangles

	#use diff to find the select area (very accurate)
	def find_select_area2(self):
		#pyautogui.click()
		self.screenshot1 = pyautogui.screenshot()
		img1 = self.screenshot1.convert('RGB')
		open_cv_image1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)
		cv2.imwrite("screenshot1.jpg",open_cv_image1)
		pyautogui.press('right')
		self.screenshot2 = pyautogui.screenshot()
		img2 = self.screenshot2.convert('RGB')
		open_cv_image2 = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2BGR)
		cv2.imwrite("screenshot2.jpg",open_cv_image2)
		width = img1.width
		height = img1.height
		diff_coor = []
		diff_value = []
		target_coor = []
		target_value = []
		left = width
		#print(width)
		right = 0
		top = height
		#print(height)
		bottom = 0
		for x in range(width):
			for y in range(height):
				pixel1 = img1.getpixel((x,y))
				pixel2 = img2.getpixel((x,y))
				if pixel1 != pixel2 and (int(pixel1[1])-int(pixel2[1])) > 0:
					diff_coor.append([x,y])
					diff_value.append([pixel1[0]-pixel2[0],pixel1[1]-pixel2[1],pixel1[2]-pixel2[2]])
					if y > self.start_pos[1]*2 - 50 and y < self.start_pos[1]*2 + 50:
						if x < left:
							left = x
						if x > right:
							right = x
						if y < top:
							top = y
						if y > bottom:
							bottom = y
					# if  (pixel1[0]-pixel2[0])>(1.5*pixel1[1]-pixel2[1]):
					# #if pixel2[0] > 1.5*pixel2[1]:
					# 	target_coor.append([x,y])
					# 	target_value.append([pixel1[0]-pixel2[0],pixel1[1]-pixel2[1],pixel1[2]-pixel2[2]])
					# 	if x < left:
					# 		left = x
					# 	if x > right:
					# 		right = x
					# 	if y < top:
					# 		top = y
					# 	if y > bottom:
					# 		bottom = y
		self.left = int(left/2)
		self.right = int(right/2)
		self.top = int(top/2)
		self.bottom = int(bottom/2)
		#print(diff_coor)
		print("")
		#print(diff_value)
		print(left,right,top,bottom)
		#print(target)
		#compare_images("screenshot1.jpg","screenshot2.jpg","diff.jpg")
		return

	#use diff to find the first note
	def find_first_note(self):
		pyautogui.click(x=self.select_tool[0],y=self.select_tool[1])
		pyautogui.press('right')
		self.screenshot1 = pyautogui.screenshot()
		img1 = self.screenshot1.convert('RGB')
		open_cv_image1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)
		cv2.imwrite("screenshot1.jpg",open_cv_image1)
		pyautogui.press('left')
		self.screenshot2 = pyautogui.screenshot()
		img2 = self.screenshot2.convert('RGB')
		open_cv_image2 = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2BGR)
		cv2.imwrite("screenshot2.jpg",open_cv_image2)
		width = img1.width
		height = img1.height
		diff_coor = []
		diff_value = []
		target_coor = []
		target_value = []
		left = width
		#print(width)
		right = 0
		top = height
		#print(height)
		bottom = 0
		for x in range(width):
			for y in range(height):
				pixel1 = img1.getpixel((x,y))
				pixel2 = img2.getpixel((x,y))
				if pixel1 != pixel2 and (int(pixel1[1])-int(pixel2[1])) > 0:
					diff_coor.append([x,y])
					diff_value.append([pixel1[0]-pixel2[0],pixel1[1]-pixel2[1],pixel1[2]-pixel2[2],x,y])
					if  (pixel1[0]-pixel2[0])>(1.5*pixel1[1]-pixel2[1]):
					#if pixel2[0] > 1.5*pixel2[1]:
						target_coor.append([x,y])
						target_value.append([pixel1[0]-pixel2[0],pixel1[1]-pixel2[1],pixel1[2]-pixel2[2]])
						if x < left:
							left = x
						if x > right:
							right = x
						if y < top:
							top = y
						if y > bottom:
							bottom = y
		self.left = int(left/2)
		self.right = int(right/2)
		self.top = int(top/2)
		self.bottom = int(bottom/2)
		self.start_pos[0] = int((self.left+self.right)/2)
		self.start_pos[1] = int((self.top+self.bottom)/2)
		self.sep_point.append([self.left,self.right,self.top,self.bottom])
		self.zero_pos = [self.left,self.start_pos[1]]
		#print(diff_coor)
		print("")
		#print(diff_value)
		# for e in diff_value:
		# 	if e[4] == 1066 or e[4] == 1067 or e[4] == 1068:
		# 		print(e)
		print(self.start_pos[0],self.start_pos[1])
		#print(target)
		#compare_images("screenshot1.jpg","screenshot2.jpg","diff.jpg")
		return

	#remove a separation if it supposed not be a sep
	def note_sep(self,x1,y1):
		pyautogui.click(x=self.blank[0],y=self.blank[1])
		#moveToX = self.left/2
		#moveToY = (self.top+self.bottom)/4
		moveToX = x1
		moveToY = y1
		secs_between_clicks = 0.2
		#pyautogui.click(x=self.sep_tool[0],y=self.sep_tool[1]) #select the sep tool
		pyautogui.doubleClick(x=moveToX, y=moveToY, interval=secs_between_clicks) #remove/add seperation
		#due to the software problem, we need "undo" once to make it work
		pyautogui.click(x=self.edit[0],y=self.edit[1])
		pyautogui.click(x=self.undo[0],y=self.undo[1])
		return

	#get the pitch list from the midi file, store in self.pitch_list and self.time_list
	def melody(self):
		speed = 1.25 #adjust the speed of music, slow when speed>1
		# Load MIDI file into PrettyMIDI object
		midi_data = pretty_midi.PrettyMIDI(self.midi)
		instrument = midi_data.instruments[0]
		print(instrument.name)
		start = []
		end = []
		for note in instrument.notes:
			start.append(note.start*speed)
			end.append(note.end*speed)
			self.pitch_list.append(note.pitch)
		zipped = list(zip(self.pitch_list, start, end))
		sorted(zipped, key=lambda x: x[1])
		self.pitch_list = []
		for i in range(len(zipped)):
			self.pitch_list.append(zipped[i][0])
			self.time_list.append(zipped[i][1:])
		print(len(self.pitch_list))
		print(len(self.time_list))
		return

	#execute seperation operation to make seperation correct
	def sep_operation(self):
		error = 10
		pyautogui.click(x=self.sep_tool[0],y=self.sep_tool[1])
		std = [] #the standard sep point from midi file
		source = [] #the source audio sep point
		ope_list = [] #the point need to use seperation tool
		# for i in range(len(self.time_list)):
		# 	std.append(self.time_list[i][1])
		for i in range(len(self.time_list)-19):
			time = self.time_list[i+18][1] - self.time_list[18][0]
			std.append(time)
		for i in range(len(self.sep_point)-2):
			if abs(self.sep_point[i+1][0] - self.sep_point[i][0]) < error:
				self.sep_point[i+1][0] = self.sep_point[i][1]
			elif abs(self.sep_point[i+1][1] -self.sep_point[i][1]) < error:
				self.sep_point[i][1] = self.sep_point[i+1][0]
			elif self.sep_point[i+1][0] < self.sep_point[i][1]:
				temp = int(self.sep_point[i+1][0])
				self.sep_point[i+1][0] = self.sep_point[i][1]
				self.sep_point[i][0] = temp
		for i in range(len(self.sep_point)-1):
			time_point = ((self.sep_point[i+1][0]+self.sep_point[i][1])/2 - self.zero_pos[0])/self.beat
			source.append(time_point)

		ct_std = 0
		ct_source = 0
		bound = min(max(std),source[-2]) #exclued the last term
		while ct_std < len(std) and ct_source < len(source) and source[ct_source] < bound and std[ct_std] < bound:
			if abs(source[ct_source] - std[ct_std]) <= 0.1: #no need to do operation
				ct_std += 1
				ct_source += 1
			elif (source[ct_source] - std[ct_std]) > 0.1: #missing seperation
				ope_list.append([std[ct_std],0])
				ct_std += 1
			else: #unnecessary seperation
				ope_list.append([source[ct_source],1])
				ct_source += 1
		if ct_std == len(std):
			while ct_source < len(source) and source[ct_source] < bound:
				ope_list.append([source[ct_source],1])
				ct_source += 1
		else:
			while ct_std < len(std) and std[ct_std] < bound:
				ope_list.append([std[ct_std],0])
				ct_std += 1
		#print(std)
		print(source)
		print(ope_list)
		print(len(ope_list))
		for i in range(len(ope_list)-1): #exclued the last term
			x = ope_list[i][0] * self.beat + self.zero_pos[0] 
			y = self.zero_pos[1]
			self.note_sep(x,y)
		return



#test case for func sep_operation()
if __name__ == '__main__':
	gui = autoGUI()
	gui.find_first_note()
	gui.note_count()
	#gui.zero_pos[0] = 111
	#gui.zero_pos[1] = 533
	#gui.sep_point = [[111, 177, 516, 548], [181, 237, 515, 549], [237, 279, 515, 547], [279, 366, 515, 545], [366, 416, 515, 544], [416, 465, 515, 546], [463, 486, 515, 545], [486, 562, 514, 550], [559, 589, 515, 546], [587, 723, 517, 547], [723, 748, 515, 541], [746, 824, 515, 547], [824, 899, 515, 548], [1280, 0, 800, 0]]
	gui.midi = "bad_guy.mid"
	gui.melody()
	gui.sep_operation()
	
	
	

	