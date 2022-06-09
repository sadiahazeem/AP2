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

plt.plot()
plt.legend()
plt.grid()
plt.show()
plt.close()



############## ENERGIEN ##############

# mit R = 3.1 * E^3/2??


def ChInE(ch, ch_list):
    channel_max = np.max(ch_list)
    channel_min = 0
    m = 4/(channel_max - channel_min)
    d = 4 - (channel_max*d)
    return m * ch + d






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

# plotten
#plt.figure()
#plt.hist(n100,  bins=26, color = 'k',  alpha=0.5, density=True, label='Messwerte')
#plt.hist(p_p, bins=26, color='g', alpha=0.5, density=True, label='Poissonverteilung')
#plt.hist(p_n, bins=26, color='y', alpha=0.5, density=True, label='Gaußverteilung')
#plt.legend(loc="best")
#plt.xlabel("Zählrate N")
#plt.ylabel("P(N")
#plt.show()