from struct import unpack
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
from uncertainties import ufloat
import uncertainties.unumpy as unp


########################## KONSTANTEN DEFINIEREN ##########################

T_0 = 273.15 # kelvin
p_0 = 1013.2e-3 # bar
b = 50e-3 # meter, länge der messkammer 
p = 0.8 # bar


########################## FUNKTIONEN DEFINIEREN ##########################

def lambda_1(z, deltaD):
    #d_h = deltaD/5.046
    lambd = (2*deltaD/5.046)/z
    return lambd

def delta_n(lambda_2, z, b):
    del_n = (z*lambda_2)/(2*b)
    return del_n

def N(T, p_vorher, p_strich, deltaN):
    N = 1 + deltaN * T/T_0 * p_0/(p_vorher - p_strich)
    return N




########################## WERTE EINLESEN ##########################

#Z1 = StringIO('''
#    3100
#    3120
#    3100
#    3070
#    3090
#    3080
#    3010
#    3090
#    3030
#    3050
#''')
#
#Z2 = StringIO('''
#    48  47
#    60  45
#    44  41
#''')
#
#

Z1 = np.genfromtxt('zaehlraten.txt', unpack = True)
Z2 = np.genfromtxt('zaehlraten2.txt', unpack = True)



########################## BERECHNUNGEN TEIL 1 ##########################

wellenl_1 = lambda_1(Z1, 5e-3)
print("---------- wellenlaengen laser:", wellenl_1)



########################## MIT FEHLER ##########################

Z1_f = unp.uarray(Z1, 5)
wellenl_f = lambda_1(Z1_f, 5e-3)
print("---------- LAMBDA mit fehler von 5:", wellenl_f)

mittel1 = np.mean(wellenl_f)
print("---------- lambda MITTEL mit fehler:", mittel1)


########################## BERECHNUNGEN TEIL 2 ##########################

Z2_f = unp.uarray(Z2, 5)
delN = delta_n(635e-9, Z2_f, 50e-3)
eta = N(20, 800, 0, delN)
print("---------- BRECHUNGSINDEX luft mit fehler von 5:", eta)
mittel2 = np.mean(eta)
print("---------- brechungsindex MITTEL mit fehler:", mittel2)


########################## BERECHNUNGEN DISKUSSION ##########################

abw_lambd = 100*(635-645)/635 
print("---------- ABWEICHUNG LAMBDA in %", abw_lambd)

abw_luft = 100*(1.000292-1.0000000280)/1.000292
print("---------- ABWEICHUNG LUFT in %", abw_luft)
