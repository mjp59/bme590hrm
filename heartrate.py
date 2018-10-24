import matplotlib
import csv
import numpy as np
import math
import scipy
from scipy.signal import butter, lfilter, freqz
from numpy import diff
import statistics
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import logging
import json
import sys



def main():
    x = sys.argv[-1]
    logging.basicConfig(filename='heartrate.log', level=logging.DEBUG)
    if x == 'heartrate.py':
        logging.warning('Taking user input high risk for invalid file')
        print('Enter the filename:')
        x = input()
    time_volt = read_my_file(x)
    time = time_volt[0]
    volt = time_volt[1]
    fs = 1 / (time[1] - time[0])
    filtered_volt = butter_lowpass_filter(volt, 20.0, fs, 6)
    ext_volt = (min_stupid_method(volt), max_stupid_method(volt))
    duration = subtract_stupid_method(min_stupid_method(time), max_stupid_method(time))
    slope = diff_signal(time, filtered_volt)
    avg_slope = take_avg(slope)
    std_slope = get_std(slope)
    if math.isnan(std_slope):
        threshold = max(slope) * .8

    elif max(slope) / std_slope > 8.5:
        threshold = std_slope * 2
    else:
        threshold = avg_slope + (4 * std_slope)

    try:
        print("Enter the start time for average heart rate calculation (must be 0 or greater and less than " + str(duration)
              , ":")
        y = input()
        print("Enter the end time for average heart rate calculation (must be 0 or greater and less than " + str(duration),
              ":")
        z = input()
        if float(y) > duration or float(y) < 0 or float(z) > duration or float(z) < 0:
            print("Error: Enter start and end values with the allowed range ")
            sys.exit()
        if float(z) < float(y) or float(y) > float(z):
            print("Error: Enter an start time that is smaller than the end time or an end time that "
                  "is greater than the start time")
        beat_time = check_for_peak(float(y), float(z), fs, threshold, time, slope)
    except ValueError:
        print("Error: Enter a Numeric Value")
        sys.exit()

    beat_count = length_stupid_method(beat_time)
    avg_bpm = calc_avg_heartrate(beat_time)
    dict = make_dict(avg_bpm, ext_volt, duration, beat_count, beat_time)
    write_json(dict)


def read_my_file(filename):
    """
              Reads values from first two columns in a csv file

    :param filename: string
                Must be the name of a csv file to read
    :return: float array
            two float arrays of equal length. Indexes correspond. The first array is time and second array is voltage
    """
    time = []
    voltage = []
    try:
        with open(filename, encoding='utf-8-sig') as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            for row in csvReader:
                if row[0] != '' and row[0] != 'bad data' and float(row[0]) >= 0 and row[1] != '' and \
                        row[1] != 'bad data':
                    time.append(float(row[0]))
                    voltage.append(float(row[1]))

        return time, voltage

    except FileNotFoundError:
        print("Err... File not found")



def butter_lowpass(cutoff, fs, order=5):
    """
            creates the correct coefficients to simulate a low pass filter

    :param cutoff: float
            Cutoff is the desired cutoff frequency of the low pass filter
    :param fs: float
            The sampling rate from the imported data, normalizes the cutoff based sampling rate.
    :param order: integer
           determines the number of coefficients for the filter
    :return: floats
           Returns the coefficients to be used in the low pass filter
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    """
        Filters out frequency information above the the cutoff in the selected data
    :param data: float array
             Data that will filtered by the low pass filter
    :param cutoff: float
             Cutoff is the desired cutoff frequency of the low pass filter
    :param fs: float
             The sampling rate of the data to be filtered
    :param order: integer
             determines the number of coefficients for the filter
    :return: float array
            Returns the filtered data in a float array.
    """
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def min_stupid_method(array):
    """
        Finds the min and max values in the input array
    :param : float array
            Array of multiple numeric values
    :return: tuple
            Returns a tuple containing min and max of the array. First element of the tuple is the min and the second
            element is the max.
    """
    extreme1 = (min(array))
    return extreme1


def max_stupid_method(array):
    extreme2 = (max(array))
    return extreme2


def subtract_stupid_method(min, max):
    duration = max - min
    return duration

def diff_signal(array1, array2):
    """
        Takes the derivative of signal y with respect to x.

    :param array1: float array
            Float array of independent var. , the derivative is taken with respect to this var.
    :param array2: float array
            Float array of the dependent var. , looking at the change of this var. with respect to x
    :return: Float Array
            Returns a Float Array that contains the derivative of the signal. The length of the return array will be
            N-1 (N = length of the input array).
    """
    dy = diff(array2)
    dx = diff(array1)
    slope = dy / dx
    return slope


def take_avg(array):
    """
        Takes the average of a numeric array
    :param array: float array
            Array of numeric values
    :return: float
            Returns a single float, that is the average of the input array
    """
    total = sum(array)
    avg = total / len(array)
    return avg


def get_std(array):
    """
        Returns the standard deviation of the array
    :param array: float array
        Array of numeric values
    :return: float
        Returns a single float, that is the standard deviation of the input array
    """
    std = statistics.stdev(array)
    return std


def check_for_peak(start, end, fs, threshold, array1, array2):
    """
        Determines the number of qs peaks within a given time frame
    :param start: Float
        User specfic time to start checking for peaks
    :param end: float
        User specfic time to stop checking for peaks
    :param fs: float
        Sampling rate of peak data so the time between samples can be calc.
    :param threshold: float
        Numeric value that the array2 value must be greater than to be considered a peak
    :param array1: float array
        Array of numeric values that are the times which the signal was sampled
    :param array2: float array
        Array of numeric values that are the value of the signal at that time
    :return: float array, integer
        Returns a array of the times that the peaks/ beats occur. Also returns an integer that represents the number of
        beats in the given time frame
    """
    beat_time = []
    current_time = 0
    start_index = 0
    end_index = 0
    for x in range(len(array1)):
        if (start - (1 / fs)) <= array1[x] <= (start + (1 / fs)):
            start_index = x
        if (end - (1 / fs)) <= array1[x] <= (end + (1 / fs)):
            end_index = x

    if max(array2) / get_std(array2) > 8.5:
        threshold = get_std(array2) * 2
        for x in range(start_index, end_index):
            if abs(array2[x]) >= threshold and (array1[x] >= (current_time + .5) or array1[x] == 0):
                current_time = array1[x]
                beat_time.append(array1[x])

    elif abs(min(array2)) > max(array2):
        for x in range(start_index, end_index):
            if abs(array2[x]) >= threshold and (array1[x] >= (current_time + .1) or array1[x] == 0):
                current_time = array1[x]
                beat_time.append(array1[x])
    else:
        for x in range(start_index, end_index):
            if array2[x] >= threshold and (array1[x] >= (current_time + .1) or array1[x] == 0):
                current_time = array1[x]
                beat_time.append(array1[x])
    return beat_time


def length_stupid_method(array):
    beat_count = len(array)
    return beat_count

def calc_avg_heartrate(array):
    """
        Calcs the average heart from the array of time values where beats occur
    :param array: float array
        array of the times where the beats/ qs peaks occur
    :return: float
        Returns the average bpm of the patient during the user specifc time range
    """
    summation = 0
    count = 0
    if len(array) == 0 or len(array) == 1:
        return "Not Enough QS Peaks in Time Range to Determine BPM"
    for x in range(len(array)):
        if x != (len(array) - 1):
            bpm = 60 / (array[x + 1] - array[x])
            summation = summation + bpm
            count = count + 1
    avg_bpm = summation / count
    return avg_bpm


def make_dict(mean_bpm, volt_ext, duration, num_beats, beats):
    """

    :param mean_bpm: float
        Average bpm of the signal over the specfic time range
    :param volt_ext: tuple
        Tuple of the min and max voltages in the signal
    :param duration: float
        Length of sample/ data strip
    :param num_beats: integer
        The number of beats that occur in the specfic time frame
    :param beats: float array
        Float array of the times that qs peaks occur
    :return: dictionary
        returns a dictionary of the important metrics from the signal data
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
    """
        Writes the input dictionary to a text file using json
    :param dict: dictionary
        Dictionary with all the important metrics for the data signal. Dict is writing a file named metrics.txt
    """
    with open('metrics.txt', 'w') as outfile:
        json.dump(dict, outfile, indent = 2)


if __name__ == "__main__":
    main()

