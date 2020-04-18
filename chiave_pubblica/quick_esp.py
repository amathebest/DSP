import math
import datetime as dt
import numpy as np

print("Insert a: ")
a = int(input())
print("Insert m: ")
m = int(input())
print("Insert n: ")
n = int(input())

d = 1
c = 0
binary_exp = np.binary_repr(m)

# processing
initial_dt = dt.datetime.now()

for i in range(len(binary_exp)):
    d = (d*d) % n
    c = 2*c
    if int(binary_exp[i]) == 1:
        d = (d*a) % n
        c += 1
ending_dt = dt.datetime.now()
time = ending_dt - initial_dt
print(str(a) + "^" + str(m) + " mod " + str(n) + " = " + str(d))
print("The computation took", time.microseconds*1000, "ms.")
