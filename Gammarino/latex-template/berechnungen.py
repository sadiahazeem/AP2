from struct import unpack
import matplotlib
matplotlib.use('MacOSX', force=True)
import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as const
import uncertainties as unp
from scipy import stats
from scipy.optimize import curve_fit
from scipy.stats import norm
#import pandas as pd
#from sympy.solvers import solve
#from sympy import Symbol

# gemessen werden d, ∆d, t und N 
n0 = 0
d_pb, t_pb, N_pb = np.genfromtxt("v704/content/messpb.txt", unpack = True)

# ---- einheiten umrechnen ----
d_pb *= 10**-3

# ---- lin Reg, x: d, y: log(N_pb) ----
logN_pb = np.log(N_pb)
pm_pb, cov_pb = np.polyfit(d_pb, logN_pb, deg = 1, cov = True)
std = np.sqrt(np.diag(cov_pb))
m_pb = unp.ufloat(pm_pb[0], std[0])
b_pb = unp.ufloat(pm_pb[1], std[1])
print("m und b von Blei: ", m_pb, b_pb)
print('Blei: N durch t - n0', N_pb/t_pb-n0)

xdata = np.linspace(0, 0.025, 2000)
plt.errorbar(d_pb*1e3, np.log((N_pb/t_pb-n0)), np.sqrt(N_pb/t_pb-n0), fmt='x', color = "tab:purple", label='Messwerte')                    # noch mal kontrollieren ob log an der richtigen stelle
plt.plot(xdata*1e3, (unp.nominal_value(m_pb)*xdata + unp.nominal_value(b_pb)), '-', color = "tab:purple", alpha = 0.5, label='Ausgleichsfunktion')
##plt.yscale('log')
#plt.xlim(0, 22)
#plt.ylim(10, 170)
plt.xlabel("d in mm")
plt.ylabel("Impulse N")
plt.legend(loc='best')
plt.tight_layout()
#plt.show()
plt.close()

# --------------> für zweites material und betastrahlung einfach kopieren und pb bzw Blei ersetzen


# compton-absorptionskorffizient µ_com

eps_cs = 1.295 
r_e = 2.82e-15 # in metern, (klassischer Elektronenradius)

Z_pb = 82
Z_zn = 30
rho_pb = 11300 # kg/m^3
rho_zn =  7140 # kg/m^3
M_pb =  0.2072 # kg/mol
M_zn = 0.06539 # kg/mol

sigma_com = 2*np.pi*r_e**2*((1+ eps_cs)/eps_cs**2 * (2*(1+eps_cs)/(1+2*eps_cs) - 1/eps_cs*np.log(1+2*eps_cs)) + 1/(2*eps_cs)*np.log(1+2*eps_cs) - (1+ 3*eps_cs)/(1+2*eps_cs)**2)
print("sigma compton in m^2: ", sigma_com)

