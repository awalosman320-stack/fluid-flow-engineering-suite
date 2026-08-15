"""Independent engineering verification functions."""

import math


def colebrook_friction_factor(
    reynolds_number,
    roughness,
    diameter,
    tolerance=1e-10,
    max_iterations=100
):
    """
    Solve the Colebrook-White equation iteratively.

    Parameters
    ----------
    reynolds_number : float
        Reynolds number of the flow.
    roughness : float
        Absolute pipe roughness in metres.
    diameter : float
        Internal pipe diameter in metres.
    tolerance : float, optional
        Convergence tolerance for the iterative solution.
    max_iterations : int, optional
        Maximum number of iterations.

    Returns
    -------
    float
        Darcy friction factor obtained from the
        Colebrook-White equation.

    Raises
    ------
    ValueError
        If the input values are physically invalid.
    RuntimeError
        If the iterative solution does not converge.
    """
    if reynolds_number <= 4000:
        raise ValueError(
            "Colebrook verification is intended for turbulent flow "
            "(Re > 4000)."
        )

    if roughness < 0:
        raise ValueError("Roughness cannot be negative.")

    if diameter <= 0:
        raise ValueError("Diameter must be greater than zero.")

    if tolerance <= 0:
        raise ValueError("Tolerance must be greater than zero.")

    if max_iterations <= 0:
        raise ValueError("Maximum iterations must be positive.")

    relative_roughness = roughness / diameter

    # Initial estimate.
    friction_factor = 0.02

    for _ in range(max_iterations):
        previous_factor = friction_factor

        friction_factor = 1 / (
            -2
            * math.log10(
                relative_roughness / 3.7
                + 2.51
                / (
                    reynolds_number
                    * math.sqrt(previous_factor)
                )
            )
        ) ** 2

        if abs(friction_factor - previous_factor) < tolerance:
            return friction_factor

    raise RuntimeError(
        "Colebrook calculation did not converge "
        "within the maximum number of iterations."
    )


def compare_friction_factors(
    calculated_factor,
    verified_factor
):
    """
    Compare two friction-factor calculations.

    Parameters
    ----------
    calculated_factor : float
        Friction factor from the main calculation.
    verified_factor : float
        Independently verified friction factor.

    Returns
    -------
    dict
        Absolute difference and percentage difference.
    """
    if calculated_factor <= 0:
        raise ValueError(
            "Calculated friction factor must be greater than zero."
        )

    if verified_factor <= 0:
        raise ValueError(
            "Verified friction factor must be greater than zero."
        )

    absolute_difference = abs(
        calculated_factor - verified_factor
    )

    percentage_difference = (
        absolute_difference
        / verified_factor
        * 100
    )

    return {
        "absolute_difference": absolute_difference,
        "percentage_difference": percentage_difference,
    }