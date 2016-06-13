#! /usr/bin/python

"""
electronics.py
Used to calculate optimal values of components for the desired resolution of measurements 
Started by Andy Wickert on 20 May, 2011.
"""

from __future__ import division # No floor division

def thermistor(R_T,B,R_ref,T0=25,ADC_bits=10,part_number='',VCC=3.3,Tmin=-40,Tmax=50):
  """
  Provides the resolution of a thermistor (R_T), in degrees C, as a function of 
  temperature (T0) with the assumption that the thermistor is placed as the first 
  resistor in a voltage divider

  Thermistor with resistance R_T at temperature T0 (usually 25 degrees C).
  B is the thermistor's B-value in Kelvin; see:
  http://en.wikipedia.org/wiki/Thermistor#B_parameter_equation
  and
  http://www.mathworks.com/help/toolbox/physmod/elec/ref/thermistor.html
  R_Ref is the resistance of the reference resistor in the voltage divider.
  ADC_bits is the analog-to-digital converter resolution; defaults to 10-bit
  part_number is for plotting; it defaults to nothing, but can be used to provide
  manufacturer or DigiKey part numbers on the plot
  Tmin and Tmax are the min and max temperatures to display in degrees C

  Function by default shows a range of -40 to 50 degrees C; this should be about the 
  bounds that we'll ever see in Colorado, and the lower bound is the limit of the 
  ratings of quite a bit of electronic equipment.
  Uses the B-equation
  VCC is really unnecessary, as it gets normalized out, but including it in case I 
  want to involve it in some plots in the future
  """

  # IMPORT LIBRARIES
  
  import numpy as np
  from matplotlib import pyplot as plt
  
  # SET UP TEMPERATURE RANGE  
  
  dT = 0.1 # degrees C
  T = np.arange(Tmin,Tmax+dT,dT)
  Tmid = (T[0:-1]+T[1:])/2 # For use with diff(V)
  
  # CALCULATE RESOLUTION
  
  res = 2**ADC_bits - 1
  
  # CALCULATE RESISTANCE OF THERMISTOR AS f(T)
  
  r_inf = R_T * np.exp(-B/(273.15+T0)) # expect T0 in degC, so convert it to Kelvin
  R = r_inf * np.exp(B/(T+273.15))
  
  # CALCULATE VOLTAGE DIVIDER OUTPUT
  
  V = VCC * R_ref/(R+R_ref)
  
  # Provide entire dynamic range
  # Not really necessary; will always output b/t 0 and VCC
  # Vmin = (V>=0).nonzero() # Don't see how we could go below this
  # Vmax = 
  
  # CALCULATE CHANGE IN VOLTAGE WITH CHANGE IN TEMPERATURE
  
  dVdT = np.diff(V) / dT
  ADC_intervals_per_volt = res/VCC
  deg_C_per_ADC_interval = 1/(dVdT*ADC_intervals_per_volt)

  # PLOT
  
  fig = plt.figure(1)
  
  plt.title('Thermistor ' + str(part_number) + ': $R_T=$' + '%.1f'%(R_T/1000) + 
              'k$\Omega$; $R_r = $' + '%.1f'%(R_ref/1000) + 'k$\Omega$; $B = $' + 
              str(B) + 'K',fontsize=16)
  
  plt.xlabel('Temperature ($^\circ$C)',fontsize=16)
  plt.ylabel('Resolution ($^\circ$C)',fontsize=16)
  
  plt.plot(Tmid,deg_C_per_ADC_interval)
  
  plt.show()
