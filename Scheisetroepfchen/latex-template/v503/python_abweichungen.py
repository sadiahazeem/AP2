from struct import unpack
from io import StringIO
import matplotlib.pyplot as plt
import numpy as np

f = StringIO('''
-0.06   0.09
-0.26   0.07
-0.41   0.11
0.12    0.21
-0.174  1.74
0.25    0.15
-0.27   0.09
0.26    0.14
0.32    0.13
0.65    0.09
0.29    0.1
0.15    0.11
0       0.11
0.07    0.09
0.07    0.125
0.3     0
-0.17   0.13
-0.12   0.13
-0.24   0.04
0.13    0.23
-0.22   0
-0.44   0.87
0.17    0
-0.27   0.15
0.23    0
''')


a, b = np.genfromtxt(f, unpack = True)

c = (b-a)*100/(b)
print("abweichungen in prozent")
print(c)