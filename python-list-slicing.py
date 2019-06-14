# -*- coding: utf-8 -*-
"""
An attempt to clarify Python slicing by writing Python code
that performs list slicing as it's done by the CPythong
implementation.

Please note the references in the code to methods in the
CPython.

@author: Glenn Bruns
"""

# return the result of slicing list x
# See the part of list_subscript() in listobject.c that pertains
# to when the indexing item is a PySliceObject
def slicer(x, start=None, stop=None, step=None):
    # Handle slicing index values of None, and a step value of 0.
    # See PySlice_Unpack() in sliceobject.c, which
    # extracts start, stop, step from a PySliceObject.
    maxint = 10000000  # hack to simulate PY_SSIZE_T_MAX
    if step == None:
        step = 1
    elif step == 0:
        raise ValueError('slice step cannot be zero')

    if start == None:
        start = maxint if step < 0 else 0
    if stop == None:
        stop = -maxint if step < 0 else maxint
          
    # Handle negative slice indexes and bad slice indexes.
    # Compute number of elements in the slice as slice_length.
    # See PySlice_AdjustIndices() in sliceobject.c
    length = len(x)
    slice_length = 0
    
    if start < 0:
        start += length
        if start < 0:
            start = -1 if step < 0 else 0
    elif start >= length:
        start = length - 1 if step < 0 else length
    
    if stop < 0:
        stop += length
        if stop < 0:
            stop = -1 if step < 0 else 0
    elif stop > length:
        stop = length - 1 if step < 0 else length
        
    if step < 0:
        if stop < start:
            slice_length = (start - stop - 1) // (-step) + 1
    else: 
        if start < stop:
            slice_length = (stop - start - 1) // step + 1
        
    # cases of step = 1 and step != 1 are treated separately
    if slice_length <= 0:
        return []
    elif step == 1:
        # see list_slice() in listobject.c
        result = []
        for i in range(stop - start):
            result.append(x[i+start])
        return result
    else:
        result = []
        cur = start
        for i in range(slice_length):
            result.append(x[cur])
            cur += step
        return result
    
#==============================================================================
# Testing code
#==============================================================================
            
import random

def comp_expr(x1, x2):
    print(x1)
    print(x2)

# some manual tests   
x = [4,6,2,4,9,5]
comp_expr(x[::], slicer(x))
comp_expr(x[1:3], slicer(x,start=1,stop=3))
comp_expr(x[5:1:-1], slicer(x,5,1,-1))
comp_expr(x[-7:-4:6], slicer(x,-7,-4,6))
comp_expr(x[10:7:-3], slicer(x,10,7,-3))
comp_expr(x[-8:10], slicer(x,start=-8,stop=10))

# run some automated tests
def rand_comp(num_tests=50):
    # generate a random list of random size
    m = random.randint(1,30)
    x = random.sample(range(1000), m)
    result = True
    n = len(x)+3
    for _ in range(num_tests):
        start = random.randint(-n,n) if random.random() < 0.3 else None
        stop  = random.randint(-n,n) if random.random() < 0.3 else None
        step  = random.randint(-n,n) if random.random() < 0.3 else None
        if step != 0:
            x1 = x[start:stop:step]
            x2 = slicer(x, start, stop, step)
            # print("x = {}".format(x))
            # print("x[{}:{}:{}] = {}".format(start, stop, step, x1))
            result = x1 == x2
        if not result:
            print("x = {}".format(x))
            print("x[{}:{}:{}] = {}".format(start, stop, step, x1))
            print("slicer(x, {}, {}, {}) = {}".format(start, stop, step, x2))
            print("Lists not equal!")
            break
    print("success" if result else "failure")

# check a bunch of random slices
rand_comp(100000)


