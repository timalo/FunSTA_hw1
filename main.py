import csv
import numpy as np
import math

def main():
    with open("measurements.csv", mode="r") as m:
        with open("groundtruth.csv", mode="r") as g:
            csv_file = csv.reader(m)
            groundtruth_file = csv.reader(g)
            result_array = []
            groundtruth_array = []
            for line in csv_file:
                result_array.append(line)
            for csv_line in groundtruth_file:
                groundtruth_array.append(csv_line)

    truth_array = []
    for line in groundtruth_array:
        s1 = line[0]
        s2 = line[1]
        s3 = line[2]
        pieceOfS = [s1, s2, s3]
        for i in range(len(pieceOfS)):
            truth_array.append(pieceOfS[i])
    s = np.array([truth_array], dtype='float')
    s = np.transpose(s)
    M_array = []
    for line in result_array:
        r1 = line[0]
        r2 = line[1]
        r3 = line[2]
        pieceOfM = [[r1, r2, r3, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, r1, r2, r3, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, r1, r2, r3, 1]]
        #don't do this        
        for line in pieceOfM:
            M_array.append(line)

    M = np.matrix(M_array, dtype='float')
    b = np.dot(np.linalg.pinv(M), s)

    a11 = float(b[0])
    a12 = float(b[1])
    a13 = float(b[2])
    b1 = float(b[3])
    a21 = float(b[4])
    a22 = float(b[5])
    a23 = float(b[6])
    b2 = float(b[7])
    a31 = float(b[8])
    a32 = float(b[9])
    a33 = float(b[10])
    b3 = float(b[11]) #don't look at this, it is horrible

    A = np.matrix([[a11, a12, a13], [a21, a22, a23], [a31, a32, a33]])

    bMatrix = np.matrix([[b1], 
                        [b2],
                         [b3]])

    def correctMeasurement(meas):
        corrected = []
        meas_array = np.array([[meas[0]],
                                [meas[1]],
                                [meas[2]]], dtype='float')
        corrected = (A * meas_array + bMatrix)
        return corrected

    corrected_array = []
    for line in result_array:
        corrected_line = correctMeasurement(line)
        corrected_array.append(corrected_line)


    error_array = []

    for i in range(len(corrected_array)):
        temp_list = []
        for j in range(len(corrected_array[i])):
            r = round(float(corrected_array[i][j]) - float(groundtruth_array[i][j]), 5)
            temp_list.append(r)
        error_array.append(temp_list)
    
    #print(minimumSquare(error_array))
    #print(result_array)
    print(minimumSquare(np.array(result_array, dtype='float')))
    """for line in error_array:
        print(line)"""
    #error_array contains the error of the measurements compared to the ground truth, which is given in groundtruth.csv


def minimumSquare(errors):
    """Function for calculating the least minimum square sum
    Takes in a error_array which contains the error of every measurement"""
    sum_of_errors = 0
    for line in errors:
        square = math.sqrt(line[0]**2 + line[1]**2 + line[2]**2)
        sum_of_errors += square

    return sum_of_errors

if __name__ == "__main__":
    main()

#e = s - y
#e = error
#s = ground truth (found in other file)
#y = measurement
#r can also be substituted in place of y

#half assed way of checking square sum of errors
