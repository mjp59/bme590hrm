import csv
import numpy as np
import scipy
from scipy.signal import butter, lfilter, freqz
from numpy import diff
import statistics
import json


def main():
    print('Enter the filename:')
    x = input()
    time_volt = read_my_file(x)
    time = time_volt[0]
    volt = time_volt[1]
    fs = 1 / (time[1] - time[0])
    filtered_volt = butter_lowpass_filter(volt, 20.0, fs, 6)
    ext_volt = min_max(volt)
    ext_time = min_max(time)
    duration = ext_time[1] - ext_time[0]
    slope = diff_signal(time, filtered_volt)
    avg_slope = take_avg(slope)
    std_slope = get_std(slope)
    threshold = avg_slope + (2 * std_slope)
    print("Enter the start time for average heart rate calculation (must be 0 or greater and less than " + str(duration)
          , ":")
    y = input()
    print("Enter the end time for average heart rate calculation (must be 0 or greater and less than " + str(duration),
          ":")
    z = input()
    beat_info = check_for_peak(float(y), float(z), fs, threshold, time, slope)
    beat_time = beat_info[0]
    beat_count = beat_info[1]
    avg_bpm = calc_avg_heartrate(beat_time)
    dict = make_dict(avg_bpm, ext_volt, duration, beat_count, beat_time)
    write_json(dict)


def read_my_file(filename):
    """

    :param filename:
    :return: two float arrays of equal length. Indexes correspond and one array is time and one is voltage
    """
    time = []
    voltage = []

    with open(filename, encoding='utf-8-sig') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            if row[0] != '' and float(row[0]) >= 0 and row[1] != '':
                time.append(float(row[0]))
                voltage.append(float(row[1]))


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


def min_max(array):
    """

    :param array:
    :return: tuple containing min and max of the array
    """
    extreme1 = (min(array))
    extreme2 = (max(array))
    extremes = (extreme1, extreme2)
    return extremes


def diff_signal(array1, array2):
    """


    :param array1:
    :param array2:
    :return:
    """
    dy = diff(array2)
    dx = diff(array1)
    slope = dy / dx
    return slope


def take_avg(array):
    """

    :param array:
    :return:
    """
    total = sum(array)
    avg = total / len(array)
    return avg


def get_std(array):
    """

    :param array:
    :return:
    """
    std = statistics.stdev(array)
    return std


def check_for_peak(start, end, fs, threshold, array1, array2):
    """

    :param threshold:
    :param array1:
    :param array2:
    :return:
    """
    beat_time = []
    beat_count = 0
    current_time = 0
    start_index = 0
    end_index = 0
    for x in range(len(array1)):
        if (start - (1 / fs)) <= array1[x] <= (start + (1 / fs)):
            start_index = x
        if (end - (1 / fs)) <= array1[x] <= (end + (1 / fs)):
            end_index = x
    for x in range(start_index, end_index):
        if array2[x] >= threshold and array1[x] >= (current_time + .08):
            current_time = array1[x]
            beat_time.append(array1[x])
            beat_count = beat_count + 1
    return beat_time, beat_count


def calc_avg_heartrate(array):
    """

    :param start:
    :param end:
    :param array:
    :return:
    """
    summation = 0
    count = 0
    for x in range(len(array)):
        if x != (len(array) - 1):
            bpm = 60 / (array[x + 1] - array[x])
            summation = summation + bpm
            count = count + 1
    avg_bpm = summation / count
    return avg_bpm


def make_dict(mean_bpm, volt_ext, duration, num_beats, beats):
    """

    :param mean_bpm:
    :param volt_ext:
    :param duration:
    :param num_beats:
    :param beats:
    :return:
    """
    dict = {
        "Mean_hr_bpm": mean_bpm,
        "voltage_extremes": volt_ext,
        "duration": duration,
        "num_beats": num_beats,
        "beats": beats
    }
    return dict


def write_json(dict):
    with open('data.txt', 'w') as outfile:
        json.dump(dict, outfile, indent = 2)


if __name__ == "__main__":
    main()

