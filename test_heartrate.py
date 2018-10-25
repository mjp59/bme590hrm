from heartrate import read_my_file
from heartrate import butter_lowpass
from heartrate import butter_lowpass_filter
from heartrate import diff_signal
from heartrate import take_avg
from heartrate import check_for_peak
from heartrate import min_stupid_method
from heartrate import max_stupid_method
from heartrate import subtract_stupid_method
from heartrate import length_stupid_method
from heartrate import get_std
from heartrate import calc_avg_heartrate
from heartrate import make_dict
import pytest
import numpy as np
import json
import math


@pytest.mark.parametrize("candidate,expected", [
    ('Test.csv', ([0, 1.2, 2.4], [-.375, -.475, 4])),



])
def test_read_my_file(candidate, expected):
    response = read_my_file(candidate)
    assert response[0] == expected[0]
    assert response[1] == expected[1]


@pytest.mark.parametrize("candidate", [
    'what',


])
def test_read_my_file(candidate):
    with pytest.raises(FileNotFoundError) as excinfo:
        read_my_file(candidate)
        print(str(excinfo.value))
    assert str(excinfo.value) == "[Errno 2] No such file or directory: 'what'"


@pytest.mark.parametrize("cutoff, fs, order,expected", [
    (3.667, 30, 6, ([0.00094045, 0.00564271, 0.01410677, 0.01880902,
                     0.01410677, 0.00564271, 0.00094045],
                    [1., -3.04492596, 4.28973778, -3.42146954,
                     1.60826347, -0.41810886, 0.04669197])),

])
def test_butter_lowpass(cutoff, fs, order, expected):
    response = butter_lowpass(cutoff, fs, order)
    assert np.allclose(response[0], expected[0])
    assert np.allclose(response[1], expected[1])


T = 5.0
n = int(T * 30)
t = np.linspace(0, T, n, endpoint=False)
data = np.sin(1.2*2*np.pi*t) + 1.5*np.cos(9*2*np.pi*t) + \
       0.5*np.sin(12.0*2*np.pi*t)


@pytest.mark.parametrize("data, cutoff, fs, order,expected", [
    (data, 3.667, 30, 6, [0.00141068,  0.01283382,  0.05349742,
                          0.13741716,  0.25054009,  0.36194211,
     0.45909427,  0.55284894,  0.65525127,
                          0.7690796,   0.88314594,  0.96675818,
     0.98558238,  0.92427353,  0.78481487,
                          0.57964823,  0.33445123,  0.077532,
     -0.17460127, -0.41022938, -0.61597217,
                          -0.78449324, -0.91079605, -0.98329614,
     -0.99342681, -0.94213446, -0.83056357,
                          -0.66239634, -0.45216134, -0.21584732,
     0.03491927,  0.28353429,  0.51134855,
                          0.70753204,  0.86178905,  0.96054398,
     0.99824139,  0.97569704,  0.89118286,
                          0.74832676,  0.56009559,  0.33764406,
     0.09160092, -0.15960256, -0.39855348,
                          -0.61425471, -0.79238693, -0.91833802,
     -0.98713297, -0.99604418, -0.94055743,
                          -0.82493686, -0.65989893, -0.45289449,
     -0.21529384,  0.03400242,  0.28014658,
                          0.51112163,  0.70947678,  0.86113433,
     0.9604951,   1.00052196,  0.97524539,
                          0.88918044,  0.74938287,  0.56067402,
     0.33573013,  0.09213149, -0.1577588,
                          -0.39985792, -0.61502563, -0.79053508,
     -0.91881047, -0.98886271, -0.9946411,
                          -0.93974551, -0.82680729, -0.65947764,
     -0.45121421, -0.21672166,  0.03319471,
                          0.28203935,  0.51072466,  0.70781062,
     0.86256246,  0.96129337,  0.99861747,
                          0.97563464,  0.89084532, 0.74795856,
     0.55988129,  0.33763872,  0.0917434,
                          -0.15942512, -0.39843618, -0.61423502,
     -0.79244448, -0.91842188, -0.98719521,
                          -0.99606177, -0.94053561, -0.82489803,
     -0.65986675, -0.45288224, -0.21530128,
                          0.03398483,  0.2801303,   0.51111402,
     0.7094788,   0.8611421,   0.96050316,
                          1.00052639,  0.97524519,  0.88917711,
     0.74937896,  0.56067156,  0.33572985,
                          0.09213286, -0.15775693, -0.3998566,
     -0.61502532, -0.79053562, -0.91881134,
                          -0.9888634,  -0.99464134, -0.93974532,
     -0.82680689, -0.65947729, -0.45121406,
                          -0.21672172,  0.03319454,  0.28203917,
     0.51072457,  0.70781063,  0.86256254,
                          0.96129346,  0.99861752,  0.97563464,
     0.89084529,  0.74795852,  0.55988126,
                          0.33763872,  0.09174341, -0.1594251,
     -0.39843616, -0.61423502, -0.79244449,
                          -0.91842189, -0.98719522, -0.99606178]),

])
def test_butter_lowpass_filter(data, cutoff, fs, order, expected):
    response = butter_lowpass_filter(data, cutoff, fs, order)
    assert np.allclose(response, expected)


@pytest.mark.parametrize("array1, array2, expected", [
    ([0, 1, 3], [0, 1, 3], (1, 1)),
    ([0, 2, 4], [0, 4, 8], (2, 2))



])
def test_diff_signal(array1, array2, expected):
    response = diff_signal(array1, array2)
    assert response[0] == expected[0]
    assert response[1] == expected[1]


@pytest.mark.parametrize("array, expected", [
    ([0, 1, 5], 2),
    ([0, 2, 4], 2)



])
def test_take_avg(array, expected):
    response = take_avg(array)
    assert response == expected


@pytest.mark.parametrize("start, end, fs, thres, array1, array2, expected", [
    (0, 10, 7/12, 5, [0, 2, 4, 6, 8, 9, 12], [0, 4, 4.9, 5, 5.1, 8, 12],
     [6, 8]),
    (0, 10, 7/12, 5, [0, 2, 4, 6, 8, 9, 12], [0, 4, 4.9, 4.9999, 0, 0, 0],
     []),
    (0, 10, 2/3, 5, [0, 2, 4, 6, 8, 9], [7, 5, 7, 8, 3, 2], [0, 2, 4, 6]),




])
def test_check_for_peak(start, end, fs, thres, array1, array2, expected):
    response = check_for_peak(start, end, fs, thres, array1, array2)
    assert response == expected


for x in range(1, 33):
    c = "test_data"
    d = str(x) + '.csv'
    e = c + d
    time_volt = read_my_file(e)
    time = time_volt[0]
    volt = time_volt[1]
    fs = 1 / (time[1] - time[0])
    filtered_volt = butter_lowpass_filter(volt, 20.0, fs, 6)
    ext_volt = (min_stupid_method(volt), max_stupid_method(volt))
    duration = subtract_stupid_method(min_stupid_method(time),
                                      max_stupid_method(time))
    slope = diff_signal(time, filtered_volt)
    avg_slope = take_avg(slope)
    std_slope = get_std(slope)
    if math.isnan(std_slope):
        threshold = max(slope) * .8

    elif max(slope) / std_slope > 8.5:
        threshold = std_slope * 2

    else:
        threshold = avg_slope + (4 * std_slope)
    a = 'beat_time'
    b = str(x)
    globals()[a + b] = check_for_peak(0, duration, fs, threshold, time, slope)


@pytest.mark.parametrize("array, expected", [
    ([0, 0, 0, 0], 4),
    (beat_time1, 34),
    (beat_time2, 32),
    (beat_time3, 34),
    (beat_time4, 32),
    (beat_time5, 34),
    (beat_time7, 31),
    (beat_time8, 32),
    (beat_time9, 28),
    (beat_time10, 44),
    (beat_time12, 9),
    (beat_time13, 3),
    (beat_time15, 7),
    (beat_time16, 19),
    (beat_time17, 19),
    (beat_time18, 19),
    (beat_time19, 19),
    (beat_time20, 19),
    (beat_time21, 19),
    (beat_time22, 37),
    (beat_time23, 75),
    (beat_time25, 30),
    (beat_time27, 62),
    (beat_time28, 1),
    (beat_time29, 9),
    (beat_time30, 77),
    (beat_time31, 19),
    (beat_time32, 19),
])
def test_length_stupid_method(array, expected):
    response = length_stupid_method(array)
    assert response == expected


@pytest.mark.parametrize("array, expected", [
    ([0, 1, 2, 3], 0),
    ([1, 2, 3, 4], 1),
])
def test_min_stupid_method(array, expected):
    response = min_stupid_method(array)
    assert response == expected


@pytest.mark.parametrize("array, expected", [
    ([0, 1, 2, 3], 3),
    ([1, 2, 3, 4], 4),
])
def test_max_stupid_method(array, expected):
    response = max_stupid_method(array)
    assert response == expected


@pytest.mark.parametrize("min1, max1, expected", [
    (3, 6, 3),
    (3, 7, 4),
])
def test_subtract_stupid_method(min1, max1, expected):
    response = subtract_stupid_method(min1, max1)
    assert response == expected


@pytest.mark.parametrize("array, expected", [
    ([0, 1, 2], 1),
])
def test_get_std(array, expected):
    response = get_std(array)
    assert response == expected


@pytest.mark.parametrize("array, expected", [
    ([0, 1, 2], 60),
])
def test_calc_avg_heartrate(array, expected):
    response = calc_avg_heartrate(array)
    assert response == expected


@pytest.mark.parametrize("mean_bpm, volt_ext, duration, num_beats, beats, r", [
    (60, (0, 60), 10, 5, [0, 1, 2, 3, 4], 60),
])
def test_make_dict(mean_bpm, volt_ext, duration, num_beats, beats, r):
    response = make_dict(mean_bpm, volt_ext, duration, num_beats, beats)
    bpm = response.get('Mean_hr_bpm')
    assert bpm == r


@pytest.mark.parametrize("file", [
    "metrics.txt",
])
def test_write_json(file):
    with open(file) as f:
        data = json.load(f)
        x = "Mean_hr_bpm" in data
        assert x
