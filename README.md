# Bisection Method

### Table of Contents
* [Conda environemnt, installation, and testing](#install)
* [Bisection method algorithm](#algo)
* [Tutorial](#tutorial)
* [More Information](#more)

### Conda environment, install, and testing <a name="install"></a>

```bash
conda create --name bisection-method-env python=3.12
```

```bash
conda activate bisection-method-env
```

```bash
python --version
```

```bash
pip install --upgrade pip setuptools wheel
```

```bash
pip install -e .
```

```bash
pytest -v --cov=bisectionmethod --cov-report term-missing
```

don't forget to set VSCode virtual environment

### Bisection Method Algorithm <a name="algo"></a>

The **Bisection Method** is a numerical technique to find roots of a continuous function \( f(x) \). The method works by repeatedly dividing an interval \([a, b]\) in half and selecting the subinterval in which the root lies. The algorithm for the Bisection Method is as follows:

1. **Choose an interval \([a, b]\)**:
   - \( f(a) \cdot f(b) < 0 \), which means the function has a root in the interval.
2. **Compute the midpoint**:
   \[
   c = \frac{a + b}{2}
   \]
3. **Check the sign of \( f(c) \)**:
   - If \( f(c) = 0 \), then \( c \) is the root.
   - If \( f(a) \cdot f(c) < 0 \), the root lies in \([a, c]\). Update \( b = c \).
   - Otherwise, the root lies in \([c, b]\). Update \( a = c \).
4. **Repeat** until the interval size \(|b - a|\) is smaller than the desired tolerance.

**Advantages of the Bisection Method**:
1. **Simplicity**: The method is easy to understand and implement.
2. **Guaranteed Convergence**: If the function \( f(x) \) is continuous and \( f(a) \cdot f(b) < 0 \), the method is guaranteed to converge to a root.
3. **Robustness**: It works well for a wide range of functions without requiring derivatives or complex calculations.
4. **Predictable Behavior**: The error decreases by approximately half in each iteration, providing predictable convergence.

**Limitations of the Bisection Method**:
1. **Slow Convergence**: Compared to other methods like Newton-Raphson or secant, the bisection method can converge more slowly.
2. **Requires Bracketing**: The method requires an interval \([a, b]\) where \( f(a) \cdot f(b) < 0 \), which may not always be easy to identify.
3. **Limited Precision**: The method converges linearly, which may not be efficient for high-precision requirements.
4. **Not Suitable for Multiple Roots**: The method may fail or behave inconsistently if the function has multiple roots within the interval.
5. **Function Continuity Required**: It assumes \( f(x) \) is continuous in \([a, b]\), and any discontinuities can cause issues.

### Tutorial <a name="tutorial"></a>


### More information <a name="more"></a>
