"""Analytical illustration, not an SFCL performance benchmark."""
import math


def relative_jump_loss(z):
    if z <= -1:
        raise ValueError("Relative jump must exceed -1")
    return 1 + z / 2 - math.sqrt(1 + z)


if __name__ == "__main__":
    print("Relative jump | exact loss / V | quadratic approximation")
    for jump in (-0.75, -0.5, 0.1, 1.0, 3.0):
        print(f"{jump:+.2f} | {relative_jump_loss(jump):.8f} | {jump * jump / 8:.8f}")
