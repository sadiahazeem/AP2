import matplotlib
matplotlib.use('MacOSX', force=True)
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
import uncertainties as unp
import matplotlib.ticker as plticker#
try:
    from PIL import Image
except ImportError:
    import Image



s = 0.5 * 10**-2
t = 1.8 *10**-6

print("v = ", s/t)


########## brusttumor ##########

#print("durchmesser der beiden kleinen löcher zusammen: ", 2/7 * 13.8)
#print("durchmesser des festen tumors: ", 1.5 * 13.8)
#print("tiefe des festen tumors: ", 1.4 * 13.8)
#print("tiefe des flüssigen tumors: ", 1.8 * 13.8)



########## bscan tiefen und durchmesser auswerten ##########

#print("--------von oben: --------")
#print("tiefe von 8: ",  4.25 * 13.8)
#print("tiefe von 7: ",  3.7 * 13.8)
#print("tiefe von 6: ",  3 * 13.8)
#print("tiefe von 5: ",  1.8 * 13.8)
#print("tiefe von 4: ",  2.4 * 13.8)
#print("tiefe von 3: ",  1.8 * 13.8)
#print("tiefe von 2: ",  1.25 * 13.8)
#print("tiefe von 1: ",  0.7 * 13.8)
#print("tiefe von k1: ", 8.1*1/9 * 13.8)
#print("tiefe von k2: ", 7.2*1/9 * 13.8)
#print("tiefe von G: ",  4.1 * 13.8)
#print("--------von unten: --------")
#print("tiefe von 8: ",  0.6 * 13.8)
#print("tiefe von 7: ",  1.2 * 13.8)
#print("tiefe von 6: ",  1.9 * 13.8)
#print("tiefe von 5: ",  2.3 * 13.8)
#print("tiefe von 4: ",  3.0 * 13.8)
#print("tiefe von 3: ",  3.5 * 13.8)
#print("tiefe von 2: ",  4.1 * 13.8)
#print("tiefe von 1: ",  4.6 * 13.8)
#print("tiefe von k1: ", 3.9 * 13.8)
#print("tiefe von k2: ", 4.0 * 13.8)
#print("tiefe von G: ",  1.1 * 13.8)
#print("durchmesser von 8: ",  0.3 * 13.8)
#print("durchmesser von 7: ",  0.2 * 13.8)
#print("durchmesser von 6: ",  0.18 * 13.8)
#print("durchmesser von 5: ",  0.15 * 13.8)
#print("durchmesser von 4: ",  0.1 * 13.8)
#print("durchmesser von 3: ",  0.08 * 13.8)
#print("durchmesser von 2: ",  0.1 * 13.8)
#print("durchmesser von 1: ",  0.1 * 13.8)
#print("durchmesser von k1: ", 0.07 * 13.8)
#print("durchmesser von k2: ", 0.07 * 13.8)
#print("durchmesser von G: ",  0.25 * 13.8)



########## Abweichungen ##########


def abw(lit, exp):
    proz = (lit - exp)/lit * 100
    return proz


#       LOCH 3
print("3: Abweichung A unten: ",  abw(23.4, 24.2))
print("3: Abweichung A oben: ",  abw(55.1, 55.6))
print("3: Abweichung B unten: ",  abw(23.4, 24.84))
print("3: Abweichung B oben: ",  abw(55.1, 48.3))

#       LOCH 7
print("7: Abweichung A unten: ",  abw(54.2, 54.9))
print("7: Abweichung A oben: ",  abw(22.1, 22.9))
print("7: Abweichung B unten: ",  abw(54.2, 51.1))
print("7: Abweichung B oben: ",  abw(22.1, 16.6))

#       LOCH G
print("G: Abweichung A unten: ",  abw(16.4, 16.7))
print("G: Abweichung A oben: ",  abw(55.5, 56.5))
print("G: Abweichung B unten: ",  abw(16.4, 15.2))
print("G: Abweichung B oben: ",  abw(55.5, 56.6))

#           oben    unten    unten a           oben a
#      3  &  23.4  & 55.1  &  24.2   &       & 55.6  &       &       &        &       \\
#      7  &  54.2  & 22.1  &  54.9   &       & 22.9  &       &       &        &       \\
#      G  &  16.4  & 55.5  &  56.5   &       & 16.7  &       &       &        &       \\

print("5: Abweichung A Durchmesser: ",  abw(2.8, 3.41))
print("5: Abweichung B Durchmesser: ",  abw(2.8, 2.07))

c_s = unp.ufloat(2714, 30)
print("Abweichung Schallgeschwindigkeit: ",  abw(2730, c_s))


print("anpassungsschicht in mm: ", 0.05601347899463367*1e-2*2730)
print("Laufzeitkorrektur soll: ", 4*1e-3/2730)