"""Heat-transfer engineering calculations.

This module contains analytical calculations for:
1. Steady-state conduction through a flat wall.
2. Newton's Law of Cooling.
"""

import math


def calculate_conduction_heat_rate(
    thermal_conductivity,
    area,
    thickness,
    temperature_hot,
    temperature_cold,
):
    """
    Calculate steady-state heat-transfer rate through a flat wall.

    Fourier's law for one-dimensional steady conduction is:

        Q = k A (Th - Tc) / L

    Parameters
    ----------
    thermal_conductivity : float
        Material thermal conductivity in W/(m.K).
    area : float
        Wall area in m².
    thickness : float
        Wall thickness in m.
    temperature_hot : float
        Temperature of the hot surface in °C.
    temperature_cold : float
        Temperature of the cold surface in °C.

    Returns
    -------
    float
        Heat-transfer rate in watts.
    """
    if thermal_conductivity <= 0:
        raise ValueError(
            "Thermal conductivity must be greater than zero."
        )

    if area <= 0:
        raise ValueError(
            "Wall area must be greater than zero."
        )

    if thickness <= 0:
        raise ValueError(
            "Wall thickness must be greater than zero."
        )

    temperature_difference = (
        temperature_hot - temperature_cold
    )

    return (
        thermal_conductivity
        * area
        * temperature_difference
        / thickness
    )


def calculate_cooling_time(
    initial_temperature,
    target_temperature,
    ambient_temperature,
    heat_transfer_coefficient,
    area,
    mass,
    specific_heat,
):
    """
    Calculate cooling time using Newton's Law of Cooling.

    The lumped-capacitance model is:

        T(t) = T_inf + (T0 - T_inf)
               exp[-h A t / (m cp)]

    Rearranging gives:

        t = -(m cp / h A)
            ln[(Ttarget - T_inf)/(T0 - T_inf)]

    Parameters
    ----------
    initial_temperature : float
        Initial object temperature in °C.
    target_temperature : float
        Desired final temperature in °C.
    ambient_temperature : float
        Surrounding fluid temperature in °C.
    heat_transfer_coefficient : float
        Convective heat-transfer coefficient in W/(m².K).
    area : float
        Exposed surface area in m².
    mass : float
        Object mass in kg.
    specific_heat : float
        Specific heat capacity in J/(kg.K).

    Returns
    -------
    float
        Cooling time in seconds.
    """
    if heat_transfer_coefficient <= 0:
        raise ValueError(
            "Heat-transfer coefficient must be greater than zero."
        )

    if area <= 0:
        raise ValueError(
            "Surface area must be greater than zero."
        )

    if mass <= 0:
        raise ValueError(
            "Mass must be greater than zero."
        )

    if specific_heat <= 0:
        raise ValueError(
            "Specific heat must be greater than zero."
        )

    if initial_temperature == ambient_temperature:
        raise ValueError(
            "Initial temperature cannot equal ambient temperature."
        )

    numerator = target_temperature - ambient_temperature
    denominator = initial_temperature - ambient_temperature

    ratio = numerator / denominator

    if ratio <= 0 or ratio >= 1:
        raise ValueError(
            "Target temperature must lie between the initial "
            "and ambient temperatures."
        )

    time_seconds = (
        -(mass * specific_heat)
        / (heat_transfer_coefficient * area)
        * math.log(ratio)
    )

    return time_seconds


def cooling_temperature(
    time,
    initial_temperature,
    ambient_temperature,
    heat_transfer_coefficient,
    area,
    mass,
    specific_heat,
):
    """
    Calculate object temperature at a specified time.

    Parameters
    ----------
    time : float
        Time in seconds.
    initial_temperature : float
        Initial object temperature in °C.
    ambient_temperature : float
        Surrounding temperature in °C.
    heat_transfer_coefficient : float
        Convective heat-transfer coefficient in W/(m².K).
    area : float
        Exposed surface area in m².
    mass : float
        Object mass in kg.
    specific_heat : float
        Specific heat capacity in J/(kg.K).

    Returns
    -------
    float
        Object temperature in °C.
    """
    if time < 0:
        raise ValueError("Time cannot be negative.")

    if heat_transfer_coefficient <= 0:
        raise ValueError(
            "Heat-transfer coefficient must be greater than zero."
        )

    if area <= 0:
        raise ValueError(
            "Surface area must be greater than zero."
        )

    if mass <= 0:
        raise ValueError(
            "Mass must be greater than zero."
        )

    if specific_heat <= 0:
        raise ValueError(
            "Specific heat must be greater than zero."
        )

    exponential_term = math.exp(
        -heat_transfer_coefficient
        * area
        * time
        / (mass * specific_heat)
    )

    return (
        ambient_temperature
        + (
            initial_temperature
            - ambient_temperature
        )
        * exponential_term
    )