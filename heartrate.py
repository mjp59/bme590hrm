import csv
import numpy as np
from scipy.signal import butter, lfilter, freqz


def read_my_file(filename):
    """

    :param filename:
    :return: two float arrays of equal length. Indexes correspond and one arrray is time and one is voltage
    """
    time = []
    voltage = []

    with open(filename, encoding='utf-8-sig') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            if row[0] != '' and float(row[0]) >= 0 and row[1] != '':
                time.append(float(row[0]))
                voltage.append(float(row[1]))

    print(time)
    print(voltage)
    return time, voltage


def butter_lowpass(cutoff, fs, order=5):
    """

    :param cutoff: float
    :param fs:
    :param order:
    :return:
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    """

    :param data:
    :param cutoff:
    :param fs:
    :param order:
    :return:
    """
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y
