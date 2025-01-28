import numpy as np
from typing import Callable, Union


def hello_world():
    return "hello world"


def midpoint(a: float, b: float) -> float:
    """
    Given points a and b. Will return midpoint c.
    """
    c = (a + b) / 2.0
    return c


def check_a_less_b(a: float, b: float):
    """
    Given points a and b.
    Will throw an error if a > b.
    """
    if a >= b:
        raise ValueError(f"Invalid input: {a} is greater than {b}.")
    return True


def check_max_iter(num_iter: int, max_iter: int):
    """
    Given number of iterations and maximum number of iterations.
    Will throw an error if the number of iterations > maximum.
    """
    if num_iter > max_iter:
        raise ValueError(f"Maximum number of iterations ({max_iter}) reached without convergence")
    return


def check_sign_compatible(a: float, b: float, fcn_a: float, fcn_b: float):
    """
    Given point a and b and a function evaluation of point a and b.
    Will return true if fcn(a) > 0 and fcn(b) < 0.
    Will return true if fcan(a) < 0 and fcn(b) > 0.
    Will return false otherwise.
    """
    if fcn_a > 0 and fcn_b < 0:
        return
    elif fcn_a < 0 and fcn_b > 0:
        return
    else:
        raise ValueError("a and b are not guaranteed to contain a root of the continous function provided")
    return


def update_a_b(a: float, b: float, c: float, fcn_a: float, fcn_b: float, fcn_c: float) -> Union[float, float, float, float]:
    """
    Given endpoints a and b and midpoint c and function evaluations of each.
    Will update a and b according to c to keep one evaluation of fcn positive and one negative.
    If fcn_a, fcn_b, or fcn_c are exactly zero, a and b will both be assigned to the corresponding input.
    """
    if np.sign(fcn_a) == np.sign(fcn_b):
        raise ValueError("The function evaluations must have one positive and one negative value.")
    if fcn_c == 0:
        return c, c, fcn_c, fcn_c
    if fcn_a == 0:
        return a, a, fcn_a, fcn_a
    if fcn_b == 0:
        return b, b, fcn_b, fcn_b
    if np.sign(fcn_a) == np.sign(fcn_c):
        return c, b, fcn_c, fcn_b
    elif np.sign(fcn_b) == np.sign(fcn_c):
        return a, c, fcn_a, fcn_c


def root_found(a: float, b: float, fcn_a: float, fcn_b: float, tol_input: float, tol_output: float) -> bool:
    """
    Given endpoints a and b and the desired tolerance.
    Will return "True" if the root is found.
    Will return "False" otherwise.
    """
    val_input = np.abs(a - b)
    val_output = np.mean(np.abs(fcn_a) + np.abs(fcn_b))
    if val_input < tol_input or val_output < tol_output:
        return True
    else:
        return False


def update_step(fcn: Callable, a: float, b: float, fcn_a: float, fcn_b: float) -> Union[float, float, float, float]:
    """
    Given a continuous function, bounds a and b, and function values at a and b.
    Will compute the midpoint c and perform the update to a and b according to the bisection method.
    Will return new values of a, b, fcn_a and fcn_b.
    """
    c = midpoint(a, b)
    fcn_c = fcn(c)
    a, b, fcn_a, fcn_b = update_a_b(a, b, c, fcn_a, fcn_b, fcn_c)
    return a, b, fcn_a, fcn_b


def run_bisection_method(fcn: Callable, a: float, b: float, tol_input: float = 10 ** -9, tol_output: float = 10 ** -30, max_num_iter: int = 1000) -> dict:
    """
    """
    check_a_less_b(a, b)
    fcn_a = fcn(a)
    fcn_b = fcn(b)
    check_sign_compatible(a, b, fcn_a, fcn_b)
    num_iter = 0
    a_list = []
    b_list = []
    fcn_a_list = []
    fcn_b_list = []
    while root_found(a, b, fcn_a, fcn_b, tol_input, tol_output) is False:
        check_max_iter(num_iter, max_num_iter)
        num_iter += 1
        a, b, fcn_a, fcn_b = update_step(fcn, a, b, fcn_a, fcn_b)
        a_list.append(a)
        b_list.append(b)
        fcn_a_list.append(fcn_a)
        fcn_b_list.append(fcn_b)
    final_root = midpoint(a, b)
    result = {"solution": final_root,
              "num_iter": num_iter,
              "all_a": a_list,
              "all_fcn_a": fcn_a_list,
              "all_b": b_list,
              "all_fcn_b": fcn_b_list}
    return result

