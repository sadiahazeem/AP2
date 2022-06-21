from struct import unpack
import matplotlib
matplotlib.use('MacOSX', force=True)
import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as const
import uncertainties



############################# DATEN EINLESEN #############################

c = 2730 # m/s 
c_w = 1480  # im wasser

tiefe  = 4*10**(-2)      # abmessungen acrylblock
breite = 15.02*10**(-2)
hoehe  = 8.04*10**(-2)

t_oben, t_unten, s_oben, s_unten, s_obens, s_untens = np.genfromtxt("ascan.txt", unpack = True)
t_oben *= 10**-6    # µs zu s
t_unten *= 10**-6
s_oben *= 2*10**-3    # mm zu m, mal 2 wegen Impuls-Echo
s_unten *= 2*10**-3
s_obens *= 2*10**-3
s_untens *= 2*10**-3
t_a = np.append(t_oben, t_unten) 
s_a = np.append(s_obens, s_untens) 
s_schieb = np.append(s_oben, s_unten) 
print(s_a)

############################# MITTELUNG ZU C UND ANPASSUNGSSCHICHT #############################

# korrekturzeit = t_schall - t_(aus s gemessen mit schall) | s = v*t

korr_o =  t_oben - (s_obens/c)
#print("korrekturzeiten oben: ", korr_o)
korr_u = t_unten - (s_untens/c)
#print("korrekturzeiten unten: ", korr_u)
korr_beide = np.array([korr_o, korr_u])
korr = np.mean(korr_beide)
#print("korrekturzeit gesamt: ", korr)


# lineare regression der form 2*s = c*t + d  |  d ist die anpassungsschicht
params, covariance_matrix = np.polyfit(t_a*10**6, s_a*10**2, deg=1, cov=True)
errors = np.sqrt(np.diag(covariance_matrix))

for name, value, error in zip('ab', params, errors):
    print(f'{name} = {value:.3f} ± {error:.3f}')


x_plot = np.linspace(0, 45)

plt.figure()
plt.plot(t_a*10**(6), (s_a*10**(2)+0.372), 'mx', label='Messwerte der Laufzeiten')
plt.plot(x_plot, (params[0] * x_plot + params[1]+0.372), label='Lineare Regression', color = "tab:purple")
plt.xlabel('t / µs')
plt.ylabel('s / cm')
plt.xlim(0, 45)
plt.ylim(0, 13)
plt.legend()
plt.grid()

# Output
#plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
#plt.savefig('build/plot.pdf')
#plt.show()
plt.close()
#print("paramteter c und anpassungsschichtdicke d, fehler von d: ", params[0], params[1], errors[1])


############################# LÖCHER TIEFE UND MAßE #############################

print("korrekturzeit prüfen: ", 3*10**3/2730)

def lochdicke(tu, to):
    s_u = 0.5 * c * tu * 10**2
    s_o = 0.5 * c * to * 10**2
    d = hoehe*10**2 - s_u - s_o + 0.3     # korrektur von 0.3 
    d = np.round(d, 3)
    return d

def sdurchlaufen(t):
    s = 0.5*10**2 * c * t
    return s

# theoretische lochdicke
loecher = hoehe*10**2 - s_unten*1/2*10**2 - s_oben*1/2*10**2

print("lochdurchmesser in cm: ", lochdicke(t_unten, t_oben))
print("errechnete strecke in cm: ", loecher)        # hier ist noch was faul
print("tiefe in cm von unten: ", np.round(sdurchlaufen(t_unten),2))
print("tiefe in cm von oben: ", np.round(sdurchlaufen(t_oben),2))


############################# AUFLÖSUNGSVERMÖGEN #############################

# abbildungen einfügen, evtl a scan neu plotten (nur txt datei??)

zwei_o, zwei_u, ein_o, ein_u = np.genfromtxt("aufloesung.txt", unpack = True)




# KORREKTUR: FIT STRECKE/LAUFZEIT
x_fit = np.linspace(0, 25, 20) 
pm_k, cov_k = np.polyfit(0.5*(t_a*10**(6)), ((t_a*2730)*10**(2)-(0.5*s_schieb*10**(2))), deg = 1, cov = True)    # x in s und y in m
errors = np.sqrt(np.diag(cov_k))
plt.figure()
plt.plot(0.5*t_a*10**(6), ((t_a*2730)*10**(2)-(0.5*s_schieb*10**(2))-0.36), 'mx', label='Messwerte der Laufzeiten')
plt.plot(x_fit, (pm_k[0]*x_fit + pm_k[1]-0.36), "m-", alpha = 0.5, label = "Ausgleichsgerade")
plt.ylabel('Tiefe s / cm')
plt.xlabel('Laufzeit t / µs')
plt.ylim(0, 7.5)
plt.xlim(0, 25)
plt.legend()
plt.grid()
#plt.show()
print("parameter c und anpassungsschichtdicke d, fehler von c in µs: ", pm_k[0], pm_k[1], errors[0])


def abw(lit, exp):
    proz = (lit - exp)/lit * 100
    return proz

sascan = np.array([80.04-24.2-55.6, 80.04-54.9-22.9, 80.04-16.7-56.5])
sbscan = np.array([80.04-24.8-48.3, 80.04-51.1-16.6, 80.04-15.2-56.6])
gemessen = np.array([2.75, 4.55, 9.95])
print("Berechnete Durchmesser A-Scan: ", sascan)
print("Berechnete Durchmesser B-Scan: ", sbscan)
print("Abweichungen a-scan: ", abw(gemessen, sascan))
print("Abweichungen b-scan: ", abw(gemessen, sbscan))