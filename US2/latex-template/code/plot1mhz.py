# plot zu 1 mhz k1 k2
import matplotlib
matplotlib.use('MacOSX', force=True)
import matplotlib.pyplot as plt
import numpy as np

t1, amp, hf, tgc = np.genfromtxt("1mhzk1k2zeit.txt", unpack = True)

plt.figure()
plt.plot(t1, amp, "m-", label = "Messung bei 1MHz")
plt.xlabel('t / µs')
plt.ylabel('Amplitude / V')
plt.legend()
plt.grid()
plt.show()
plt.close()