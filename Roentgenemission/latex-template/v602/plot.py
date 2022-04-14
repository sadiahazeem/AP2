import matplotlib.pyplot as plt
import numpy as np


################################################################

#x = np.linspace(0, 10, 1000)
#y = x ** np.sin(x)
#
#plt.subplot(1, 2, 1)
#plt.plot(x, y, label='Kurve')
#plt.xlabel(r'$\alpha \mathbin{/} \unit{\ohm}$')
#plt.ylabel(r'$y \mathbin{/} \unit{\micro\joule}$')
#plt.legend(loc='best')
#
#plt.subplot(1, 2, 2)
#plt.plot(x, y, label='Kurve')
#plt.xlabel(r'$\alpha \mathbin{/} \unit{\ohm}$')
#plt.ylabel(r'$y \mathbin{/} \unit{\micro\joule}$')
#plt.legend(loc='best')
#
## in matplotlibrc leider (noch) nicht möglich
#plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
#plt.savefig('build/plot.pdf')

####################################################

x, Y = np.genfromtxt('content/mess2.txt', unpack=True)
Y = Y * 1000
y = np.sqrt(Y)


params, covariance_matrix = np.polyfit(x, y, deg=1, cov=True)

errors = np.sqrt(np.diag(covariance_matrix))

print('---------------------------- a = {:.3f} ± {:.4f}'.format(params[0], errors[0]))
print('---------------------------- b = {:.3f} ± {:.4f}'.format(params[1], errors[1]))

def gerade (x, m, b):
    return m*x+b

z = np.linspace(np.min(x) - 3, np.max(x) + 3)

plt.plot(x, y, 'rx', label='Messdaten')
plt.plot(z, gerade (z, *params), 'b-', label='Ausgleichsgerade')
plt.xlim(np.min(x) - 3, np.max(x) + 3)
plt.xlabel(r'$Z$')
plt.ylabel(r'$\sqrt{E_k} \: / \: \sqrt{eV}$')
plt.legend(loc='best')

plt.tight_layout()
plt.savefig('build/plot_moseley.pdf')
plt.close()



theta, counts = np.genfromtxt("content/absorptionZN.txt", unpack=True)

theta=1*theta   # oder doch theta halbieren?
max = theta[np.argmax(counts)]
print("Maximum bei ",max)

plt.figure(figsize=(4.76, 2.94))
plt.axvline(max,color="r",label="Position der K-Kante")
plt.plot(theta, counts, 'k.', label="Daten", ms=2.5)
plt.legend(loc="best")
plt.grid()
plt.xlabel(r'$\theta$ / $\si{\degree}$')
plt.ylabel(r'Rate / $\si{\per\second}$')

# in matplotlibrc leider (noch) nicht möglich
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/zink.pdf')
plt.close()


w_Cu, R_Cu = np.genfromtxt('content/emissionsspektrum.txt', unpack=True)
w1 = w_Cu[76:84]
R1 = R_Cu[76:84]
w2 = w_Cu[88:98]
R2 = R_Cu[88:98]

plt.plot(w_Cu, R_Cu, 'b-', label='Bremsberg')
plt.plot(w2, R2, 'g-', label=r'$K_\alpha$')
plt.plot(w1, R1, 'r-', label=r'$K_\beta$')
#plt.axvline(x = 11.9, color="r-",label='$K_\beta$ -Linie')
#plt.axvline(max, color="g-",label="$K_\alpha-Linie$")
plt.grid()
plt.ylim(0, 6500)
plt.legend()
plt.xlabel('Kristallwinkel $ \Theta$ in $^\circ$')
plt.ylabel(r'Zählrate in Impulse/$s$')
plt.savefig('build/plot_cu.pdf')
plt.close()


