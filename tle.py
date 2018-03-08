import urllib2
import array
from datetime import datetime, timedelta

def find_year(year):
    if(year >=0 and year <=56):
        year += 2000
    else:
        year += 1900

    return year;

def find_date(date):
    year = find_year(int(''.join(date[0:2])))
    day = int(''.join(date[2:5]))

    days_in_month = array.array('i', [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])

    if(year % 4 == 0):
        days_in_month[1] = 29

    i = 0
    month = 0
    while(day > 0):
        day -= days_in_month[i]
        month = i
        i += 1

    day += days_in_month[month]

    year = str(year)
    month = str(month)
    day = str(day)

    year = day + "/" + month + "/" + year
    return year;

def find_time(time):
    second = timedelta(float(time)/1000)
    time = datetime(1,1,1) + second

    hour = str(time.hour)
    minute = str(time.minute)
    second = str(time.second)
    time = hour + ":" + minute + ":" + second
    return time;

def calculate_checksum(line):
    check = 0
    for i in range(0,68):
        if(line[i].isdigit()):
            check += int(line[i])
        elif(line[i] == "-"):
            check += 1

    return check % 10;

def line1(data):
    line = list(data)
    satellite_num = ''.join(line[2:7])
    launch_year = find_year(int(''.join(line[9:11])))
    launch_num = ''.join(line[11:14])
    launch_piece = ''.join(line[14:17])
    # epoch_year = ''.join(line[20:23])
    epoch_date = find_date(''.join(line[18:23]))
    epoch_time = find_time(''.join(line[24:32]))
    first_derivative = ''.join(line[33:43])
    second_derivative = ''.join(line[44:52])
    bstar_sign = line[53]
    bstar = float(''.join(line[54:59]))/100000
    bstar_exp = ''.join(line[59:61])
    bstar = bstar_sign + str(bstar) + "e" + bstar_exp
    ephemeris = line[62]
    element = int(''.join(line[64:68]))
    checksum = int(line[68])
    check = calculate_checksum(line);

    if(element > 999):
        element -= 999

    print "=== Line_Number : ", line[0], "==="
    if(line[7] == 'U'):
        print "Satellite_Number                                 : ", satellite_num, " (Unclassified)"
    else:
        print "Satellite_Number                                 : ", satellite_num, " (Classified)"
    print "International_Designator                         : Year - ", launch_year, " Launch - ", launch_num, " Piece - ", launch_piece
    print "Epoch                                            : Date - ", epoch_date, " Time - ", epoch_time
    print "First time derivative of the Mean Motion         : ",  first_derivative
    print "Second time derivative of the Mean Motion        : ", second_derivative
    print "BSTAR drag term                                  : ", bstar
    print "Ephemeris type                                   : ", ephemeris
    print "Element number                                   : ", element
    if(checksum == check):
        print "Checksum                                         : ", checksum, " (Verified : Matched)"
    else:
        print "Checksum                                         : ", checksum, " (Verified : Not Matched)"

    return ;

def line2(data):
    line = list(data)
    satellite_num = ''.join(line[2:7])
    inclination = ''.join(line[8:16])
    ascension = ''.join(line[17:25])
    eccentricity = float(''.join(line[26:33]))/10000000
    perigee = ''.join(line[34:42])
    anomaly = ''.join(line[43:51])
    motion = ''.join(line[52:63])
    revolution_num = ''.join(line[63:68])
    checksum = int(line[68])
    check = calculate_checksum(line);

    print "\n\n=== Line_Number : ", line[0], "==="
    print "Satellite_Number                                 : ", satellite_num
    print "Inclination (degrees)                            : ", inclination
    print "Right ascension of the ascending node (degrees)  : ", ascension
    print "Eccentricity                                     : ", eccentricity
    print "Argument of perigee (degrees)                    : ", perigee
    print "Mean Anomaly (degrees)                           : ", anomaly
    print "Mean Motion (revolutions per day)                : ", motion
    print "Revolution number at epoch                       : ", revolution_num
    if(checksum == check):
        print "Checksum                                         : ", checksum, " (Verified : Matched)"
    else:
        print "Checksum                                         : ", checksum, " (Verified : Not Matched)"

    return ;

data = urllib2.urlopen("http://www.celestrak.com/NORAD/elements/stations.txt")
d = data.read()
d = d.splitlines()

print d[0] + "\n" + d[1] + "\n" + d[2]
print "\n----------------------------\n"
print "Satellite_Name : " + d[0] + "\n\n"
line1(d[1])
line2(d[2])
