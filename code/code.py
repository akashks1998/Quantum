# The following program checks if a functions symmetric block multilinear representation can be not bounded by 1.
# We check this over all functions on n variables
# A function is a counterexample if its block multilinear rep is not bounded

from sys import argv
#from random import seed
#from random import randint

n = 2  # number of variables
size_tt = 2**n  # size of the truth table of f
t = 2 # degree of the polynomials
n_bm = t * (n + 1)

def binary(l,dig): #binary representation of l (0 replaced with -1) with dig number of digits   
    rep = []
    m=int(l)
    for i in range(0,dig):
        k = m%2
        #print(m,k)
        if (k == 0):
            rep.append(-1)
        else:
            rep.append(1)
        m = int(m / 2)
    return rep

#print(binary(63))

def is_func(func):        # is this function a counterexample, needs input in block multilinear representation
    flag = 0
    for i in range(0,2**(n_bm)):
        x_b = binary(i,n_bm)  # \bar{x}
        # print(reps)
        x_ext = [(x_b[0] * x_b[3]), (x_b[0] * x_b[4]), (x_b[1] * x_b[3]), (x_b[0] * x_b[5]),(x_b[2] * x_b[3]), (x_b[1] * x_b[5]), (x_b[2] * x_b[4])]
        #print(x,x_ext)
        val = 0
        for j in range(0,7):
            val = val + x_ext[j] * func[j]
        #print("value= ", val)
        if ((val > 1) or (val < -1)):
            print("GOT A COUNTEREXAMPLE", "x_b= ", x_b,  "f=", func, "f(x)= ", val, "\n\n")
            flag = 1
            break
    if (flag == 0 ):
        print("This function is NOT a counterexample ", func)

def chi(i,j):  # Calculates \chi_i(j) , where i should be viewed as a set (-1 means index not present) and j should be viewed as an assignment.
    value = 1
    bin_j = binary(j,n)
    bin_i = binary(i,n)
    for k in range(0,n):
        if (bin_i[k] == 1):
            value = value * bin_j[k]
    #print(value, bin_i, bin_j)
    return value


def poly(func_tt):   # give the block multilinear rep of f from its truth table representation, the first entry of truth table is -1,-1,..., -1
    func_poly = [0] * size_tt
    for i in range(0,size_tt):
        func_poly[i] = 0
        for j in range(0,size_tt):
            func_poly[i] = func_poly[i] + func_tt[j] * chi(i,j)
        func_poly[i] = (1.0 / size_tt) * func_poly[i]   # ith Fourier coefficient
    print("the poly rep is ", func_poly)
    h = 0.5
    func_bm = [func_poly[0], h * func_poly[1], h * func_poly[1], h * func_poly[2], h * func_poly[2], h * func_poly[3], h * func_poly[3]]
    return func_bm


for i in range(0,2**(size_tt)):
    f_tt = binary(i, size_tt)
    print("The truth table of the function is ", f_tt)
    f_bm = poly(f_tt)
    #print("Its bm poly representation is ", f_bm)
    is_func(f_bm)




