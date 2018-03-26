'''
Calculating Orbital Elements (Keplerian elements) from Line 2 of TLE and
plotting the figure.

graphics.py is taken from https://github.com/Elucidation/OrbitalElements

Important:
In order to get the plot you have to first install Tkinter.
Type the following command into your terminal.

$ sudo apt-get install python-tk
'''

import urllib
import graphics
import numpy as np

GM = 398600.4418
pi = np.pi

def eccentricity_anomaly(anomaly, eccentricity, init, iter=500, accuracy = 0.0001):
    '''
    Calculates true anomaly from the mean anomaly

    Args:
        anomaly : mean anomaly
        eccentricity : eccentricity
        init : initial anomaly
        iter : maximum number of iterations (default 500)
        accuracy : threshold (default 0.0001)

    Returns:
        true anomaly
    '''

    for i in xrange(iter):
        true = init - (init - eccentricity * np.sin(init) - anomaly) / (1.0 - eccentricity * np.cos(init))
        if (abs(true-init) < accuracy):
            break
    return true

def orbital_elements(name, data):
    '''
    Calcualtes orbital elements from line 2 of TLE and plots it

    Args:
        name : name of the satellite
        data : line 2 of TLE for finding Keplerian elements

    Returns:
        NIL
    '''

    line = list(data)
    inclination = float(''.join(line[8:16]))
    ascension = float(''.join(line[17:25]))
    eccentricity = float(''.join(line[26:33]))/10000000
    perigee = float(''.join(line[34:42]))
    anomaly = float(''.join(line[43:51]))
    motion = float(''.join(line[52:63]))

    sec_in_day = 24*60*60
    period = sec_in_day * 1./motion
    semi_major_axis = ((period/(2*pi))**2 * GM)**(1./3)

    true_anomaly = eccentricity_anomaly(anomaly*pi/180, eccentricity, anomaly*pi/180)

    print "\n=== Orbital Elements ==="
    print "Semi-major Axis                                  : ", semi_major_axis
    print "Inclination (degrees)                            : ", inclination
    print "Right ascension of the ascending node (degrees)  : ", ascension
    print "Eccentricity                                     : ", eccentricity
    print "Argument of perigee (degrees)                    : ", perigee
    print "True Anomaly                                     : ", true_anomaly

    graphics.plotOrbit(semi_major_axis, eccentricity, inclination, ascension, perigee, true_anomaly, name)
    graphics.plotEarth()
    graphics.doDraw()

    return ;

# Reading NORAD TLE data
link = "https://celestrak.com/NORAD/elements/cubesat.txt"
data = urllib.urlopen(link)
d = data.read()
d = d.splitlines()

num = 1
name = d[num*3 - 3]
line1 = d[num*3 - 2]
line2 = d[num*3 - 1]
print name + "\n" + line1 + "\n" + line2
print "\n----------------------------\n"
print "Satellite_Name : " + name + "\n"
orbital_elements(name, line2)
