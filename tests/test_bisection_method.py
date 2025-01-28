from bisectionmethod import bisection_method as bim
import numpy as np
from pathlib import Path
import pytest
import re


def test_hello_world():
    known = "hello world"
    found = bim.hello_world()
    assert known == found


def test_midpoint():
    a = 10.0
    b = 20.0
    found = bim.midpoint(a, b)
    known = 15.0
    assert np.isclose(known, found)


def test_check_a_less_b():
    try:
        a = 3
        b = 7
        bim.check_a_less_b(a, b)
    except ValueError:
        pytest.fail("Unexpected ValueError raised for a <= b.")
    a = 10
    b = 5
    with pytest.raises(ValueError, match=f"Invalid input: {a} is greater than {b}\."):
        bim.check_a_less_b(a, b)
    with pytest.raises(ValueError) as excinfo:
        a = 12
        b = 8
        bim.check_a_less_b(a, b)
    assert str(excinfo.value) == "Invalid input: %i is greater than %i." % (a, b)


def test_check_max_iter():
    try:
        num_iter = 100
        max_iter = 1000
        bim.check_max_iter(num_iter, max_iter)
    except ValueError:
        pytest.fail("Unexpected ValueError raised for num_iter <= max_iter.")
    num_iter = 1001
    max_iter = 1000
    with pytest.raises(ValueError, match=re.escape(f"Maximum number of iterations ({max_iter}) reached without convergence")):
        bim.check_max_iter(num_iter, max_iter)
    with pytest.raises(ValueError) as excinfo:
        num_iter = 11
        max_iter = 10
        bim.check_max_iter(num_iter, max_iter)
    assert str(excinfo.value) == "Maximum number of iterations (%i) reached without convergence" % (max_iter)


def test_check_sign_compatible():
    try:
        a = 1
        b = 10
        fcn_a = -5
        fcn_b = 10
        bim.check_sign_compatible(a, b, fcn_a, fcn_b)
        a = 1
        b = 10
        fcn_a = 100
        fcn_b = -40
        bim.check_sign_compatible(a, b, fcn_a, fcn_b)
    except ValueError:
        pytest.fail("Unexpected ValueError raised for checking if the bounds contain a root")
    a = 4
    b = 17
    fcn_a = 1
    fcn_b = 100
    with pytest.raises(ValueError, match="a and b are not guaranteed to contain a root of the continous function provided"):
        bim.check_sign_compatible(a, b, fcn_a, fcn_b)
    a = -5
    b = 0
    fcn_a = -100
    fcn_b = -1000
    with pytest.raises(ValueError, match="a and b are not guaranteed to contain a root of the continous function provided"):
        bim.check_sign_compatible(a, b, fcn_a, fcn_b)


def test_update_a_b():
    # Case 1: fcn_a and fcn_c have the same sign
    a, b, fcn_a, fcn_b = bim.update_a_b(1.0, 2.0, 1.5, -0.5, 0.5, -0.2)
    assert a == 1.5
    assert b == 2.0
    assert fcn_a == -0.2
    assert fcn_b == 0.5

    # Case 2: fcn_b and fcn_c have the same sign
    a, b, fcn_a, fcn_b = bim.update_a_b(1.0, 2.0, 1.5, -0.5, 0.5, 0.2)
    assert a == 1.0
    assert b == 1.5
    assert fcn_a == -0.5
    assert fcn_b == 0.2

    # Test cases where the function evaluations do not have opposite signs
    with pytest.raises(ValueError, match="The function evaluations must have one positive and one negative value."):
        bim.update_a_b(1.0, 2.0, 1.5, 0.5, 0.5, 0.2)  # All values are positive

    with pytest.raises(ValueError, match="The function evaluations must have one positive and one negative value."):
        bim.update_a_b(1.0, 2.0, 1.5, -0.5, -0.5, -0.2)  # All values are negative
    
    # Test edge cases, such as zero crossings
    # Case 1: fcn_a is 0, update should still work
    a, b, fcn_a, fcn_b = bim.update_a_b(1.0, 2.0, 1.5, 0.0, 0.5, -0.2)
    assert a == 1.0
    assert b == 1.0
    assert fcn_a == 0
    assert fcn_b == 0

    # Case 2: fcn_b is 0, update should still work
    a, b, fcn_a, fcn_b = bim.update_a_b(1.0, 2.0, 1.5, -0.5, 0.0, 0.2)
    assert a == 2.0
    assert b == 2.0
    assert fcn_a == 0
    assert fcn_b == 0

    # Case 3: fcn_c is 0, update should still work
    a, b, fcn_a, fcn_b = bim.update_a_b(1.0, 2.0, 1.5, -0.5, 0.5, 0.0)
    assert a == 1.5
    assert b == 1.5
    assert fcn_a == 0
    assert fcn_b == 0


def test_root_found():
    # Input tolerance satisfied
    assert bim.root_found(1.0, 1.0 + 1e-10, -0.5, 0.5, tol_input=1e-9, tol_output=1e-9) == True

    # Output tolerance satisfied
    assert bim.root_found(1.0, 2.0, 1e-10, 1e-10, tol_input=1e-9, tol_output=1e-9) == True

    # Both tolerances satisfied
    assert bim.root_found(1.0, 1.0 + 1e-10, 0.0, 1e-10, tol_input=1e-9, tol_output=1e-9) == True

    # Neither tolerance satisfied
    assert bim.root_found(1.0, 2.0, -0.5, 0.5, tol_input=1e-9, tol_output=1e-9) == False
    assert bim.root_found(1.0, 1.1, -1.0, 1.0, tol_input=1e-2, tol_output=1e-2) == False

    # Edge case: Zero values
    assert bim.root_found(0.0, 0.0, 0.0, 0.0, tol_input=1e-9, tol_output=1e-9) == True


# Define a simple continuous function
def fcn(x):
    return x**2 - 2  # Root is at sqrt(2) ~ 1.414


def test_update_step():
    # Example 1
    a, b, fcn_a, fcn_b = -1.0, 2.0, fcn(-1.0), fcn(2.0)
    new_a, new_b, new_fcn_a, new_fcn_b = bim.update_step(fcn, a, b, fcn_a, fcn_b)
    assert np.isclose(new_a, bim.midpoint(a, b))
    assert np.isclose(new_b, b)
    assert np.isclose(new_fcn_a, fcn(bim.midpoint(a, b)))
    assert np.isclose(new_fcn_b, fcn_b)

    # Example 2
    a, b, fcn_a, fcn_b = 1.0, 2.0, fcn(1.0), fcn(2.0)
    new_a, new_b, new_fcn_a, new_fcn_b = bim.update_step(fcn, a, b, fcn_a, fcn_b)
    assert np.isclose(new_a, a)
    assert np.isclose(new_b, bim.midpoint(1.0, 2.0))
    assert np.isclose(new_fcn_a, fcn_a)
    assert np.isclose(new_fcn_b, fcn(bim.midpoint(a, b)))


def fcn_2(x):
    return (x - 10.75) ** 3.0


def fcn_3(x):
    return x


def test_run_bisection_method():
    # examples that do converge
    result = bim.run_bisection_method(fcn, 0.0, 10.0, 10 ** -10, 10 ** -20)
    assert np.isclose(result["solution"], np.sqrt(2))
    assert len(result["all_a"]) == result["num_iter"]
    assert len(result["all_fcn_a"]) == result["num_iter"]
    assert len(result["all_b"]) == result["num_iter"]
    assert len(result["all_fcn_b"]) == result["num_iter"]
    tol_input = 10 ** -10
    tol_output = 10 ** -30
    result = bim.run_bisection_method(fcn_2, 0.0, 20.0, tol_input, tol_output)
    assert np.isclose(result["solution"], 10.75, 10 ** -9)
    # examples that give errors
    a = 5.0
    b = 10.0
    with pytest.raises(ValueError, match="a and b are not guaranteed to contain a root of the continous function provided"):
        bim.run_bisection_method(fcn_3, a, b)
    a = 10
    b = -3
    with pytest.raises(ValueError, match=f"Invalid input: {a} is greater than {b}\."):
        bim.run_bisection_method(fcn_3, a, b)
    tol_input = 10 ** -10
    tol_output = 10 ** -30
    max_num_iter = 10
    with pytest.raises(ValueError, match=re.escape(f"Maximum number of iterations ({max_num_iter}) reached without convergence")):
        bim.run_bisection_method(fcn_2, 0.0, 20.0, tol_input, tol_output, max_num_iter)


def test_plot_function_with_inset():
    result = bim.run_bisection_method(fcn, 0.0, 10.0, 10 ** -10, 10 ** -20)
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("files").resolve()
    fig_name_with_path = data_path.joinpath("test_plot_funciton_with_inset.png").resolve()
    bim.plot_function_with_inset(fcn, result, fig_name_with_path)
    assert fig_name_with_path.is_file()


def test_plot_bisection_results():
    result = bim.run_bisection_method(fcn, 0.0, 10.0, 10 ** -10, 10 ** -20)
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("files").resolve()
    fig_name_with_path = data_path.joinpath("test_plot_bisection_results.png").resolve()
    bim.plot_bisection_results(result, fig_name_with_path)
    assert fig_name_with_path.is_file()
