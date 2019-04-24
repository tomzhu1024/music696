import struct
import wave

from pylab import *

filename = r'original.wav'
wavefile = wave.open(filename, 'rb')  # open for writing

nchannels = wavefile.getnchannels()
sample_width = wavefile.getsampwidth()
framerate = wavefile.getframerate()
numframes = wavefile.getnframes()

print("channel", nchannels)
print("sample_width", sample_width)
print("framerate", framerate)
print("numframes", numframes)

y = zeros(numframes)

for i in range(numframes):
    val = wavefile.readframes(1)
    left = val[0:2]
    v = struct.unpack('h', left)[0]
    y[i] = v

Fs = framerate
specgram(y, NFFT=1024, Fs=Fs, noverlap=900)
show()
