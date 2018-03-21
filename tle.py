'''
Two line element parser
Input: Two line Elements
Output: Satellite's information and it's orbital parameters
'''

import urllib2
import numpy as np
from datetime import datetime, timedelta

def find_year(year):
    '''
    Returns year of launch of the satellite.

    Values in the range 00-56 are assumed to correspond to years in the range 2000 to 2056 while
    values in the range 57-99 are assumed to correspond to years in the range 1957 to 1999.

    Args:
        year : last 2 digits of the year

    Returns:
        whole year number
    '''

    if(year >=0 and year <=56):
        return year + 2000;
    else:
        return year + 1900;

def find_date(date):
    '''
    Finds date of the year from the input (in number of days)

    Args:
        date : Number of days

    Returns:
        date in format DD/MM/YYYY
    '''

    year = find_year(int(''.join(date[0:2])))
    day = int(''.join(date[2:5]))

    daysInMonth = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])

    ''' If the year is Leap year or not '''
    if(year % 4 == 0):
        daysInMonth[1] = 29

    i = 0
    month = 0
    while(day > 0):
        day -= daysInMonth[i]
        month = i
        i += 1

    day += daysInMonth[month]

    year = str(day) + "/" + str(month) + "/" + str(year)
    return year;

def find_time(time):
    '''
    Finds date of the year from the input (in milliseconds)

    Args:
        time : Time in milliseconds

    Returns:
        time in format HH:MM:SS
    '''

    second = timedelta(float(time)/1000)
    time = datetime(1,1,1) + second

    hour = str(time.hour)
    minute = str(time.minute)
    second = str(time.second)
    time = hour + ":" + minute + ":" + second
    return time;

def calculate_checksum(line):
    '''
    Checks the integrity of the data

    Args:
        line : Whole line of TLE

    Returns:
        calculated checksum from the line
    '''

    check = 0
    for i in range(0,68):
        if(line[i].isdigit()):
            check += int(line[i])
        elif(line[i] == "-"):
            check += 1

    return check % 10;

def line1(data):
    '''
    Parses line 1 of TLE

    Args:
        data : Line 1 of TLE
    '''

    line = list(data)
    satelliteNum = ''.join(line[2:7])
    launchYear = find_year(int(''.join(line[9:11])))
    launchNum = ''.join(line[11:14])
    launchPiece = ''.join(line[14:17])
    epochDate = find_date(''.join(line[18:23]))
    epochTime = find_time(''.join(line[24:32]))
    firstDerivative = float(''.join(line[33:43]))
    secondDerivative = ''.join(line[44:52])
    bstarSign = line[53]
    bstar = float(''.join(line[54:59]))/100000
    bstarExp = ''.join(line[59:61])
    bstar = bstarSign + str(bstar) + "e" + bstarExp
    ephemeris = line[62]
    element = int(''.join(line[64:68]))
    checksum = int(line[68])
    check = calculate_checksum(line);

    if(element > 999):
        element -= 999

    print "=== Line_Number : ", line[0], "==="
    if(line[7] == 'U'):
        print "Satellite_Number                                 : ", satelliteNum, " (Unclassified)"
    else:
        print "Satellite_Number                                 : ", satelliteNum, " (Classified)"
    print "International_Designator                         : Year -", launchYear, " Launch -", launchNum, " Piece -", launchPiece
    print "Epoch                                            : Date - ", epochDate, " Time - ", epochTime
    print "First time derivative of the Mean Motion         : ",  firstDerivative
    print "Second time derivative of the Mean Motion        : ", secondDerivative
    print "BSTAR drag term                                  : ", bstar
    print "Ephemeris type                                   : ", ephemeris
    print "Element number                                   : ", element
    if(checksum == check):
        print "Checksum                                         : ", checksum, " (Verified : Matched)"
    else:
        print "Checksum                                         : ", checksum, " (Verified : Not Matched)"

    return ;

def line2(data):
    '''
    Parses line 2 of TLE

    Args:
        data : Line 2 of TLE
    '''

    line = list(data)
    satelliteNum = ''.join(line[2:7])
    inclination = float(''.join(line[8:16]))
    ascension = ''.join(line[17:25])
    eccentricity = float(''.join(line[26:33]))/10000000
    perigee = ''.join(line[34:42])
    anomaly = ''.join(line[43:51])
    motion = ''.join(line[52:63])
    revolutionNum = ''.join(line[63:68])
    checksum = int(line[68])
    check = calculate_checksum(line);

    print "\n\n=== Line_Number : ", line[0], "==="
    print "Satellite_Number                                 : ", satelliteNum
    print "Inclination (degrees)                            : ", inclination
    print "Right ascension of the ascending node (degrees)  : ", ascension
    print "Eccentricity                                     : ", eccentricity
    print "Argument of perigee (degrees)                    : ", perigee
    print "Mean Anomaly (degrees)                           : ", anomaly
    print "Mean Motion (revolutions per day)                : ", motion
    print "Revolution number at epoch                       : ", revolutionNum
    if(checksum == check):
        print "Checksum                                         : ", checksum, " (Verified : Matched)"
    else:
        print "Checksum                                         : ", checksum, " (Verified : Not Matched)"

    return ;


# Reading NORAD TLE data
# link = "http://www.celestrak.com/NORAD/elements/stations.txt"
link = "https://celestrak.com/NORAD/elements/cubesat.txt"
data = urllib2.urlopen(link)
d = data.read()
d = d.splitlines()

print d[0] + "\n" + d[1] + "\n" + d[2]
print "\n----------------------------\n"
print "Satellite_Name : " + d[0] + "\n\n"
line1(d[1])
line2(d[2])
