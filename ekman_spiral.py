# Import basic maths and scientific Python routines for integration:
import numpy as np
from scipy import eye
from scipy.integrate import ode

#Define a function that returns 2*i - q^2/K(t).
#Here t stands for z+h, y stands for q, and arg1 is any parameter
#argument (you can have more than one, i.e. arg1, arg2):
def f(t, y, arg1):
   #Specify K(z) here, which uses arg1:
   K=1.0+arg1*t
   return 2.0j-y**2/K   #j here is sqrt(-1) in Python

#Specify parameters:
h_in = input(' Depth h of upper layer (default: 1)? ')
h=float(h_in or 1.0)

mu_in = input(' Surface eddy viscosity mu (default: 2)? ')
mu=float(mu_in or 2.0)

#This is the parameter to be passed to the function above:
a=(mu-1.0)/h

#Define integrator and set initial values and parameter(s):
r = ode(f).set_integrator('zvode', method='bdf')
r.set_initial_value(1.0+1.0j).set_f_params(a)
#If you need to pass two parameters, say a & b, use (a,b) at end of this line.

#Set interval size in z for output:
dz=h/2500.0

#Open output files to contain the real and imaginary parts of q(z):
qr_file = open('qr.asc','w')
qi_file = open('qi.asc','w')
print(1.0, -h, file=qr_file)
print(1.0, -h, file=qi_file)

#Solve ode:
while r.successful() and r.t < h-1.e-10:
   r.integrate(r.t+dz)
   qr=float(r.y.real)
   qi=float(r.y.imag)
   z=float(r.t)-h
   print(qr, z, file=qr_file)
   print(qi, z, file=qi_file)

print ('')
print (' The surface deflection angle is ',np.arctan(qi/qr)*180.0/np.pi)
print ('')
print (' The real & imaginary parts of q vs z are in qr.asc & qi.asc')
