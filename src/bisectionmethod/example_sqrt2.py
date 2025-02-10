from bisectionmethod import bisection_method as bim
  # Adjust import based on directory structure
import os
from pathlib import Path

# Define the function
def f(x):
    return x**2 - 2  # Root is at sqrt(2)

# Define the bounds
a = 1.0  # Lower bound
b = 2.0  # Upper bound

# Call the bisection method
result = bim.run_bisection_method(fcn=f, a=a, b=b, tol_input=1e-9, tol_output=1e-30)

# Print the result
print("Root:", result["solution"])
print("Number of iterations:", result["num_iter"])

# Create a directory for figures if it doesn't exist
figs_path = Path(os.getcwd()).joinpath("figs")
figs_path.mkdir(parents=True, exist_ok=True)

# Plot the results
fig_name_with_path = figs_path.joinpath("tutorial_1_bisection_results.png")
bim.plot_bisection_results(result, fig_name_with_path)

fig_name_with_path = figs_path.joinpath("tutorial_1_function_vis.png")
bim.plot_function_with_inset(f, result, fig_name_with_path)
