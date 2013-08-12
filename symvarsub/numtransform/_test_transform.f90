program main
use iso_c_binding, only: c_double
use transform, only: perform
implicit none

integer, parameter :: dp = c_double

integer, parameter :: n = 3
real(c_double), dimension(n,2) :: input
real(c_double), dimension(n,2) :: output
input(:,1) = [1.0_dp, 2.0_dp, 3.0_dp]
input(:,2) = [7.0_dp, 8.0_dp, 9.0_dp]
call perform(n, input, output)
print *, output
end program
