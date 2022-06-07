import matplotlib
matplotlib.use('MacOSX', force=True)
import matplotlib.pyplot as plt
import numpy as np

t_a = np.array([1.08e-05, 1.68e-05, 2.33e-05, 2.93e-05, 3.50e-05, 4.07e-05, 4.67e-05, 4.43e-05,
 4.56e-05, 3.27e-05, 1.22e-05, 4.56e-05, 4.02e-05, 3.47e-05, 2.93e-05, 2.35e-05,
 1.77e-05, 1.19e-05, 1.52e-05, 1.41e-05, 6.10e-06, 4.14e-05])

s_a = np.array([0.0294, 0.0462, 0.0632, 0.0798, 0.0954, 0.1114, 0.1274, 0.1214, 0.1244, 0.0802,
 0.0332, 0.1244, 0.1096, 0.0942, 0.08, 0.0642, 0.0488, 0.0328, 0.0414, 0.0388,
 0.0168, 0.113])

print(s_a)

params, covariance_matrix = np.polyfit(t_a, s_a, deg=1, cov=True)
errors = np.sqrt(np.diag(covariance_matrix))
x_pl = np.linspace(0, 100)

plt.figure()
plt.plot(t_a, s_a, 'mx', label='Messwerte der Laufzeiten')
plt.plot(x_pl, (params[0] * x_pl + params[1]), label='Lineare Regression')
plt.xlabel('t in second')
plt.ylabel('s in m')
plt.xlim(0, 45)
plt.ylim(0, 13)
plt.legend()
plt.grid()
plt.show()