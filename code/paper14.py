from sys import argv
import math
import itertools
from mip import *


def is_func(func):        # is this function a counterexample, needs input in block multilinear representation
    m=Model()
    global t
    print("t: "+str(t))
    permutations_t=list(itertools.permutations(list(range(t))))
    print("permutation")
    print(permutations_t)
    x_b=[]
    x_ext=[]
    x_sum=[]
    t_fact=math.factorial(t)
    for x in range(n+1):
        x_b.append( [m.add_var(name="x_b_"+str(x)+"_"+str(i),var_type=BINARY) for i in range(t)] )
    for x in range(size_tt):
        x_ext.append([m.add_var(name="x_ext_"+str(x)+"_"+str(i),var_type=BINARY) for i in range(t_fact)])
        x_sum.append([m.add_var(name="x_sum_"+str(x)+"_"+str(i),var_type=INTEGER) for i in range(t_fact)])
        vars=[]
        temp=x
        cnt=0
        for i in range(n):
            if 1&temp==1:
                vars.append(i+1)
                cnt+=1
            temp//=2
        vars+=[0]*(t-cnt)
        for y in range(t_fact):
            m+=(x_ext[x][y]+2*x_sum[x][y]==xsum(x_b[vars[z]][permutations_t[y][z]] for z in range(t)))

    m.objective=xsum( func[x][y]*(1-2*x_ext[x][y]) for x in range(size_tt) for y in range(t_fact) )
    status = m.optimize(max_seconds=500)
    if status == OptimizationStatus.OPTIMAL:
        print('Optimal value is'+str(m.objective_value))
        if m.objective_value<-1-1e-5:
            print('Counter eample found with {} as its minimum value'.format(m.objective_value))
            for k in x_ext:
                # if abs(v.x) > 1e-6: # only printing non-zeros
                for v in k:
                    print('{} : {}'.format(v.name, v.x))
            print(func)
            exit()
            # exit()
