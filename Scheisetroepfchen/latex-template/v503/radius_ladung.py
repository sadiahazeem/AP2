from struct import unpack
from io import StringIO
import matplotlib.pyplot as plt
import numpy as np


############################ einlesen der werte aus txt ############################

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

f_397 = StringIO('''
2.06    4.23
1.40    2.44
3.72    1.84
3.4     2.15
8.36    4.18
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




############################ konstanten definieren ############################

rho_oel = 886           # in kg pro m^3
rho_luft = 1.2041       # "
g = 9.81                # in newton pro kg
eta21_unk = 1.8275e-5   # in N*s*m^-2, aus der abbildung in der anleitung
eta22_unk = 1.834e-5    
eta23_unk = 1.8375e-5
d = 7.6250e-3           # plattenabstand kondensator in metern
b = 0.008226                # cunningham-faktor in pascal*meter
p = 101325              # Luftdruck durchschnittlich in pascal




############################ Viskosität korrigieren nach Cunningham ############################

eta21 = eta21_unk
eta22 = eta22_unk   
eta23 = eta23_unk




############################ zeiten in geschwindigkeiten umwandeln, radien berechnen ############################

tauf_220, tab_220 = np.genfromtxt(f_220, unpack = True)
vauf_220 = -5e-4/tauf_220
vab_220 = 5e-4/tab_220
r220 = np.sqrt((9*eta23*(vab_220 - vauf_220))/(2*g*(rho_oel - rho_luft)))
print("------------- die radien der Tröpchen bei 2,20V. der erste und fünfte wert sind wichtig ", r220) # hier sind der erste und fünfte wert wichtig

tauf_304, tab_304 = np.genfromtxt(f_304, unpack = True)
vauf_304 = -5e-4/tauf_304
vab_304 = 5e-4/tab_304
r304 = np.sqrt((9*eta22*(vab_304 - vauf_304))/(2*g*(rho_oel - rho_luft)))
print("------------- die radien der Tröpchen bei 3,04V. der zweite wert ist wichtig ", r304)              # -------> bei U = 3,97V sind alle messwerte ungültig lol, daher nicht aufgeführt

tauf_457, tab_457 = np.genfromtxt(f_457, unpack = True)
vauf_457 = -5e-4/tauf_457
vab_457 = 5e-4/tab_457
r457 = np.sqrt((9*eta21*(vab_457 - vauf_457))/(2*g*(rho_oel - rho_luft)))
print("------------- die radien der Tröpchen bei 4,57V. der vierte wert ist wichtig ", r457)    # hier ist der vierte wert wichtig

tauf_491, tab_491 = np.genfromtxt(f_491, unpack = True)
vauf_491 = -5e-4/tauf_491
vab_491 = 5e-4/tab_491
r491 = np.sqrt((9*eta23*(vab_491 - vauf_491))/(2*g*(rho_oel - rho_luft)))
print("------------- die radien der Tröpchen bei 4,91V. der vierte wert ist wichtig ", r491)    # hier ist der vierte wert wichtig 



############################ Viskosität korrigieren nach Cunningham ############################

#eta21 = eta21_unk * (1/(1 + (b/(p*r457))))
#eta22 = eta22_unk   # wird nicht benötigt
#eta23_220 = eta23_unk * (1/(1 + (b/(p*r220))))
#eta23_491 = eta23_unk * (1/(1 + (b/(p*r491))))

eta21 = eta21_unk 
eta22 = eta22_unk   # wird nicht benötigt
eta23_220 = eta23_unk 
eta23_491 = eta23_unk 




############################ e-felder berechnen ############################

E220 = 2.2 / d
E304 = 3.04 / d
E457 = 4.57 / d
E491 = 4.91 / d



############################ ladungen bestimmen ############################

q220 = 3*np.pi*eta23_220*np.sqrt((9*eta23_220*(vab_220-vauf_220))/(4*g*(rho_oel - rho_luft)))*((vab_220 + vauf_220)/E220)
print("------------- die unkorrigierten ladungen der Tröpchen bei 2,20V. der erste und fünfte wert sind wichtig ", q220) # hier sind der erste und fünfte wert wichtig


q304 = 3*np.pi*eta22*np.sqrt((9*eta22*(vab_304-vauf_304))/(4*g*(rho_oel - rho_luft)))*((vab_304 + vauf_304)/E304)
print("------------- die unkorrigierten ladungen der Tröpchen bei 3,04V. der zweite wert ist wichtig ", q304) # hier ist der zweite wert wichtig


q457 = 3*np.pi*eta21*np.sqrt((9*eta21*(vab_457-vauf_457))/(4*g*(rho_oel - rho_luft)))*((vab_457 + vauf_457)/E457)
print("------------- die unkorrigierten ladungen der Tröpchen bei 4,57V. der vierte wert ist wichtig ", q457)    # hier ist der vierte wert wichtig


q491 = 3*np.pi*eta23_491*np.sqrt((9*eta23_491*(vab_491-vauf_491))/(4*g*(rho_oel - rho_luft)))*((vab_491 + vauf_491)/E491)
print("------------- die unkorrigierten ladungen der Tröpchen bei 4,91V. der vierte wert ist wichtig ", q491)    # hier ist der vierte wert wichtig 

# print("-------------test: datentyp ist", type(q220))



############################ ladungen korrigieren ############################

q220_korr = q220 * (1/(1+(b/(p*r220))))**3/2
print("---------------- die korrigierte ladung bei 2,20V beträgt (erster und fünfter wert): ", q220_korr)

q304_korr = q304 * (1/(1+(b/(p*r304))))**3/2
print("---------------- die korrigierte ladung bei 3,04V beträgt (zweiter wert): ", q304_korr)

q457_korr = q457 * (1/(1+(b/(p*r457))))**3/2
print("---------------- die korrigierte ladung bei 4,57V beträgt (vierter wert): ", q457_korr)

q491_korr = q491 * (1/(1+(b/(p*r491))))**3/2
print("---------------- die korrigierte ladung bei 4,91V beträgt (vierter wert): ", q491_korr)




