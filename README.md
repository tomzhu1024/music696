# music696

Research repository

# word_sep.py

## 用途

该方案用于对中文音频逐字切分

## 原理

计算音频的能量图谱。由于中文每个字间有明显的能量衰减，降噪后每一个波峰可看作单独的字。

## 函数解释

### word_sep(wav,rate,wpm,coef_valley,coef_top)

返回每个字的开始时间与结束时间

- wav

音频源

- rate

采样率

- wpm

word-per-min. 描述音频中的语速

- coef_valley

该数值以上的波谷不会被作为分断点

- coef_top

该数值以下的波峰视作噪音

### energy_graph(wav,rate)

绘制音频的能量图谱

- wav

音频源

- rate

采样率

### t_stretch(valid_word,time_list,wav,rate,out_name)

输出根据midi文件进行时间拉伸后的音频文件

- valid_word

音频文件每个字的开始时间和结束时间

- time_list

midi文件中旋律每个音的开始时间和结束时间

- wav

音频文件

- rate

采样率

- out_name

输出文件名

### melody(midi_file)

返回midi文件中旋律每个音的开始时间和结束时间

- midi_file

midi文件路径

# autogui.py

## 用途

使用pyautogui操作melodyne完成调音工作

## 方法解释

- note_count()

count the total number of note in the source audio and store the position of each note.

- note_duration(pic)

get the length of one block. Used for auto pitch shift

- single_pitch_reset(note_index)

move a single note to the pitch of the first note

- pitch_reset()

move all note to the pitch of the first note

- find_select_area2()

use diff to find the select area

- find_first_note()

use diff to find the first note

- note_sep(x1,y1)

remove a separation if it supposed not be a sep

- melody()

get the pitch list from the midi file, store in self.pitch_list and self.time_list

- sep_operation()

execute seperation operation to make seperation correct

# webVAD.py

voice activate detect




