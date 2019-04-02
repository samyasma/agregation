from matplotlib.pyplot import *
import math
import numpy

def force(r):
    return 48.0*(math.pow(r,-12)-0.5*math.pow(r,-6))
r = numpy.arange(0.8,4.0,0.01)
f = r.copy()

for i in range(r.size):
    f[i] = force(r[i])

figure(figsize=(8,6))
plot(r,f)
xlabel("distance entre 2 boules")
ylabel("Potentiel répulsion-attraction")
axis([0,4,-4,10])
grid()
show()