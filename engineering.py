"""Core engineering objects for the FluidFlow Engineering Suite."""


class Fluid:
    """Represent the physical properties of a working fluid."""

    def __init__(self, name, density, viscosity):
        """
        Initialize a fluid.

        Parameters
        ----------
        name : str
            Name of the fluid.
        density : float
            Fluid density in kg/m^3.
        viscosity : float
            Dynamic viscosity in Pa.s.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Fluid name must be a non-empty string.")

        if density <= 0:
            raise ValueError("Fluid density must be greater than zero.")

        if viscosity <= 0:
            raise ValueError("Dynamic viscosity must be greater than zero.")

        self.name = name
        self.density = float(density)
        self.viscosity = float(viscosity)

    def __repr__(self):
        """Return a readable representation of the fluid."""
        return (
            f"Fluid(name='{self.name}', "
            f"density={self.density}, "
            f"viscosity={self.viscosity})"
        )


class Pipe:
    """Represent the geometric properties of a circular pipe."""

    def __init__(self, diameter, length, roughness):
        """
        Initialize a pipe.

        Parameters
        ----------
        diameter : float
            Internal pipe diameter in metres.
        length : float
            Pipe length in metres.
        roughness : float
            Absolute pipe roughness in metres.
        """
        if diameter <= 0:
            raise ValueError("Pipe diameter must be greater than zero.")

        if length <= 0:
            raise ValueError("Pipe length must be greater than zero.")

        if roughness < 0:
            raise ValueError("Pipe roughness cannot be negative.")

        self.diameter = float(diameter)
        self.length = float(length)
        self.roughness = float(roughness)

    @property
    def area(self):
        """Calculate the internal cross-sectional area in square metres."""
        import math

        return math.pi * self.diameter**2 / 4


class HeatTransferWall:
    """Represent a flat wall used for conduction calculations."""

    def __init__(self, thickness, area, thermal_conductivity):
        """
        Initialize a flat wall.

        Parameters
        ----------
        thickness : float
            Wall thickness in metres.
        area : float
            Heat-transfer area in square metres.
        thermal_conductivity : float
            Thermal conductivity in W/(m.K).
        """
        if thickness <= 0:
            raise ValueError("Wall thickness must be greater than zero.")

        if area <= 0:
            raise ValueError("Wall area must be greater than zero.")

        if thermal_conductivity <= 0:
            raise ValueError(
                "Thermal conductivity must be greater than zero."
            )

        self.thickness = float(thickness)
        self.area = float(area)
        self.thermal_conductivity = float(thermal_conductivity)