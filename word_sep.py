import os
import copy as cp
from pylab import *
import pretty_midi
import librosa             # The librosa library
import librosa.display     # librosa's display module (for plotting features)
import IPython.display     # IPython's display module (for in-line audio)
import matplotlib.pyplot as plt # matplotlib plotting functions
import matplotlib.style as ms   # plotting style
import numpy as np              # numpy numerical functions
import scipy
import math
import random
import csv
import copy

#coef < 1, wpm - word per minute (word length)
def word_sep(wav,rate,wpm,coef_valley=0.15,coef_top=0.3):
	y,sr = librosa.load(wav,sr=rate)
	y_energy = librosa.feature.rms(y=y)
	y_sample = []
	time = []
	y_y = []
	valley_ind = []
	valley = {} #valley store the time for each valley index
	stop_time = []
	int_val = [] #validate interval
	for i in range(len(y_energy[0])):
		y_sample.append([i,y_energy[0][i]])
		time.append(i*512/rate)
		y_y.append(y_energy[0][i])
	thred_valley = max(y_y)*coef_valley
	thred_top = max(y_y)*coef_top
	#print(y_y)
	
	#there might be some problem adding head if there is a long silence at the beginning
	valley_ind.append(0)
	valley[0] = time[0]
	
	# add the valley larger than thred_valley
	for i in range(len(y_y)-2):
		if ((y_y[i+2]-y_y[i+1]) > 0 and (y_y[i+1]-y_y[i]) <= 0) or ((y_y[i+2]-y_y[i+1]) >= 0 and (y_y[i+1]-y_y[i]) < 0):
			if y_y[i+1] < thred_valley:
				valley_ind.append(i+1)
				valley[i+1] = time[i+1]
	stop_time.append(valley[valley_ind[0]])
	
	#remove short/invalid interval
	i = 0
	while i < (len(valley_ind)-1):
		while i < (len(valley_ind)-1) and (valley[valley_ind[i+1]] - valley[valley_ind[i]]) < wpm*0.4:
			if max(y_y[valley_ind[i]:valley_ind[i+1]]) < thred_top:
				stop_time.append(valley[valley_ind[i+1]])
				int_val.append(0)
				i += 1
			else:
				valley_ind.remove(valley_ind[i+1])
		if i+1 < len(valley_ind):
			stop_time.append(valley[valley_ind[i+1]])
			if max(y_y[valley_ind[i]:valley_ind[i+1]]) < thred_top:
				int_val.append(0)
			else:
				int_val.append(1)
		i += 1
	
	#there might be problem add the tail 
	stop_time.append(time[-1])
	int_val.append(1)
	
	valid_word = []
	for i in range(len(stop_time)-1):
		if int_val[i] == 1:
			valid_word.append([stop_time[i],stop_time[i+1]])
	print(stop_time)
	print(int_val)
	return valid_word

def energy_graph(wav,rate):
	y,sr = librosa.load(wav,sr=rate)
	print(len(y))
	y_energy = librosa.feature.rms(y=y)
	y_sample = []
	time = []
	y_y = []
	for i in range(len(y_energy[0])):
		y_sample.append([i,y_energy[0][i]])
		time.append(i*512/rate)
		y_y.append(y_energy[0][i])
	plt.plot(time,y_y)
	plt.savefig("zbs_second_energy_fig.png")
	return y,sr

#term in time_list - [whether_silence,start,end]
def t_stretch(valid_word,time_list,wav,rate,out_name):
	blen = 0.02
	y,sr = librosa.load(wav,sr=rate)
	new_y = np.array([])
	words = []
	for i in range(len(valid_word)):
		start = int(valid_word[i][0]*sr)
		end = int(valid_word[i][1]*sr)
		word = y[start:end]
		words.append([word,(end-start)/sr])
	#print(words)
	ct = 0
	#either melody or words_list is longer, choose the shorter one
	for i in range(min([len(time_list),len(words)])):
		rlen = time_list[i][2]-time_list[i][1]
		if time_list[i][0] == 0:
			ratio = words[ct][1]/(rlen-blen)
			new_word = librosa.effects.time_stretch(words[ct][0],ratio)
			new_y = np.concatenate((new_y,new_word))
			#add 0.1s silence to seperate each word for easy pitch shifting
			blank = [0]*int(rate*blen)
			blank = np.array(blank)
			new_y = np.concatenate((new_y,blank))
			#print(new_y)
			ct += 1
		else:
			blank = [0]*int(rate*rlen)
			blank = np.array(blank)
			new_y = np.concatenate((new_y,blank))
	print(len(new_y))
	librosa.output.write_wav(out_name,new_y,44100)
	return

def melody(midi_file):
	speed = 1.25 #adjust the speed of music, slow when speed>1
	# Load MIDI file into PrettyMIDI object
	midi_data = pretty_midi.PrettyMIDI(midi_file)
	instrument = midi_data.instruments[0]
	print(instrument.name)
	time_list = []
	start = []
	end = []
	for note in instrument.notes:
		start.append(note.start*speed)
		end.append(note.end*speed)
	start.sort()
	end.sort()
	# for i in range(len(start)-1):
	# 	time_list.append([0,start[i],end[i]])
	# 	if end[i] < start[i+1]:
	# 		time_list.append([1,end[i],start[i+1]])
	for i in range(len(start)-19):
		time_list.append([0,start[i+18],end[i+18]])
		if end[i] < start[i+1]:
			time_list.append([1,end[i+18],start[i+19]])
	return time_list

# y,sr = energy_graph("zbs_second.wav",44100)
#valid_word = word_sep("zbs_ori_highpass.wav",44100,0.4,coef_valley=0.15,coef_top=0.3)
#valid_word = word_sep("zbs_second.wav",44100,0.3,coef_valley=0.3,coef_top=0.3)
#valid_word = word_sep("sanguo_cut.wav",44100,0.35,coef_valley=0.15,coef_top=0.3)
valid_word = word_sep("mianjing_cut.wav",44100,0.4,coef_valley=0.15,coef_top=0.3)
print(valid_word)
#time_list = [[0,0,0.4],[0,0.4,0.8],[0,0.8,1.2],[0,1.2,1.6],[0,1.6,2.4],[0,2.4,3.2],[0,3.2,4.0],[1,4.0,6.4]] #for zbs sentence1
#time_list = [[0,0,0.4],[0,0.4,0.8],[0,0.8,1.2],[0,1.2,1.6],[0,1.6,2.8],[0,2.8,3.0],[0,3.0,4.0],[1,4.0,5.6]] #for zbs sentence2
time_list = melody("bad_guy.mid")
#time_list = melody("jasmine_flower.mid")
#t_stretch(valid_word,time_list,"zbs_ori_highpass.wav",44100)
#t_stretch(valid_word,time_list,"sanguo_cut.wav",44100,"sanguo+bad.wav")
#t_stretch(valid_word,time_list,"sanguo_cut.wav",44100,"sanguo+jas.wav")
#t_stretch(valid_word,time_list,"mianjing_cut.wav",44100,"mianjing+jas.wav")
t_stretch(valid_word,time_list,"mianjing_cut.wav",44100,"mianjing+bad.wav")
#t_stretch(valid_word,time_list,"zbs_second.wav",44100)

# y1,sr1 = librosa.load("zbs_sample_44100.wav",sr=44100)
# y2,sr2 = librosa.load("zbs_ori.wav",sr=44100)
# print(len(y1),len(y2))
# print(y1.shape,y2.shape)
# print(y2[1])
# y1_energy = librosa.feature.rms(y=y1)
# y2_energy = librosa.feature.rms(y=y2)
# print(len(y1_energy[0]))
# print(len(y2_energy[0]))
# y1_sample = []
# y2_sample = []
# time1 = []
# time2 = []
# y1_y = []
# y2_y = []
# for i in range(len(y1_energy[0])):
# 	y1_sample.append([i,y1_energy[0][i]])
# 	time1.append(i*512/44100)
# 	y1_y.append(y1_energy[0][i])
# for j in range(len(y2_energy[0])):
# 	y2_sample.append([j,y2_energy[0][j]])
# 	time2.append(j*512/44100)
# 	y2_y.append(y2_energy[0][j])
# plt.plot(time1,y1_y)
# plt.plot(time2,y2_y)
# plt.savefig("result_fig.png")
#a = Guichu_Generator(None,None,time_coef=1*512*512/44100/44100,beat_coef=10)
#result, q = a.local_DTW_2d(y1_sample,y2_sample)
#print(result[0][3])
#print(result[0][3])
#temp = result[0][3]
# for in range(len(result[0][3]-1)):
# 	temp_dif.append([])
# mix_y = np.array([])
# fast = 1
# slow = 1
# i = len(temp)-1
# while i > 0:
# 	if fast == 1 and slow == 1:
# 		if (temp[i-1][0] - temp[i][0]) == (temp[i-1][1] - temp[i][1]):
# 			mix_y = np.concatenate((mix_y,y2[temp[i][1]*512:temp[i][1]*512+512]))
# 		elif (temp[i-1][0] - temp[i][0]) < (temp[i-1][1] - temp[i][1]):
# 			fast += 1
# 			ori_temp = temp[i][1] #time stamp
# 			temp_y = y2[ori_temp*512:ori_temp*512+512]
# 		else:
# 			slow += 1
# 			ori_temp = temp[i][1]
# 			temp_y = y2[ori_temp*512:ori_temp*512+512]
# 	elif slow > 1:
# 		if (temp[i-1][0] - temp[i][0]) <= (temp[i-1][1] - temp[i][1]):
# 			mix_temp = librosa.effects.time_stretch(temp_y,1.0/slow)
# 			mix_y = np.concatenate((mix_y,mix_temp)) 
# 			slow = 1
# 		else:
# 			slow += 1
# 	else:
# 		if (temp[i-1][0] - temp[i][0]) >= (temp[i-1][1] - temp[i][1]):
# 			mix_temp = librosa.effects.time_stretch(temp_y,fast)
# 			mix_y = np.concatenate((mix_y,mix_temp)) 
# 			fast = 1
# 		else:
# 			fast += 1
# 			ori_temp = np.concatenate((temp_y,y2[temp[i][1]*512:temp[i][1]*512+512]))
# 	print(i,mix_y.shape,slow,fast)
# 	i -= 1
# print(mix_y.shape,slow,fast)
# librosa.output.write_wav("final.wav",mix_y,44100)


