
import math

def ntc_to_temperature(R_ntc_kohm, a=26.732, b=-0.033):
    """Exponential conversion (not used in StreamViewer by default)."""
    return math.log(R_ntc_kohm / a) / b

def resistance_to_celsius_poly(x):
    """Polynomial formula used by StreamViewer."""
    return (
        -7e-16 * x**6 +
        3e-12 * x**5 +
        -6e-9 * x**4 +
        6e-6 * x**3 +
        -0.0029 * x**2 +
        0.8 * x +
        -12.959
    )

# Quick test
if __name__ == "__main__":
    for r in [10, 52, 100, 270]:
        print(f"R = {r} kΩ → {resistance_to_celsius_poly(r):.2f} °C")













