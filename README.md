# bme590hrm

[![Build Status](https://travis-ci.com/mjp59/bme590hrm.svg?branch=master)](https://travis-ci.com/mjp59/bme590hrm)


The current developed program is written in python 3.7. The main to activate the program is from the command line using the command, "python heartrate.py <filename>". The user has the option to enter their file used in the program from the command line as an argument. The file must be a csv file. If no file is enter in the command line then the program will ask the user for a input file to run on. The csv file must consist of a time (column 1) and voltage (column 2) array in the csv in the correct columns. If these requirements are met by the data file then the program will execute properly. Any data in the csv file outside the first two columns will simply be ignored by the program. 
	Once the program has both its time and voltage arrays, it will operate as a peak finding algorthim to find the qs peaks in the ecg signal.  The program will find the peaks within the user defined time window, that must be a window within the start and end time of the signal. This will be the most likely spot errors outside of the user uploading a bad file. 
		The peak finding algothrim works by taking the differential of the ecg signal. The average and the standard deviation of the differential are taken of the differential. These values are used to determine the thresholding of the signal. The signal counts as a beat if value of the differential signal is above the threshold and does not occur with .08 seconds of the previous peaks. This stops double counting of the peaks from occurring. The thresholding used for the check peak algorthim also changes depending on the standard deviation and the snr of the signal. 
		The program will then use the time location of the peaks to calculate the average heart rate over the user window. It will return this value along with the extreme voltages, time of the peaks, the duration of the signal, and the number of peaks/beats in a dictionary. This dictionary will then be output as a json with the name metrics.txt. This file will be updated everytime the programs runs. 
		The program will handle errors and expectations by catching the error, printing a error message, raising the error, and then exiting the program with an exit code of 0 (sys.exit).
		
BONUS: The program is known to work for 25 out of the 32 data files. Test_data files 6, 11, 14, 24, 26, 27, and 28 are not working properly and do not return the correct number of beats in the file. The number of beats were determined by using matlibplot to plot the signals from each data file and manually counting the number of beats. This allowed for accurate testing of the data files by testing the program for the number beats in the signal. Odds are if the program counts the number of manually counted beats that they are where the beats/peaks occur. Plus the peak finding algorthim changes depending on key values of the data set. This allows the program to correctly calculate values for data sets were the patient has wellens diease. The modification of the algorthim is that the abs value of the differential array is taken to make high negative voltage a positive voltage that can be detected by the thresholding. Multiple ways to input filename.  
		
MIT License

Copyright (c) [2018] [Michael Postiglione]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.