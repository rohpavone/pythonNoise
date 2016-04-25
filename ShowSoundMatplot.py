import pyaudio
import matplotlib.pyplot as plt
import numpy as np

def multiply(sig1, sig2):
    if len(sig1) != len(sig2):
        return []

    for i in range(len(sig1)):
        sig1[i] = sig2[i] * sig1[i]

    return sig1 # worked, still needs to be digitized




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

''' pyaudio shit right here '''
CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 15

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,
                frames_per_buffer=CHUNK)

''' end of section '''




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

for i in range(int(RATE/CHUNK*RECORD_SECONDS)):
    fig.canvas.restore_region(backgrounds)
    line.set_ydata(printData())
    axes.draw_artist(line)
    fig.canvas.blit(axes.bbox)

print("DONE")

stream.stop_stream()
stream.close()

p.terminate()
