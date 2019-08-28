import pyautogui
import cv2
import numpy as np
import PIL
from PIL import Image, ImageChops, ImageDraw

#test case for pitch_reset
if __name__ == '__main__':
	gui = autoGUI()
	pyautogui.click()
	gui.find_select_area2()
	print(pyautogui.position())
	#gui.note_sep()
	moveToX = 275
	moveToY = 497
	secs_between_clicks = 0.2
	pyautogui.click(x=64,y=188)
	#pyautogui.click(x=moveToX,y=moveToY)
	pyautogui.doubleClick(x=moveToX,y=moveToY,interval=0.2)
	#pyautogui.click(x=218,y=282)
	#pyautogui.click(x=moveToX,y=moveToY,clicks=2,interval=0.1)
	#print(pyautogui.size())
	

if __name__ == '__main__':
	gui = autoGUI()
	#gui.find_select_area2()
	print(pyautogui.position())
	#gui.note_sep()
	#moveToX = 216
	moveToX = 200
	moveToY = 503
	secs_between_clicks = 0.2
	pyautogui.click(x=218,y=282)
	#pyautogui.click(x=moveToX,y=moveToY,clicks=2,interval=0.1)
	#pyautogui.click(x=moveToX,y=moveToY)
	pyautogui.doubleClick(x=moveToX,y=moveToY,interval=0.1)
	pyautogui.click(x=gui.edit[0],y=gui.edit[1])
	pyautogui.click(x=gui.undo[0],y=gui.undo[1])
	#pyautogui.click(x=moveToX,y=moveToY,clicks=2,interval=0.1)
	#print(pyautogui.size())
	#draw_rec("diff.jpg","output.jpg",375,425,1012,1044)
	# img = Image.open('green2.png').convert('RGB')
	# open_cv_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
	# for i in range(len(open_cv_image)):
	# 	print(open_cv_image[i])

#test case for find current position
if __name__ == '__main__':
	gui = autoGUI()
	#gui.find_select_area2()
	print(pyautogui.position())

#test case for func find_first_note()
if __name__ == '__main__':
	gui = autoGUI()
	gui.find_first_note()

#test case for pitch_reset
if __name__ == '__main__':
	gui = autoGUI()
	gui.find_first_note()
	gui.note_count()
	print(len(gui.sep_point))
	gui.pitch_reset()

#test case for note_count
if __name__ == '__main__':
	gui = autoGUI()
	gui.find_first_note()
	gui.note_count()

#test case for melody()
if __name__ == '__main__':
	gui = autoGUI()
	gui.midi = "bad_guy.mid"
	gui.melody()

#test case for func sep_operation()
if __name__ == '__main__':
	gui = autoGUI()
	gui.find_first_note()
	gui.note_count()
	#gui.zero_pos[0] = 113
	#gui.zero_pos[1] = 533
	#gui.sep_point = [[113, 179, 517, 549], [183, 237, 517, 550], [239, 271, 519, 547], [282, 368, 521, 546], [371, 416, 522, 545], [418, 467, 520, 546], [465, 484, 520, 546], [488, 559, 516, 551], [561, 589, 520, 546], [591, 725, 519, 548], [725, 748, 525, 542], [748, 821, 519, 548], [826, 901, 518, 549], [1280, 0, 800, 0]]
	#sep_list = [[1.0330578512396693, 1], [1.939387955729167, 0], [2.1198347107438016, 1], [2.9173553719008263, 1], [4.399644222005207, 0], [5.24793388429752, 1], [5.771696362304688, 0], [5.871900826446281, 1], [6.349838574218751, 0], [6.888357332356772, 0], [7.42687609049479, 0], [7.990969986979167, 0]]
	gui.midi = "bad_guy.mid"
	gui.melody()
	gui.sep_operation()
