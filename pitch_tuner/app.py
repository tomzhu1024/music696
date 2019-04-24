import librosa

y, sr = librosa.load('original.wav', sr=44100)  # y is a numpy array of the wav file, sr = sample rate
y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=0.5)  # shifted by 0.5 half steps
librosa.output.write_wav("processed.wav", y_shifted, 44100)
