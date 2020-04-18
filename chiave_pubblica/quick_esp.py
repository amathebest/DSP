import datetime as dt

print("Insert a: ")
a = int(input())
print("Insert m: ")
m = int(input())
print("Insert n: ")
n = int(input())


print(a, m, n)

initial_dt = dt.datetime.now()

### insert code to be benchmarked here ###

ending_dt = dt.datetime.now()
res = ending_dt - initial_dt
print("The computation took " + res)
