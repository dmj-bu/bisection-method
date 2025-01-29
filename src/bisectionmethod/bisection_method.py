import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Callable, Union


def hello_world():
    return "hello world!"


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
    a_list.append(a)
    b_list.append(b)
    fcn_a_list.append(fcn_a)
    fcn_b_list.append(fcn_b)
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


def plot_bisection_results(result: dict, fig_name_with_path: Path):
    """
    Plots the results of the bisection method.
    
    Parameters:
        result (dict): Output dictionary from the `run_bisection_method` function, containing:
            - "all_a": List of all intermediate a values
            - "all_b": List of all intermediate b values
            - "num_iter": Number of iterations
    """
    a_values = result["all_a"]
    b_values = result["all_b"]
    num_iter = result["num_iter"]
    final_root = result["solution"]

    # Compute midpoint values for visualization
    midpoints = [(a + b) / 2.0 for a, b in zip(a_values, b_values)]
    
    # Compute interval sizes
    interval_sizes = [b - a for a, b in zip(a_values, b_values)]
    
    # Plot a and b values over iterations
    fig, axs = plt.subplots(1, 2, figsize=(9, 4))
    axs[0].plot(range(0, num_iter + 1), a_values, marker="o", color="red", label="a values", linestyle="--")
    axs[0].plot(range(0, num_iter + 1), b_values, marker="s", color="blue", label="b values", linestyle="--")
    axs[0].plot(range(0, num_iter + 1), midpoints, marker=".", color="cyan", label="Midpoints", linestyle="-")
    axs[0].scatter([num_iter], [final_root], color="yellow", label="Root: %0.6f" % (final_root), s=200, edgecolors="black")
    axs[0].set_xlabel("Iteration")
    axs[0].set_ylabel("Value")
    axs[0].set_title("Convergence of a, b, and Midpoints")
    axs[0].legend()
    axs[0].grid(True)
    
    # Plot interval sizes over iterations
    axs[1].plot(range(0, num_iter + 1), interval_sizes, marker="o", color="black", linestyle="-")
    axs[1].set_yscale("log")
    axs[1].set_xlabel("Iteration")
    axs[1].set_ylabel("Interval Size (log scale)")
    axs[1].set_title("Convergence of Interval Size")
    axs[1].grid(True)

    plt.tight_layout()
    plt.savefig(fig_name_with_path)
    return


def plot_function_with_inset(fcn, result: dict, fig_name_with_path: Path):
    """
    Plots the original function and visualizes the evolution of `a` and `b` 
    with an inset plot zoomed in around the root.

    Parameters:
        fcn (callable): The function being solved using the bisection method.
        a_values (list): List of `a` values from the iterations.
        b_values (list): List of `b` values from the iterations.
        result (dict): Output dictionary from `run_bisection_method` containing:
            - "solution": The computed root.
    """
    # Extract the root and define a range around it for better visualization
    root = result["solution"]
    a_values = result["all_a"]
    b_values = result["all_b"]
    x_range = np.linspace(min(a_values) - 1, max(b_values) + 1, 1000)
    y_values = [fcn(x) for x in x_range]
    
    # Main plot: Original function
    plt.figure(figsize=(6, 4))
    plt.plot(x_range, y_values, label="f(x)", color="black")
    plt.axhline(0, color="black", linestyle="--", linewidth=0.8)  # Horizontal line at y=0
    plt.scatter(a_values, [fcn(a) for a in a_values], marker="o", color="red", label="a values", zorder=5)
    plt.scatter(b_values, [fcn(b) for b in b_values], marker="s", color="blue", label="b values", zorder=5)
    plt.scatter([root], [fcn(root)], color="yellow", label="Root", zorder=10, s=100, edgecolors="black")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Function Plot with Iterations of a and b")
    plt.legend()
    plt.grid(True)
    
    # Inset plot: Zoomed-in view around the root
    ax_inset = plt.gca().inset_axes([0.6, 0.6, 0.3, 0.3])  # Define inset position and size
    zoom_range = np.linspace(root - 0.5, root + 0.5, 500)
    zoom_y_values = [fcn(x) for x in zoom_range]
    ax_inset.plot(zoom_range, zoom_y_values, color="black")
    ax_inset.scatter(a_values, [fcn(a) for a in a_values], marker="o", color="red", s=10)
    ax_inset.scatter(b_values, [fcn(b) for b in b_values], marker="s", color="blue", s=10)
    ax_inset.scatter([root], [fcn(root)], color="yellow", s=50, edgecolors="black")
    ax_inset.axhline(0, color="black", linestyle="--", linewidth=0.8)
    ax_inset.set_xlim(root - 0.1, root + 0.1)
    ax_inset.set_ylim(-0.1, 0.1)
    ax_inset.set_title("Zoomed-in View of Root")
    ax_inset.grid(True)
    
    plt.tight_layout()
    plt.savefig(fig_name_with_path)
    return
