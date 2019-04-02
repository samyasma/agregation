from pylab import *

def lj(r, epsilon=1.0, sigma=1.0):

	if r > 0.0:
		return epsilon*(sigma**12/r**12-sigma**6/r**6)
	else:
		return None

x=arange(0.5,2.5,0.001)
vlj = vectorize(lj)

plot(x, vlj(x))
show()