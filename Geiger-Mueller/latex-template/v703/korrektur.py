import matplotlib
matplotlib.use('MacOSX', force=True)
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import uncertainties.unumpy as unp
from uncertainties import ufloat
import scipy.constants as const
from io import StringIO 
from struct import unpack
from uncertainties.unumpy import (
    nominal_values as noms,
    std_devs as stds,
    uarray
)



charakteristik = StringIO('''
330    12435   0.1
340    13454   0.1
350    13651   0.1
360    13660   0.1
370    13778   0.1
380    13770   0.1
390    13738   0.15
400    14003   0.15
410    14192   0.18
420    13730   0.2
430    14211   0.21
440    13861   0.21
480    14391   0.3
490    14047   0.3
500    14092   0.3
510    14164   0.3
520    14296   0.3
590    14337   0.4
600    14202   0.4
610    14087   0.45
620    14180   0.45
630    14290   0.47
640    14130   0.48
650    14466   0.5
660    14052   0.5
670    14170   0.5
680    14589   0.52
690    14653   0.6
700    14715   0.6
''')

######################### DATEN EINLESEN #########################

uchar, nchar, ichar = np.genfromtxt(charakteristik, unpack = True)
fehlerN = np.sqrt(nchar)
uchar = uchar[1:]
nchar = nchar[1:]
fehlerN=fehlerN[1:]
ichar = ichar[1:]
nchar_f = unp.uarray(nchar, fehlerN)        # wegen Poissonverteilung
print("Zählrate N mit Fehler", nchar_f)

######################### FUNKTIONEN DEFINIEREN #########################



######################### lineare Regression für den Plateau-Bereich #########################

# Bereich beschränken auf Plateau

u_pl = uchar[7:-3]
n_pl = nchar[7:-3]
print("Länge des Plateaus: ", u_pl[0], "V bis ", u_pl[17], "V")
print("Länge u_pl: ", u_pl.size)
print("Länge n_pl: ", n_pl.size)


params, covariance_matrix = np.polyfit(u_pl, n_pl, deg = 1 , cov = True)
print("parameter: ", params)
errors = np.sqrt(np.diag(covariance_matrix))
print("FEHLER parameter: ", errors)


x = np.linspace(u_pl[0], u_pl[-1])


######################### ZÄHLROHRCHARAKTERISTIK PLOT #########################

# N gegen U auftragen, Steigung des Plateaus berechnen (lin Regression)
# und daran Ausgleichsgerade einzeichnen
#print('Steigung in Prozent pro 100V: ', ((params[0] * 600 + params[1]) - (params[0] * 500 + params[1])) / 100)


plt.figure()
plt.errorbar(uchar, unp.nominal_values(nchar_f), label = "Messdaten", fmt='yx', yerr=fehlerN)
plt.plot(x, (params[0] * x + params[1]), label = "Plateau-Ausgleichsgerade", color = "g")
plt.xlabel('Spannung U in V')
plt.ylabel('Zählrate N')
plt.legend(loc = 'best')
#plt.show()
plt.close()




######################### TOTZEIT #########################

# 2-Quellen-Methode


N3=unp.uarray(21844,np.sqrt(21844))
N34=unp.uarray(39105,np.sqrt(39105))           # hier wird in der rechung erst durch 120s geteilt
N4=unp.uarray(17594,np.sqrt(17594))             # nach der fehlerrechnung
T=((N3/120)+(N4/120)-(N34/120))/(1/60*N3*N4)   
#print("N3, N34 und N4 mit Fehler: ", N2)
print("----Totzeit 2 Quellen Methode: ", T)
T_abgelesen = 130e-6



######################### FREIGESETZTE LADUNG NACH ZÄHLROHRSPANNUNG #########################

I = ichar
I *= 10**(-6) # I in A 
nchar /= 120 

def Z3(i, n):
    z = i/(const.elementary_charge * n)
    return z

def fehlerZ(i, n, deltai, deltan):
    fehler = np.sqrt((1/(n*const.elementary_charge))**2 * deltai**2 + (i/(n**2 *const.elementary_charge))**2 * deltan**2 )
    return fehler 


Nerr = unp.uarray(nchar, np.sqrt(nchar))
Ierr = unp.uarray(I, 0.05 * 10**(-6))
Z = Ierr / (const.elementary_charge * Nerr)
#I *= 10**6 # I in µA
print("--------- Z mit Fehler: ", Z)
print("fehler Z: ", fehlerZ(I, nchar, 0.05 * 10**(-6), np.sqrt(nchar))) # gibt realistische ergebnisse ?

def f(x):
    y = m*x + b
    return y


pm, cov = np.polyfit(x = unp.nominal_values(Ierr), y = unp.nominal_values(Z), deg = 1, cov = True)
err = np.sqrt(np.diag(cov))
print("geradenparameter Z und deren fehler : ", pm, err)


plt.figure()
plt.errorbar(I*10**6, unp.nominal_values(Z), label = "Messdaten", fmt='yx', yerr=unp.std_devs(Z))
#plt.plot(x,(pm[0] * x + pm[1]), label = 'Ausgleichsgerade', color = 'green')
plt.xlabel('Strom I in µA')
plt.ylabel('Freigesetzte Elementarladungen')
plt.legend(loc = 'best')
plt.show()
plt.close()


######################### ABWEICHUNGEN #########################

def abw(lit, exp):
    proz = (lit - exp)/lit * 100
    return proz

#print("Prozentuale Abweichung der 2-Quellen-M von abgelesenem Wert: ", abw(T_abgelesen, T_zweiQ))