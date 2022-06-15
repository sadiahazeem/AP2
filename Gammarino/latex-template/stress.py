from struct import unpack
import matplotlib
matplotlib.use('MacOSX', force=True)
import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as const
import uncertainties.unumpy as unp
from scipy import stats
from scipy.optimize import curve_fit
from scipy.stats import norm
from uncertainties import ufloat



# gemessen werden d, ∆d, t und N 
n0 = 941        # über 300s gemessen
N_pb, t_pb, d_pb = np.genfromtxt("v704/content/bleiii.txt", unpack = True)
N_pb /= t_pb
print("nullaktivität gamma: ", n0/300)


# ---- lin Reg, y-achse logarithmiert
logdpb = np.log(d_pb)
pm_pb, cov_pb = np.polyfit(d_pb, np.log(unp.nominal_values(N_pb)), deg = 1, cov = True)
std = np.sqrt(np.diag(cov_pb))
m_pb = ufloat(pm_pb[0], std[0])
b_pb = ufloat(pm_pb[1], std[1])

xdata = np.linspace(0.5, 27, 45)
plt.errorbar(d_pb, unp.nominal_values(N_pb), fmt='x', color = "m", yerr= unp.std_devs(N_pb), label='Messwerte')
plt.plot(xdata, np.exp((unp.nominal_values(m_pb)*xdata + unp.nominal_values(b_pb))), '-', color = "m", alpha = 0.5, label='Ausgleichsfunktion')
plt.yscale('log')
#plt.xlim(0, 22)
#plt.ylim(10, 170)
plt.xlabel("d in mm")
plt.ylabel("Impulse N/s")
plt.legend(loc='best')
plt.tight_layout()
#plt.show()
plt.close()

print("m und b von Blei: ", m_pb*1e3, b_pb)
#print(" N pro Sekunde von Blei: ", N_pb)



N_zn, t_zn, d_zn = np.genfromtxt("v704/content/zinkipinki.txt", unpack = True)
N_zn -= n0
N_zn = unp.uarray(N_zn, np.sqrt(N_zn))
N_zn /= t_zn

# ---- lin Reg, y-achse logarithmiert
logdzn = np.log(d_zn)
pm_zn, cov_zn = np.polyfit(d_zn, np.log(unp.nominal_values(N_zn)), deg = 1, cov = True)
std = np.sqrt(np.diag(cov_zn))
m_zn = ufloat(pm_zn[0], std[0])
b_zn = ufloat(pm_zn[1], std[1])

xdata = np.linspace(0.5, 20, 45)
plt.errorbar(d_zn, unp.nominal_values(N_zn), fmt='x', color = "tab:purple", yerr= unp.std_devs(N_zn), label='Messwerte')
plt.plot(xdata, np.exp((unp.nominal_values(m_zn)*xdata + unp.nominal_values(b_zn))), '-', color = "tab:purple", alpha = 0.5, label='Ausgleichsfunktion')
plt.yscale('log')
#plt.xlim(0, 22)
#plt.ylim(10, 170)
plt.xlabel("d in mm")
plt.ylabel("Impulse N/s")
plt.legend(loc='best')
plt.tight_layout()
#plt.show()
plt.close()

print("m und b von Zink: ", m_zn*1e3, b_zn)
#print(" N pro Sekunde von Zink: ", N_zn)


#            BETASTRAHLUNG

n0 = (603/900)
N_beta, t_beta, d_beta = np.genfromtxt("v704/content/beta.txt", unpack = True)
N_beta -= n0
#print(N_beta - n0)
N_beta = unp.uarray(N_beta, np.sqrt(N_beta))
N_beta /= t_beta

# ---- lin Reg, y-achse logarithmiert
logdbeta = np.log(d_beta)
pm_beta, cov_beta = np.polyfit(d_beta[:-6], np.log(unp.nominal_values(N_beta[:-6])), deg = 1, cov = True)
std = np.sqrt(np.diag(cov_beta))        # erste gerade (oben)
m_beta = ufloat(pm_beta[0], std[0])
b_beta = ufloat(pm_beta[1], std[1])

pm_beta2, cov_beta2 = np.polyfit(d_beta[5:], np.log(unp.nominal_values(N_beta[5:])), deg = 1, cov = True)
std2 = np.sqrt(np.diag(cov_beta2))        # zweite gerade (unten)
m_beta2 = ufloat(pm_beta2[0], std2[0])
b_beta2 = ufloat(pm_beta2[1], std2[1])

xdata = np.linspace(0.5, 300, 50)
xdata2 = np.linspace(0.5, 500, 50)
plt.errorbar(d_beta, unp.nominal_values(N_beta), fmt='yx', yerr= unp.std_devs(N_beta), label='Messwerte')
plt.plot(xdata, np.exp((unp.nominal_values(m_beta)*xdata + unp.nominal_values(b_beta))), '--', color = "tab:purple", alpha = 0.45, label='Ausgleichsfunktion 1')
plt.plot(xdata2, np.exp((unp.nominal_values(m_beta2)*xdata + unp.nominal_values(b_beta2))), '--', color = "tab:purple", alpha = 0.7, label='Ausgleichsfunktion 2')
plt.yscale('log')
#plt.xlim(0, 22)
#plt.ylim(10, 170)
plt.xlabel("d in µm")
plt.ylabel("Impulse N/s")
plt.legend(loc='best')
plt.tight_layout()
#plt.show()
plt.close()
print("m und b von beta: ", m_beta*1e3, b_beta)
print("m und b von beta 2: ", m_beta2*1e6, b_beta2)

R = (b_beta2 - b_beta)/(m_beta*1e3 - m_beta2*1e8)
print("R von Beta: ", R)
Rmax = 2700*R
Emax = 1.92*np.sqrt(unp.nominal_values(Rmax)**2 + 0.22*unp.nominal_values(Rmax))
print("maximale Reichweite Beta: ", Rmax)
print("maximale Energie Beta: ", Emax)


# compton-absorptionskoeffizient µ_com

eps_cs = 1.295 
r_e = 2.82e-15 # in metern, (klassischer Elektronenradius)

Z_pb = 82
Z_zn = 30
rho_pb = 11340 # kg/m^3
rho_zn =  7140 # kg/m^3
M_pb =  0.2072 # kg/mol
M_zn = 0.06539 # kg/mol

sigma_com = 2*np.pi*r_e**2*((1+ eps_cs)/eps_cs**2 * (2*(1+eps_cs)/(1+2*eps_cs) - 1/eps_cs*np.log(1+2*eps_cs)) + 1/(2*eps_cs)*np.log(1+2*eps_cs) - (1+ 3*eps_cs)/(1+2*eps_cs)**2)
print("sigma compton in m^2: ", sigma_com)
# (z = Ordnungszahl, N_l = Loschmidtsche Zahl, M = Molekulargewicht, ρ = Dichte)
# mu = sigma * (z*N*rho)/M
############# für aluminium (gar nicht nötig lol)
z = 13
Nl = 2.68*1e25
rho_al = 2700 # kg/m^3
m = 1e-7 * rho_al
mu_coma = sigma_com * (z*Nl*rho_al)/m
#print("mu compton: ", mu_coma)

z = 82                      # BLEI
m = 18.26*1e-6 * rho_pb
mu_comp = sigma_com * (z*Nl*rho_pb)/m
print("mu compton blei m^-1: ", mu_comp)

z = 30                      # ZINK  (soll eig 50.544)
m = 9.16*1e-6 * rho_zn
mu_comz = sigma_com * (z*Nl*rho_zn)/m
print("mu compton zink m^-1: ", mu_comz)

print("nullaktivität beta: ", n0)