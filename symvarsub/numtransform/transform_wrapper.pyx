from numpy cimport ndarray
from numpy import zeros, float64, asfortranarray

cdef extern void perform(int * n, double * input, double * output)

def transform(double [:,:] inp, int n_exprs):
    cdef int n = inp.shape[0]
    cdef ndarray[double, mode="fortran", ndim=2] inp_arr = \
        asfortranarray(inp)
    cdef ndarray[double, mode="fortran", ndim=2] output = \
        zeros((n, n_exprs), order='F', dtype=float64)

    perform(&n, &inp_arr[0,0], &output[0,0])
    return output
