import random
from sys import argv
import math
import itertools
from mip import *

#from random import seed
#from random import randint
fil = open("output1.txt", "w")
count = 0 # global variable to count number of counterexamples
n = 4
t = 4
m = n**t

block = [ [i] for i in range(n) ]
block_s = [ str(i) for i in range(n) ]
monom = block
monom_s = block_s
for j in range(t-1):
    monom = [ a+b for a in monom for b in block ]
    monom_s = [ a+','+b for a in monom_s for b in block_s ]
#print(monom)
#print(monom_s)

def is_func(f, n, t): # is this function a counterexample, needs input in block multilinear representation
    M = Model()
    fil.write("Number of blocks: {}\n".format(str(t)))
    x = []
    y = []
    z = []
    for i in range(t):
        x.append( [M.add_var(name = "x_"+str(j)+"_"+str(i), var_type = BINARY) for j in range(n)] )
    for S in range(m):
        y.append( M.add_var(name = "y_"+monom_s[S], var_type = BINARY) ) # This will store the value of monomials
        z.append( M.add_var(name = "z_"+monom_s[S], var_type = INTEGER) )
        
        M += (y[S] + 2*z[S] == xsum(x[j][monom[S][j]] for j in range(t))) # Adding Constraints of the ILP

    M.objective = xsum( (1/math.sqrt(m)) * f[S] * (1-2*y[S]) for S in range(m) )
    status = M.optimize(max_seconds = 10000)
    if status == OptimizationStatus.OPTIMAL:
        fil.write('Optimal value is {}\n'.format(str(M.objective_value)))
        if M.objective_value < -1-1e-5:
            fil.write('Counter example found with {} as its minimum value\n'.format(M.objective_value))
            for v in M.vars:
                fil.write('{} : {}\n'.format(v.name, v.x))
            exit()

f = [1]*(m//2) + [-1]*(m - m//2)
random.shuffle(f)
#print(f)
fil.write("Polynomial:{}\n".format(str(f)))
is_func(f, n, t)
