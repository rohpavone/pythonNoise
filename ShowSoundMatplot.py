import pyaudio
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter, freqz

''' pyaudio shit right here '''
CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 15

def butter_lowpass(cutoff, fs, order=5):
	nyq = 0.5 * fs
	normal_cutoff = cutoff / nyq
	b, a = butter(order, normal_cutoff, btype='low', analog=False)
	return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
	b, a = butter_lowpass(cutoff, fs, order=order)
	y = lfilter(b, a, data)
	return y


def printData():
    global y
    data = stream.read(CHUNK)
    for i in range(CHUNK):
        y[i] = (int.from_bytes(data[4*i:4*i+2], byteorder='little', signed=True))
        #right_channel.append(int.from_bytes(data[4*i+2:4*i+3], byteorder='big', signed=True))
    
    #left_channel = np.fft.fft(left_channel)
    #temp = copy.deepcopy(left_channel[:CHUNK/2])
    #left_channel[:CHUNK/2] = copy.deepcopy(left_channel[CHUNK/2:])
    #left_channel[CHUNK/2:] = temp'''
    return left_channel



p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,
                frames_per_buffer=CHUNK)

''' end of section '''
order = 6
cutoff = 1000
b, a  = butter_lowpass(cutoff, RATE, order)

''' pylab shit goes here '''
fig, axes = plt.subplots(nrows=1)
fig.show()
x = np.arange(0, CHUNK, 1)
y = [0]*CHUNK
axes.set_xlim([0, 1024])
axes.set_ylim([-17000, 17000])

fig.canvas.draw()
styles = ['r-']

def plot(ax, style):
    return ax.plot(x, y, style, animated=True)[0]

line = plot(axes, styles[0])
backgrounds = fig.canvas.copy_from_bbox(axes.bbox)


''' the shit that's going down '''

print("recording commencing")
l = []
for i in range(int(RATE/CHUNK*RECORD_SECONDS)):
    fig.canvas.restore_region(backgrounds)
    l = printData()
    y = butter_lowpass_filter(data, cutoff, fs, order)
    line.set_ydata(y)
    axes.draw_artist(line)
    fig.canvas.blit(axes.bbox)

print("DONE")

stream.stop_stream()
stream.close()

p.terminate()
