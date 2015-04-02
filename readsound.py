import pyaudio
import numpy
import matplotlib.pyplot as plt


RATE = 48000
CHANNELS = 1
FRAMES = 3072
FORMAT = pyaudio.paInt16

recording_time = 10


p = pyaudio.PyAudio();
s = p.open(rate = RATE,
           channels = CHANNELS,
           format = FORMAT,
           frames_per_buffer = FRAMES,
           input = True)

data = s.read(FRAMES)
data = numpy.fromstring(data,dtype=numpy.int16)
plt.plot(data)
plt.show()

s.close()
