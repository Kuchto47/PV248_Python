import wave
import sys
import struct
import numpy


def open_file(file_name):
    return wave.open(file_name, 'rb')


def main():
    # file opening
    file = open_file(sys.argv[1])
    params = file.getparams()  # ([0]nchannels, [1]sampwidth, [2]framerate, [3]nframes, [4]comptype, [5]compname)
    data = file.readframes(params[3])
    file.close()
    # file closing
    # getting data
    data_size = params[0] * params[3]
    # fmt = "%ih" % data_size
    unpacked_data = struct.unpack('{n}h'.format(n=data_size), data)
    unpacked_data = numpy.array(unpacked_data)
    #getting data done
    w = numpy.fft.fft(unpacked_data)
    freqs = numpy.fft.fftfreq(len(w))
    print(freqs.min(), freqs.max())
    # find peak
    idx = numpy.argmax(numpy.abs(w))
    freq = freqs[idx]
    freq_in_hertz = abs(freq * params[2])
    print(freq_in_hertz)


main()
