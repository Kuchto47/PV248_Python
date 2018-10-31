import wave
import sys
import struct
import numpy


def open_file(file_name):
    return wave.open(file_name, 'rb')


def main():
    file = open_file(sys.argv[1])
    params = file.getparams()  # ([0]nchannels, [1]sampwidth, [2]framerate, [3]nframes, [4]comptype, [5]compname)
    frames = file.readframes(params[3])
    file.close()
    total_samples = params[0] * params[3]
    fmt = "%ih" % total_samples
    unpacked_frames = struct.unpack(fmt, frames)
    audio_duration = params[3]/params[2]
    window_number = 1
    window_size = params[2]
    windows = []
    while window_number < audio_duration:
        window = []
        for i in range(window_size):
            window.append(unpacked_frames[((window_number - 1) * window_size)+i])
        windows.append(window)
        window_number += 1
    for win in windows:
        print(numpy.fft.rfft(win))


main()
