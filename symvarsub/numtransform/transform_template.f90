module transform
    use iso_c_binding, only: c_double, c_int
    implicit none

contains

    subroutine perform(n, input, output) bind(c)
        integer(c_int), intent(in) :: n
        real(c_double), intent(in), dimension(n, ${N_ARGS}) :: input
        real(c_double), intent(out), dimension(n, ${N_EXPRS}) :: output
        ! Declare common subexpressoin variables (CSE)
    %for cse_token, cse_expr in CSES:
        real(c_double), dimension(n) :: ${cse_token}
    %endfor

        ! Assign to CSEs
    %for cse_token, cse_expr in CSES:
        ${cse_token} = ${cse_expr}
    %endfor
    
        ! Assign to output
    %for i, expr_in_cse in enumerate(EXPRS_IN_CSE, 1):
        output(:, ${i}) = ${expr_in_cse}
    %endfor
    end subroutine
end module
