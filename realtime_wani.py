import pyaudio
#import matplotlib.pyplot as plt
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy
import threading
import time
import wave
import sys

CHUNK = 128 #1024
FORMAT = pyaudio.paInt16 # Try paFloat32 too
CHANNELS = 2
RATE = 48000
RECORD_SECONDS = 20

frames = ''
final = numpy.fromstring(frames, dtype=numpy.int16)

wf = wave.open(sys.argv[1], 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(2)
wf.setframerate(RATE/4)

app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.resize(800, 800)
view = pg.GraphicsLayoutWidget()
mw.setCentralWidget(view)
mw.show()


w1 = view.addPlot(title = "Amplitude vs Time")
w1.setRange(xRange=[0.0, 20000.0], yRange=[0.0, 50000.0])
curve = w1.plot(pen='g')

def callback(in_data, frame_count, time_info, status):
    global frames, final, curve
    frames += in_data
    final = numpy.fromstring(frames, dtype=numpy.int16)
    final = abs(final)
    final = final
    masked = numpy.ma.masked_where(final < 0, final)
    masked.fill_value = 0
    final = numpy.ma.filled(masked)
    wf.writeframes(in_data)

    curve.setData(final[-20000:])
    print final
    return (frames, pyaudio.paContinue)

def getaudio():
    global final
    frames = ''
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE, #sampling rate
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)
    stream.start_stream()
    stream.stop_stream()
    stream.close()
    p.terminate()


def main():
    frames = ''
    final = numpy.fromstring(frames, dtype=numpy.int16)

if __name__ == "__main__":
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            timer = QtCore.QTimer()
            timer.timeout.connect(getaudio)
            timer.start(1)

            pg.QtGui.QApplication.instance().exec_()
