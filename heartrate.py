import csv


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
            if row[0] != '' and float(row[0]) >= 0 and row[1] != '' :
                time.append(float(row[0]))
                voltage.append(float(row[1]))

    print(time)
    print(voltage)
    return time, voltage