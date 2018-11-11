import wave
import sys
import struct
import numpy


def open_file(file_name):
    return wave.open(file_name, 'rb')


def main():
    file = open_file(sys.argv[1])
    params = file.getparams()  # ([0]nchannels, [1]sampwidth, [2]framerate, [3]nframes, [4]comptype, [5]compname)
    minimum = float("inf")
    maximum = float("-inf")
    for i in range(params[3]//params[2]):  # choosing window size to 1 second, throwing away the "unfinished" part
        data = file.readframes(params[2])
        unpacked_data = struct.unpack('%ih' % (params[0]*params[2]), data)
        unpacked_data = numpy.array(unpacked_data)
        if params[0] == 2:  # 2 channels
            unpacked_data = unpacked_data.reshape(-1, 2)  # stuff found on stackoverflow
            unpacked_data = unpacked_data.sum(axis=1)/2  # stuff found on stackoverflow
        w = numpy.fft.rfft(unpacked_data)/params[2]
        w_absolutes = numpy.abs(w)
        avg_val = numpy.average(w_absolutes)
        for j, v in enumerate(w_absolutes):
            if v >= 20*avg_val:
                if minimum == float("inf") and maximum == float("-inf"):
                    minimum = j
                    maximum = j
                else:
                    if j < minimum:
                        minimum = j
                    if j > maximum:
                        maximum = j
    file.close()
    print_peaks(minimum, maximum)


def print_peaks(mi, ma):
    if mi != float("inf") and ma != float("-inf"):
        print("low = "+str(mi)+", high = "+str(ma))
    else:
        print("no peaks")

# haha


main()
