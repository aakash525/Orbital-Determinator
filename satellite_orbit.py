import urllib2
import graphics
import numpy as np

# sudo apt-get install python-tk

GM = 398600.4418
pi = np.pi

def eccentricity_anomaly(anomaly, eccentricity, init, iter=500, accuracy = 0.0001):

    for i in xrange(iter):
        true = init - (init - eccentricity * np.sin(init) - anomaly) / (1.0 - eccentricity * np.cos(init))
        if (abs(true-init) < accuracy):
            break
    return true

def orbital_elements(name, data):
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

data = urllib2.urlopen("http://www.celestrak.com/NORAD/elements/stations.txt")
d = data.read()
d = d.splitlines()

print d[0] + "\n" + d[1] + "\n" + d[2]
print "\n----------------------------\n"
print "Satellite_Name : " + d[0] + "\n"
orbital_elements(d[0], d[2])
