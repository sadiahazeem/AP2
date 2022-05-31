import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import uncertainties.unumpy as unp
from uncertainties import ufloat
import scipy.constants as const
from struct import unpack
from uncertainties.unumpy import (
    nominal_values as noms,
    std_devs as stds,
)


######################### DATEN EINLESEN #########################

uchar, nchar, ichar = np.genfromtxt(fname = "charakteristik.txt", unpack = True)
fehlerN = np.sqrt(nchar)
nchar_f = unp.uarray(nchar, fehlerN)        # wegen Poissonverteilung
print(nchar_f)

######################### FUNKTIONEN DEFINIEREN #########################



######################### lineare Regression für den Plateau-Bereich #########################

# Bereich beschränken auf Plateau

u_pl = uchar[8:-3]
n_pl = nchar[8:-3]
print("Länge des Plateaus: ", u_pl[0], "V bis ", u_pl[17], "V")
print("Länge u_pl: ", u_pl.size)
print("Länge n_pl: ", n_pl.size)


params, covariance_matrix = np.polyfit(u_pl, n_pl, deg = 1 , cov = True)
print("parameter: ", params)

errors = np.sqrt(np.diag(covariance_matrix))
x = np.linspace(u_pl[0], u_pl[-1])

#print(f'a = {params[0]} +- {errors[0]}')
#print(f'b = {params[1]} +- {errors[1]}')
#print(f'Steigung in Prozent pro 100V: {((params[0] * 500 + params[1]) - (params[0] * 400 + params[1])) / 100}')


######################### ZÄHLROHRCHARAKTERISTIK PLOT #########################

# N gegen U auftragen, Steigung des Plateaus berechnen (lin Regression)
# und daran Ausgleichsgerade einzeichnen


plt.figure()
plt.errorbar(uchar, unp.nominal_values(nchar_f), label = "Messdaten", fmt='yx', yerr=fehlerN)
plt.plot(x, params[0] * x + params[1], label = 'Plateau-Ausgleichsgerade', color = 'green')
plt.xlabel(r'Spannung U in V')
plt.ylabel(r'Zählrate N')
plt.legend(loc = 'best')
plt.tight_layout()
#plt.show()
plt.close()

print('Steigung in Prozent pro 100V: ', ((params[0] * 600 + params[1]) - (params[0] * 500 + params[1])) / 100)



######################### TOTZEIT #########################


# 2. zwei-quellen-methode 

N1 = 96041.0 / 120.0
N2 = 76518.0 / 120.0
N21 = 158479.0 / 120.0

n1 =  ufloat(N1, np.sqrt(N1))
n2 =  ufloat(N2, np.sqrt(N2))
n21 = ufloat(N21, np.sqrt(N21))

T = (n1 + n2 - n21) / (2 * n1 * n2)

print(f'Totzeit T = {T}')

U2 = np.array([500,500,500])
N2_ohne = np.array([21844, 39105, 17594])
deltan2 = np.sqrt(N2_ohne)
N2 = unp.uarray(N2_ohne, deltan2)

N3=unp.uarray(21844,np.sqrt(21844))
N4=unp.uarray(39105,np.sqrt(39105))
N34=unp.uarray(17594,np.sqrt(17594))
N=[N3,N4,N34]
T=(N3/120+N4/120-N34/120)/(1/60*N3*N4)
print("N3, N4 und N34 mit Fehler: ", N2)
print("Totzeit 2 bestimmt: ", T)
T_abgelesen = 150e-6
T_zweiQ = unp.uarray(253.8e-6, 0.001e-6)
print("Totzeit noch mal: ", T_zweiQ)



######################### FREIGESETZTE LADUNG NACH ZÄHLROHRSPANNUNG #########################

I = ichar
I *= 10**(-6) # I in A 
nchar /= 120 

Nerr = unp.uarray(nchar, np.sqrt(nchar))
Ierr = unp.uarray(I, 0.05 * 10**(-6))
Z = Ierr / (Nerr)   # vorher Z = Ierr / (const.elementary_charge * Nerr)
#I *= 10**6 # I in µA

print("freigesetzte Ladungsmenge in Coulomb: ", Z*10**-9)

plt.figure()
plt.errorbar(uchar, unp.nominal_values(Z*10**10), label = "Messdaten", fmt='yx', yerr=unp.std_devs(Z))
#plt.plot(x, params[0] * x + params[1], label = 'Plateau-Ausgleichsgerade', color = 'green')
plt.xlabel(r'Spannung U in V')
plt.ylabel(r'Freigesetzte Ladungen in $e_0$')
plt.legend(loc = 'best')
plt.tight_layout()
#plt.show()
plt.close()


######################### ABWEICHUNGEN #########################

def abw(lit, exp):
    proz = (lit - exp)/lit * 100
    return proz

print("Prozentuale Abweichung der 2-Quellen-M von abgelesenem Wert: ", abw(T_abgelesen, T_zweiQ))