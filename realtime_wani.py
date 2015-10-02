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

class Recorder(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(Recorder, self).__init__(parent)
        view = pg.GraphicsLayoutWidget()
        w1 = view.addPlot(title = "Amplitude vs Time")
        w1.setRange(xRange = [0.0, 20000.0], yRange = [0.0, 50000.0])
        self.curve = w1.plot(pen = 'g')

        self.resize(800, 800)
        self.setCentralWidget(view)

        self.frames = ''
        self.final = numpy.fromstring(self.frames, dtype=numpy.int16)

        self.wf = wave.open(sys.argv[1], 'wb')
        self.wf.setnchannels(CHANNELS)
        self.wf.setsampwidth(2)
        self.wf.setframerate(RATE/4)
        self.show()

        self.getaudio()
        #timer = QtCore.QTimer()
        #timer.timeout.connect(self.getaudio)
        #timer.start(1)

    def callback(self, in_data, frame_count, time_info, status):
        self.frames += in_data
        self.final = numpy.fromstring(self.frames, dtype=numpy.int16)
        self.final = abs(self.final)
        self.final = self.final
        masked = numpy.ma.masked_where(self.final < 0, self.final)
        masked.fill_value = 0
        self.final = numpy.ma.filled(masked)
        self.wf.writeframes(in_data)

        self.curve.setData(self.final[-20000:])
        print self.final
        return (self.frames, pyaudio.paContinue)

    def getaudio(self):
        self.frames = ''
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE, #sampling rate
                        input=True,
                        frames_per_buffer=CHUNK,
                        stream_callback=self.callback)
        stream.start_stream()
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            app = pg.QtGui.QApplication(sys.argv)
            r = Recorder()
            app.exec_()
