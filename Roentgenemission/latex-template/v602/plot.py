import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import uncertainties.unumpy as unp
import sympy
import statistics
from scipy.optimize import curve_fit
from uncertainties import ufloat
from scipy.signal import find_peaks
import scipy.constants as const
from scipy.interpolate import UnivariateSpline

e=const.e
h=const.h
c=const.c
d_KBr=329*10**(-12) #m
ry=13.6 #eV
alpha=const.value("fine-structure constant")

################################################################

x = np.linspace(0, 10, 1000)
y = x ** np.sin(x)

plt.subplot(1, 2, 1)
plt.plot(x, y, label='Kurve')
plt.xlabel(r'$\alpha \mathbin{/} \unit{\ohm}$')
plt.ylabel(r'$y \mathbin{/} \unit{\micro\joule}$')
plt.legend(loc='best')

plt.subplot(1, 2, 2)
plt.plot(x, y, label='Kurve')
plt.xlabel(r'$\alpha \mathbin{/} \unit{\ohm}$')
plt.ylabel(r'$y \mathbin{/} \unit{\micro\joule}$')
plt.legend(loc='best')

# in matplotlibrc leider (noch) nicht möglich
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/plot.pdf')


#print (f'\n -----------------------------------Emissionsspektrum-----------------------------------')
#theta_cu,N_cu = np.genfromtxt('content/emissionsspektrum.txt', unpack = True)
#N_max = find_peaks(N_cu, height=1000)
#N_peak_cu = N_cu[N_max[0]]
#theta_peak_cu = theta_cu[N_max[0]]
#plt.plot(theta_cu, N_cu,'kx',label = 'Messdaten')
#plt.ylabel(r'$N \,/\, \mathrm{\frac{Imp}{s}}$')
#plt.plot(theta_cu[0:120],N_cu[0:120],'r--',label = 'Bremsberg')
#plt.plot(theta_cu[127:143],N_cu[127:143],'r--')
#plt.plot(theta_cu[150:180],N_cu[150:180],'r--')
#plt.axvline(theta_peak_cu[0], color='steelblue', ls = '--', label = r'$K_{\mathrm{\beta}}$')
#plt.axvline(theta_peak_cu[1], color='g', ls = '--', label = r'$K_{\mathrm{\alpha}}$')
#plt.xlabel(r'$\theta \,/\, °$')
#plt.legend()
#plt.tight_layout()
#plt.savefig("build/emissionsspektrum.pdf")
#plt.close()



#print (f'\n -----------------------------------Moseleysches-Gesetz-----------------------------------')
#
#Z = np.array ([30,31,35,38,40])
#E_K = np.array ([E_K_zn,E_K_ga,E_K_br,E_K_sr, E_K_zr])
#
#params, covariance_matrix = np.polyfit(Z, np.sqrt(E_K), deg=1, cov=True)
#
#x_plot = np.linspace(30, 40)
#plt.plot(
#    x_plot,
#    params[0] * x_plot + params[1],
#    color='steelblue',ls='-', label='Lineare Regression',
#    linewidth=3,
#   
#)
#plt.plot(Z, np.sqrt(E_K), 'kx',label="Messdaten")
#plt.legend(loc="best")
#plt.ylabel(f"Wurzel aus $E_K$")
#plt.xlabel(f"Ordnungszahl Z")
#plt.legend()
#plt.tight_layout()
#plt.savefig("build/moseley.pdf")
#plt.close()
#rconst=(params[0]**2)*e/(h*c)
#
#print(f"Ausgleichsgerade g={params[0]}x {params[1]}")
#ry_m=(params[0]**2)/h
#rconstabs=10973731.56816-((params[0]**2)*e/(h*c))
#rconstrel=(10973731.56816-(params[0]**2)*e/(h*c))/10973731.56816
#
#
#print(f"berechnete rydberg energie = {params[0]**2} rydberg const {rconst} ryconst abs{rconstabs} ryconst rel {rconstrel}")
#