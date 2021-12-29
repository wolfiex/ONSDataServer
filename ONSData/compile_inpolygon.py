'''
Compiles the numba JIT
Normal usage relies on the @jit tag and the fn. 

In order to compile with nopython=True, each var needs to be declared before the for loop

pre-compiling the code will not enable the parallel capabilities of numba (parallel CPU target is not supported by pycc/AOT compilation) see: https://github.com/numba/numba/issues/3336

[Parallel segments commented out]
[Parallel segments uncommented out - profiling favours the compiled version]


'''

import numba
import numpy as np
from numba import jit, njit
from numba.pycc import CC
cc = CC('inpolygon')



@cc.export('ray_tracing',  'b1(i2, i2, f8[:,:])')
@jit(nopython=True)
def ray_tracing(x,y,poly):
    n = len(poly)
    inside = False
    p2x = 0.0
    p2y = 0.0
    xints = 0.0
    p1x,p1y = poly[0]
    # for i in numba.prange(n+1):
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside


# @njit(parallel=True)
# def parallelpointinpolygon(points, polygon):
#     D = np.empty(len(points), dtype=numba.boolean) 
#     for i in numba.prange(0, len(D)):
#         D[i] = pointinpolygon(points[i,0], points[i,1], polygon)
#     return D    


if __name__ == "__main__":
    cc.compile()