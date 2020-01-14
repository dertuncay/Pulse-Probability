import numpy as np
from scipy.interpolate import RegularGridInterpolator
# Load Strike Slip Model
x = np.linspace(0,100,51,dtype=np.int16)
y = np.arange(5.7,8.1,0.1)
z = np.linspace(0,90,91,dtype =np.int16)
Z = np.load('strike_0_90.npy', mmap_mode='r')
interp_kwargs = dict(bounds_error=False)
interp_ss = RegularGridInterpolator((y, x, z), Z, **interp_kwargs)

# Load Smoothed Parameters
x = np.linspace(0,100,51,dtype=np.int16)
y = np.arange(5.4,8.1,0.1)
z = np.linspace(-90,-0,91,dtype =np.int16)
# Footwall
Z = np.load('nss_fw_0_90.npy', mmap_mode='r')
interp_kwargs = dict(bounds_error=False)
interp_nss_fw = RegularGridInterpolator((y, x, z), Z, **interp_kwargs)
# Hangingwall
z2 = np.linspace(0,90,91,dtype =np.int16)
Z2 = np.load('nss_hw_0_90.npy', mmap_mode='r')
interp_kwargs = dict(bounds_error=False)
interp_nss_hw = RegularGridInterpolator((y, x, z2), Z2, **interp_kwargs)

def s2sazfix(ft,s2saz):
  if s2saz > 180 or s2saz < -180:
    raise ValueError('s2saz should not exceed +/- 180. The value of s2saz was: {}'.format(s2saz))
  if ft == 0:
    if s2saz < 0:
      s2saz = abs(s2saz)
    if s2saz > 90:
      s2saz = 180 - s2saz
  elif ft == 1:
    if s2saz > 90:
      s2saz = 180 - s2saz
    elif s2saz < -90:
      s2saz = -1.*(180+s2saz)
  return s2saz

def prob_calc(ft,mw,rjb,s2saz):
  if ft not in [0,1]:
    raise ValueError('ft should be 0 or 1. The value of ft was: {}'.format(ft))
  s2saz = s2sazfix(ft,s2saz)
  if ft == 0:
    return interp_ss(np.array([mw, rjb, s2saz]))[0]
  else:
    if s2saz < 0:
      return interp_nss_fw(np.array([mw, rjb, s2saz]))[0]
    else:
      return interp_nss_hw(np.array([mw, rjb, s2saz]))[0]
''' 
Inputs:
ft = Fault type (0 = strike slip, 1 = non-strike slip)
mw = Moment magnitude
drjb = Rjb distance (km)
s2saz = source-to-site azimuth (degree)
Usage:
interp_xxx(np.array([mw, drjb, s2saz]))[0]
Output:
Probability of observing impulsive signal
'''

# Example 1
# Inputs:
# ft = 0 mw = 7.4 rjb = 10 s2saz = 45
ft = 0
mw = 7.4
rjb = 10
s2saz = 45
print(prob_calc(ft,mw, rjb, s2saz))

# Example 2
# Inputs:
# ft = 1 mw = 7.0 rjb = 20 s2saz = 70
ft = 1
mw = 7.0
rjb = 10
s2saz = 70
print(prob_calc(ft,mw, rjb, s2saz))


# Example 2
# Inputs:
# ft = 1 mw = 6.2 rjb = 5 s2saz = -10
ft = 1
mw = 6.2
rjb = 5
s2saz = -10
print(prob_calc(ft,mw, rjb, s2saz))
