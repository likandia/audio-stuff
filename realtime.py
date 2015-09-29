import pyaudio
import matplotlib.pyplot as plt
import numpy
import threading
import time

CHUNK = 8 #1024
FORMAT = pyaudio.paInt16 # Try paFloat32 too
CHANNELS = 2
RATE = 48000
RECORD_SECONDS = 20

frames = ''
final = numpy.fromstring(frames, dtype=numpy.int16)

def callback(in_data, frame_count, time_info, status):
    global frames
    frames += in_data
    final = numpy.fromstring(frames, dtype=numpy.int16)
    final = abs(final)
    final = final
    masked = numpy.ma.masked_where(final < 0, final)
    masked.fill_value = 0
    final = numpy.ma.filled(masked)

    plt.plot(final[-3000:], 'b')
    plt.ylim(0.0, 50000.0)
    #plt.pause(0.0001)
    print final
    return (in_data, pyaudio.paContinue)

def getaudio():
    frames = ''
    p = pyaudio.PyAudio()
    #for i in range(0, int(RATE / (CHUNK) * RECORD_SECONDS)):
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE, #sampling rate
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)
    stream.start_stream()
    time.sleep(RECORD_SECONDS)

    #data = stream.read(CHUNK)
    #frames += data
    #final = numpy.fromstring(frames, dtype=numpy.int16)
    #final = abs(final)
    #final = final - 500
    #masked = numpy.ma.masked_where(final < 0, final)
    #masked.fill_value = 0
    #final = numpy.ma.filled(masked)

    #plt.plot(final[-3000:], 'b')

    #stream.stop_stream()
    #stream.close()
    #time.sleep(0.0001)
    #print final
    stream.stop_stream()
    stream.close()
    p.terminate()


def main():
    frames = ''
    final = numpy.fromstring(frames, dtype=numpy.int16)

    plt.ion()
    plt.plot([0, 1])

    t0 = threading.Thread(target=getaudio)
    t0.start()

    while True:
        print "drawing"
        plt.clf()
        #plt.draw()
        time.sleep(0.1)
        plt.pause(0.0001)

if __name__ == "__main__":
    main()
