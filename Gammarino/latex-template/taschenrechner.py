import numpy as np

zinkp = 2   # mm

faktoren = np.linspace(1, 10, 10)

rot = 1.02  # mm
gelb = 1.04 # mm
supergelb = 10.02  # mm
hypergelb = 20.04  # mm

d1 = rot
d2 = 2*rot
d3 = 3*rot
d4 = 4*rot
d5 = 4*rot + gelb
d6 = 4*rot + 2*gelb
d7 = 4*rot + 2*gelb + supergelb
d8 = 4*rot + 2*gelb + 2*supergelb
d9 = hypergelb
d10 = rot + supergelb 

print(" d1 =", d1)
print(" d2 =", d2)
print(" d3 =", d3)
print(" d4 =", d4)
print(" d5 =", d5)
print(" d6 =", d6)
print(" d7 =", d7)
print(" d8 =", d8)
print(" d9 =", d9)
print(" d10 =", d10)