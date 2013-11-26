from numpy cimport ndarray, float64_t
from numpy import zeros, float64, asfortranarray

cdef extern void perform(int * n, double * input, double * output)

def transform(double [:,:] inp, int n_exprs):
    cdef int n = inp.shape[0]
    cdef ndarray[float64_t, mode="fortran", ndim=2] inp_arr = \
        asfortranarray(inp)
    cdef ndarray[float64_t, mode="fortran", ndim=2] output = \
        zeros((n, n_exprs), order='F', dtype=float64)

    perform(&n, &inp_arr[0,0], &output[0,0])
    return output
