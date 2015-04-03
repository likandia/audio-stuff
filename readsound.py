import pyaudio
import numpy
import matplotlib.pyplot as plt


if __name__ == "__main__":

    RATE = 48000
    CHANNELS = 1
    FRAMES = 3072
    FORMAT = pyaudio.paInt16

    recording_time = 10
    chunks = recording_time * RATE / FRAMES

    p = pyaudio.PyAudio();
    s = p.open(rate = RATE,
               channels = CHANNELS,
               format = FORMAT,
               frames_per_buffer = FRAMES,
               input = True)

    data = ''
    for i in range(0, chunks):
        data += s.read(FRAMES)

    data = numpy.fromstring(data,dtype=numpy.int16)
    plt.plot(data)
    plt.show()

    s.close()
