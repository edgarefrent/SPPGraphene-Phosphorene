# -*- coding: utf-8 -*-
"""Prueba05Dic.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bL1FbxXxS-FAWTTPYbD9wHQdcHdpSlhw
"""

import numpy as np
import matplotlib.pyplot as plt

# constantes
hbar = 1.0545e-34
tau = 1e-12
e = 1.6021e-19
mu = 0.9 * e    #0.9eV
c = 2.9979e8
n1 = 1.6
n2 = 1.6
epsilon_0 = 8.8546e-12
epsilon_1 = n1**2
epsilon_2 = n2**2

# Se define la conductividad sigma
def sigma(omega):
    return (1j * e**2 * mu) / (np.pi * hbar**2 * (omega + 1j/tau))

# Se define la función f
def f(omega, kx, ky):
    term1 = epsilon_1 / np.sqrt(((omega**2 / c**2) * epsilon_1 - (kx + 1j*ky)**2))
    term2 = epsilon_2 / np.sqrt(((omega**2 / c**2) * epsilon_2 - (kx + 1j*ky)**2))
    numerador = sigma(omega)
    denominador = epsilon_0 * omega
    return term1 + term2 + numerador / denominador

# Definición de la función ksp (Choon)
def ksp(omega):
    return ((n1**2 + n2**2) * (1j * omega * epsilon_0)) / sigma(omega)


# Define el rango de valores para omega y kx
frequencies = np.linspace(0.1e12, 10e13, 1000)  # Valores de f en rad/s pasando por los THz
# Calcular omega usando la relación omega = 2 * pi * f
omega = 2 * np.pi * frequencies
kx_values = np.linspace(0.1, 1e6, 1000)

# Se crea una cuadrícula de valores para omega y kx
omega_grid, kx_grid = np.meshgrid(omega, kx_values)

# Se crea una cuadrícula de valores para f y kx
f_grid, kx_grid = np.meshgrid(frequencies, kx_values)

# Se evalúa la función para las omega,kx y ky constante
z = f(omega_grid, kx_grid, ky=0)

# Se aplica el log(f^2)
w = (abs(z))**2
h = np.log(w)

# Se evalúa ksp en función de la frecuencia angular omega
m =  ksp(omega)

# Parámetros para la línea de luz 1 w = c*kx/n1
light_line1 = (kx_values * c)//(n1 * 2 * np.pi)

# Parámetros para la línea de luz 2 w = c*kx
light_line2 = (kx_values * c)//(n2 * 2 * np.pi)

# Se crea la gráfica de contorno sobre un plano 2D
plt.contourf(kx_grid, f_grid, h, levels=100, cmap='binary')
plt.plot(kx_values, light_line1, label='Light line', color='orange')
#plt.plot(light_line2, kx_values, label='Línea de luz n2')
plt.plot(np.real(m), frequencies, label='Re[$K_{SP}$]',linestyle='--', color='g')
plt.ylabel('f (Hz)')
plt.xlabel('$k_x$ (1/m)')
plt.xlim(0,1e6)
plt.ylim(0,3e13)
plt.colorbar(label='$\log[|f( \omega, {k_x}_R, {k_x}_I)|^2 ]$')
plt.legend(loc='upper left')
plt.show()

