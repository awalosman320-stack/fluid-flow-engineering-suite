"""Engineering calculation functions for the FluidFlow Engineering Suite."""

import math


def calculate_velocity(flow_rate, diameter):
    """
    Calculate the average fluid velocity in a circular pipe.

    Parameters
    ----------
    flow_rate : float
        Volumetric flow rate in m^3/s.
    diameter : float
        Internal pipe diameter in metres.

    Returns
    -------
    float
        Average fluid velocity in m/s.
    """
    if flow_rate < 0:
        raise ValueError("Flow rate cannot be negative.")

    if diameter <= 0:
        raise ValueError("Pipe diameter must be greater than zero.")

    area = math.pi * diameter**2 / 4
    return flow_rate / area


def calculate_reynolds_number(density, velocity, diameter, viscosity):
    """
    Calculate the Reynolds number for internal pipe flow.

    Parameters
    ----------
    density : float
        Fluid density in kg/m^3.
    velocity : float
        Average velocity in m/s.
    diameter : float
        Pipe diameter in metres.
    viscosity : float
        Dynamic viscosity in Pa.s.

    Returns
    -------
    float
        Reynolds number.
    """
    if density <= 0:
        raise ValueError("Density must be greater than zero.")

    if velocity < 0:
        raise ValueError("Velocity cannot be negative.")

    if diameter <= 0:
        raise ValueError("Diameter must be greater than zero.")

    if viscosity <= 0:
        raise ValueError("Viscosity must be greater than zero.")

    return (density * velocity * diameter) / viscosity


def determine_flow_regime(reynolds_number):
    """
    Determine the flow regime from the Reynolds number.

    Parameters
    ----------
    reynolds_number : float
        Reynolds number.

    Returns
    -------
    str
        Flow regime: Laminar, Transitional, or Turbulent.
    """
    if reynolds_number < 0:
        raise ValueError("Reynolds number cannot be negative.")

    if reynolds_number < 2300:
        return "Laminar"

    if reynolds_number <= 4000:
        return "Transitional"

    return "Turbulent"


def calculate_friction_factor(reynolds_number, roughness, diameter):
    """
    Calculate the Darcy friction factor.

    Laminar flow uses f = 64/Re.

    Turbulent flow uses the Swamee-Jain explicit approximation
    to the Colebrook equation.

    Parameters
    ----------
    reynolds_number : float
        Reynolds number.
    roughness : float
        Absolute pipe roughness in metres.
    diameter : float
        Pipe diameter in metres.

    Returns
    -------
    float
        Darcy friction factor.
    """
    if reynolds_number <= 0:
        raise ValueError("Reynolds number must be greater than zero.")

    if roughness < 0:
        raise ValueError("Roughness cannot be negative.")

    if diameter <= 0:
        raise ValueError("Diameter must be greater than zero.")

    if reynolds_number < 2300:
        return 64 / reynolds_number

    relative_roughness = roughness / diameter

    friction_factor = 0.25 / (
        math.log10(
            relative_roughness / 3.7
            + 5.74 / reynolds_number**0.9
        )
        ** 2
    )

    return friction_factor


def calculate_pressure_drop(
    friction_factor,
    length,
    diameter,
    density,
    velocity
):
    """
    Calculate pressure loss using the Darcy-Weisbach equation.

    Parameters
    ----------
    friction_factor : float
        Darcy friction factor.
    length : float
        Pipe length in metres.
    diameter : float
        Pipe diameter in metres.
    density : float
        Fluid density in kg/m^3.
    velocity : float
        Average fluid velocity in m/s.

    Returns
    -------
    float
        Pressure drop in Pascals.
    """
    if friction_factor < 0:
        raise ValueError("Friction factor cannot be negative.")

    if length <= 0:
        raise ValueError("Pipe length must be greater than zero.")

    if diameter <= 0:
        raise ValueError("Pipe diameter must be greater than zero.")

    if density <= 0:
        raise ValueError("Density must be greater than zero.")

    if velocity < 0:
        raise ValueError("Velocity cannot be negative.")

    return (
        friction_factor
        * (length / diameter)
        * (density * velocity**2 / 2)
    )


def calculate_pipe_flow(
    fluid,
    pipe,
    flow_rate
):
    """
    Perform a complete pipe-flow analysis.

    Parameters
    ----------
    fluid : Fluid
        Fluid object from engineering.py.
    pipe : Pipe
        Pipe object from engineering.py.
    flow_rate : float
        Volumetric flow rate in m^3/s.

    Returns
    -------
    dict
        Calculated velocity, Reynolds number, flow regime,
        friction factor, and pressure drop.
    """
    velocity = calculate_velocity(
        flow_rate,
        pipe.diameter
    )

    reynolds_number = calculate_reynolds_number(
        fluid.density,
        velocity,
        pipe.diameter,
        fluid.viscosity
    )

    flow_regime = determine_flow_regime(
        reynolds_number
    )

    friction_factor = calculate_friction_factor(
        reynolds_number,
        pipe.roughness,
        pipe.diameter
    )

    pressure_drop = calculate_pressure_drop(
        friction_factor,
        pipe.length,
        pipe.diameter,
        fluid.density,
        velocity
    )

    return {
        "velocity": velocity,
        "reynolds_number": reynolds_number,
        "flow_regime": flow_regime,
        "friction_factor": friction_factor,
        "pressure_drop": pressure_drop,
    }