from struct import unpack
import matplotlib
matplotlib.use('MacOSX', force=True)
import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as const
import uncertainties as unp
from scipy import stats
from scipy.optimize import curve_fit
import pandas as pd
from scipy.stats import norm
from sympy.solvers import solve
from sympy import Symbol



p30, ch30, n30 = np.genfromtxt("30mm.txt", unpack = True)
p36, ch36, n36 = np.genfromtxt("36mm.txt", unpack = True)
n100 = np.genfromtxt("statistik.txt", unpack = True)


############## REICHWEITE ##############

def efflnge(x0, p0, p):
    x = x0 * (p/p0)
    return x

x30 = efflnge(30, 1013, p30)    # es wird mit einem Normaldruck von 1013 mBar gerechnet
x36 = efflnge(36, 1013, p36)

# plotten
plt.figure()
plt.plot(x30, n30, "mx", label = "Zählrate bei 30mm Abstand")
plt.plot(x36, n36, "yx", label = "Zählrate bei 36mm Abstand")



# lineare regression und gerade auf höhe des halben max 
xw = np.linspace(0, 30, 30)
halb30 = np.linspace(np.max(n30)/2, np.max(n30)/2, 30)
halb36 = np.linspace(np.max(n36)/2, np.max(n36)/2, 30)

plt.plot(xw, halb30, "m--", alpha = 0.4, label = "Hälfte des Maximums bei 30mm")
plt.plot(xw, halb36, "y--", alpha = 0.6, label = "Hälfte des Maximums bei 36mm")

# lin reg | bei 30 von [-6] bis [-1], bei 36 von [] bis [] (letzten 5 werte)

params30, ma30 = np.polyfit(x30[-6:-1], n30[-6:-1], deg = 1, cov = True)
params36, ma36 = np.polyfit(x36[-4:], n36[-4:], deg = 1, cov = True)
print("parameter 30mm: ", params30)
print("parameter 36mm: ", params36)

xlin = np.linspace(15, 28, 40)
plt.plot(xlin, (params30[0]*xlin + params30[1]), "m-", alpha = 0.4)
plt.plot(xlin, (params36[0]*xlin + params36[1]), "y-", alpha = 0.6)
plt.xlabel("effektive Länge in mm")
plt.ylabel("Zählrate N")
plt.plot()
plt.legend(prop={'size': 8})
plt.grid()
#plt.show()
plt.close()


############## SCHNITTPUNKTE BERECHNEN ############## 
x = Symbol('x')
print("schnittpunkt 30 mm: ", solve(params30[0]*x + params30[1] - np.max(n30)/2))
print("schnittpunkt 36 mm: ", solve(params36[0]*x + params36[1] - np.max(n36)/2))




############## ENERGIEN ##############

def energieausR(r):              # mit R = 3.1 * E^3/2??
    E = ((r)/3.1)**(3/2)         # r in mm einsetzen
    return E

E30 = energieausR(23.5626305123838)
E36 = energieausR(23.7616497760509)

print("Energie aus R bei 30mm: ", E30)
print("Energie aus R bei 36mm: ", E36)



def ChInE(ch, ch_list):         # mit channel
    channel_max = np.max(ch_list)
    channel_min = 0
    m = 4/(channel_max - channel_min)
    d = 4 - (channel_max*m)
    return m * ch + d

e30 = ChInE(ch30, ch30)
print("e30: ", e30)
e36 = ChInE(ch36, ch36)

plt.figure(dpi = 150)
plt.plot(x30[:-1], e30[:-1], "mx", label = "Messwerte")
pm30, cov30 = np.polyfit(x30[:-1], e30[:-1], cov = True, deg = 1)
pm36, cov36 = np.polyfit(x36[:-1], e36[:-1], cov = True, deg = 1)
plt.plot(x30[:-1], (x30[:-1]*pm30[0] + pm30[1]), "m-", alpha = 0.4, label = "lineare Regression")
plt.legend(loc="best")
plt.xlabel("effektive Länge in mm")
plt.ylabel("Energie in MeV")
plt.grid()
plt.show()
plt.close()


plt.figure(dpi = 150)
plt.plot(x36[:-1], e36[:-1], "yx", label = "Messwerte")
plt.plot(x36[:-1], (x36[:-1]*pm36[0] + pm36[1]), "y-", alpha = 0.6, label = "lineare Regression")
plt.legend(loc="best")
plt.xlabel("effektive Länge in mm")
plt.ylabel("Energie in MeV")
plt.grid()
plt.show()
plt.close()

print("Energieverlust 30mm: ", pm30[0])
print("Energieverlust 36mm: ", pm36[0])

############## STATISTIK ##############

nu = np.mean(n100)
print("Statistik - Mittelwert: ", nu)
print("Statistik - Summe: ", np.sum(n100))
print("Statistik - Minimum: ", np.min(n100))
print("Statistik - Maximum: ", np.max(n100))

t = np.linspace(3700, 4400) 
sigma = (sum((n100-nu)**2)/(100))**(1/2)
p_n= np.random.normal(nu, sigma, 10000)
p_p= np.random.poisson(nu, 10000)
print('Sigma der Gaußglocke: ', sigma)

##plotten
plt.figure(dpi = 150)
plt.hist(n100,  bins=26, color = 'k',  alpha=0.5, density=True, label='Messwerte')
plt.hist(p_p, bins=26, color='g', alpha=0.5, density=True, label='Poissonverteilung')
plt.hist(p_n, bins=26, color='y', alpha=0.5, density=True, label='Gaußverteilung')
plt.legend(loc="best")
plt.xlabel("Zählrate N")
plt.ylabel("P(N)")
plt.show()



def abw(lit, exp):
    proz = (lit - exp)/lit * 100
    return proz

print("Prozentuale Abweichung E: ", abw(21.22, 20.96))
print("Prozentuale Abweichung x: ", abw(23.76, 23.56))
