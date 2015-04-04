import pyaudio
import wave
import matplotlib
import matplotlib.pyplot as plt
import numpy
import threading
import time
import sys

CHUNK = 128 #1024
FORMAT = pyaudio.paInt16 # Try paFloat32 too
CHANNELS = 2
RATE = 48000
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"


frames = ''
final = numpy.fromstring(frames, dtype=numpy.int16)

plt.ion()
plt.plot([0, 1])


def getaudio():
    frames = ''
    for i in range(0, int(RATE / (CHUNK) * RECORD_SECONDS)):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

        data = stream.read(CHUNK)
        frames += data

        final = numpy.fromstring(frames, dtype=numpy.int16)
        final = abs(final)
        final = final - 500
        masked = numpy.ma.masked_where(final < 0, final)
        masked.fill_value = 0
        final = numpy.ma.filled(masked)
        plt.plot(final)
        stream.stop_stream()
        stream.close()
        time.sleep(0.0001)
        print final
        p.terminate()

t0 = threading.Thread(target=getaudio)
t0.start()

while True:
    print "drawing"
    plt.clf()
    #plt.draw()
    time.sleep(0.1)
    plt.pause(0.0001)


#wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#wf.setnchannels(CHANNELS)
#wf.setsampwidth(p.get_sample_size(FORMAT))
#wf.setframerate(RATE)
#wf.writeframes(b''.join(frames))
#wf.close()
