######################## pakete importieren ########################

from struct import unpack       # "meine"
from io import StringIO
import matplotlib.pyplot as plt
import numpy as np

import math                     # bekannte 
import scipy.constants as const
import uncertainties.unumpy as unp
from uncertainties import ufloat
from uncertainties.unumpy import (
    nominal_values as noms,
    std_devs as stds,
)

from scipy.optimize import curve_fit    # keine ahnung was das ist 
#from table import (
#    make_table,
#    make_full_table,
#    make_composed_table,
#    make_SI,
#    write,
#)
#from regression import (
#    reg_linear,
#    reg_quadratic,
#    reg_cubic
#)
#from error_calculation import(
#    MeanError
#)


######################## konstanten definieren ########################

rho_oel = 886           # in kg pro m^3
rho_luft = 1.2041       # "
g = 9.81                # in newton pro kg
eta21_unk = 1.8275e-5   # in N*s*m^-2, aus der abbildung in der anleitung
eta22_unk = 1.834e-5    
eta23_unk = 1.8375e-5
d = ufloat(7.6250e-3, 5.1e-5)           # plattenabstand kondensator in metern
b = 0.008226                # cunningham-faktor in pascal*meter
p = 101325              # Luftdruck durchschnittlich in pascal

eta21 = eta21_unk 
eta22 = eta22_unk   
eta23_220 = eta23_unk # wird nicht benötigt
eta23_491 = eta23_unk
eta23 = eta23_unk

######################## daten einlesen ########################

f_220 = StringIO('''
2.78    3.41
2.67    4.90
12.89   2.85
8.25    2.86
8.09    19.65
''')

f_304 = StringIO('''
2.68    1.64
3.61    6.60    
2.09    4.63
1.68    4.63
9.26    3.01
''')

f_457 = StringIO('''
3.29    2.73
1.76    1.21
3.86    1.49
4.89    11.96
4.53    2.53
''')

f_491 = StringIO('''
0.87    1.96
0.92    1.26
2.27    1.13
1.80    2.46
1.49    1.49
''')

tauf_220, tab_220 = np.genfromtxt(f_220, unpack = True)
tauf_304, tab_304 = np.genfromtxt(f_304, unpack = True)
tauf_457, tab_457 = np.genfromtxt(f_457, unpack = True)
tauf_491, tab_491 = np.genfromtxt(f_491, unpack = True)



######################## funktionen zur berechnung der ladung sowie des radius ########################

#def f_q(U, n, t_auf, t_ab, d):
#    f_q = 3*np.pi*n*10**(-5)*(9/4*n*10**(-5)/9.81*(0.001/t_ab-0.001/t_auf)/(886-1.1644))**(1/2)*(0.001/t_ab+0.001/t_auf)/(U/d)
#    return f_q

def r(n, t_auf, t_ab):
    vauf = -5e-4/t_auf
    vab = 5e-4/t_ab
    r = np.sqrt((9*n*(vab - vauf))/(2*g*(rho_oel - rho_luft)))
    return r

def f_q(U, n, t_auf, t_ab, d):
    vauf = -5e-4/t_auf
    vab = 5e-4/t_ab
    f_q = 3*np.pi*n*np.sqrt((9*n*(vab - vauf))/(4*g*(rho_oel - rho_luft)))*((vab + vauf)/(U/d))
    return f_q



######################## radien und ladungen berechnen ########################

#q_220_unk = f_q(2.2, eta23, tauf_220, tab_220, d)
#print("----------- unkorrigierte ladungen bei 2,2V (1. und 5. wert): ",  q_220_unk)
#q_304_unk = f_q(3.04, eta22, tauf_304, tab_304, d)
#print("----------- unkorrigierte ladungen bei 3,04V (2. wert): ",  q_304_unk)
#q_457_unk = f_q(4.57, eta21, tauf_457, tab_457, d)
#print("----------- unkorrigierte ladungen bei 4,57V (4. wert): ",  q_457_unk)
#q_491_unk = f_q(4.91, eta23, tauf_491, tab_491, d)
#print("----------- unkorrigierte ladungen bei 4,91V (4. wert): ",  q_491_unk)


#r220 = r(eta23, tauf_220, tab_220)
#print("----------- radien bei 2,2V (1. und 5. wert): ",  r220)
#r304 = r(eta22, tauf_304, tab_304)
#print("----------- radien bei 3,04V (2. wert): ",  r304)
#r457 = r(eta21, tauf_457, tab_457)
#print("----------- radien bei 4,57V (4. wert): ",  r457)
#r491 = r(eta23, tauf_491, tab_491)
#print("----------- radien bei 4,91V (4. wert): ",  r491)

r1 = 1.76357777e-06
r2 = 9.11688693e-07
r3 = 1.42732270e-06
r4 = 1.16827163e-06
r5 = 2.14067074e-06
r = np.array([r1,r2,r3,r4,r5])
print("----------- die radien der gültigen messungen: ", r)





######################## werte für den plot zusammenstellen ########################


q1 = ufloat(-2.4871766907999152e-17, 1.6635542456497793e-19)
q2 = ufloat(-1.406902415661818e-17, 9.410101403115112e-20)
q3 = ufloat(-2.7455790551459065e-17, 1.8363873024582456e-19)
q4 = ufloat(-1.4349288690233048e-17, 9.597557025598495e-20)
q5 = ufloat(-3.033877442048127e-17, 2.029216387468256e-19)
q = np.array([q1,q2,q3,q4,q5])
print("----------- die unkorrigierten ladungen der gültigen messungen: ", q)

n = np.array([1,2,3,4,5])


######################## ladungen korrigieren ########################

q_neu = q*(1+(b/(p*r)))**(3/2)
print("----------- die korrigierten ladungen der gültigen messungen: ", q_neu)



# die korrigierten ladungen                     -> dieser block ist gar nicht mehr nötig
#q1_k = ufloat(-2.4871766907999152e-17, 1.6635542456497793e-19)
#q2_k = ufloat(-1.406902415661818e-17, 9.410101403115112e-20)
#q3_k = ufloat(-2.7455790551459065e-17, 1.8363873024582456e-19)
#q4_k = ufloat(-1.4349288690233048e-17, 9.597557025598495e-20)
#q5_k = ufloat(-3.033877442048127e-17, 2.029216387468256e-19)
#q_k = np.array([q1_k,q2_k,q3_k,q4_k,q5_k])
#print("----------- die korrigierten ladungen der gültigen messungen: ", q_k)



############################ plotten ############################
############ zuerst die unkorrigierten ladungen ############
plt.xlim(0.5, 5.5)
#plt.plot(n, unp.nominal_values(q)*10**(19), 'rx', label='Messdaten')
plt.errorbar(n, unp.nominal_values(q)*10**18, fmt='rx', yerr=unp.std_devs(q)*10**18, label='unkorrigierte Messdaten')
#plt.xlabel(r'$\text{Messung}$')
#plt.ylabel(r'$q \:/\: 10^{-18}\si{\coulomb}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
#plt.savefig('build/ladungen_unkorrigiert.pdf')
#plt.show()


############ die korrigierten ladungen ############
plt.clf()
plt.xlim(0.5, 5.5)
plt.errorbar(n, unp.nominal_values(q_neu)*10**18, fmt='rx', yerr=unp.std_devs(q_neu)*10**18, label='korrigierte Messdaten')
#plt.xlabel(r'$\text{Messung}$')
#plt.ylabel(r'$q \:/\: 10^{-18}\si{\coulomb}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
#plt.savefig('build/ladungen_neu.pdf')
#plt.show()



############################ ggT ermitteln und ausgeben ############################  



#def find_gcd(arr):
#    if len(arr) <= 1:
#        return arr
#    else:
#        for i in range(len(arr)-1):
#            a = arr[i]
#            b = arr[i+1]
#            while b:
#                a, b = b, a%b
#            arr[i+1] = a
#        return a



# q_arr = np.array([-2.66e-17, -1.6e-17, -2.89e-17, -1.59e-17, -3.2e-17])


def float_gcd(a, b, rtol = 1e-11, atol = 1e-19):
    t = min(abs(a), abs(b))
    while abs(b) > rtol * t + atol:
        a, b = b, a % b
    return a

runde1 = float_gcd(-2.66e-17, -1.6e-17)         # das wäre natürlich sexier mit einer funktion mit schleife zu lösen
print("---------------- runde 1:", runde1)
runde2 = float_gcd(runde1, -2.89e-17)
print("---------------- runde 2:", runde2)
runde3 = float_gcd(runde2, -1.59e-17)
print("---------------- runde 3:", runde3)
runde4 = float_gcd(runde3, -3.2e-17)
print("---------------- runde 4:", runde4)
e_rel = abs(runde4-1.6021766208*10**(-19))/(1.6021766208*10**(-19))*100
print("---------------- abweichung a in %:", e_rel)



runde1 = float_gcd(-2.49e-17, -1.4e-17)         
print("---------------- runde 1b:", runde1)
runde2 = float_gcd(runde1, -2.75e-17)
print("---------------- runde 2b:", runde2)
runde3 = float_gcd(runde2, -1.43e-17)
print("---------------- runde 3b:", runde3)
runde4 = float_gcd(runde3, -3.03e-17)
print("---------------- runde 4b:", runde4)
e_rel_b = abs(runde4-1.6021766208*10**(-19))/(1.6021766208*10**(-19))*100
print("---------------- abweichung b in %:", e_rel_b)



