"""Heat Transfer Calculator Streamlit page."""

import math

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from heat_transfer import (
    calculate_conduction_heat_rate,
    calculate_cooling_time,
    cooling_temperature,
)


st.set_page_config(
    page_title="Heat Transfer Calculator",
    page_icon="🔥",
    layout="wide",
)


st.title("🔥 Heat Transfer Calculator")

st.markdown(
    """
    Calculate steady-state conduction through a flat wall and
    transient cooling using Newton's Law of Cooling.

    All calculations use SI units.
    """
)


# =========================================================
# SECTION 1 — STEADY-STATE CONDUCTION
# =========================================================

st.header("1. Steady-State Conduction")

st.markdown(
    """
    **Physical meaning:** This section calculates the rate at which
    thermal energy passes through a flat wall when temperatures are
    steady and heat transfer occurs by conduction.

    Fourier's law:

    \[
    Q = \\frac{kA(T_{hot}-T_{cold})}{L}
    \]

    where:

    - **k** = thermal conductivity of the wall material, W/(m·K)
    - **A** = wall area, m²
    - **L** = wall thickness, m
    - **Thot** = hot-side temperature, °C
    - **Tcold** = cold-side temperature, °C
    """
)


col1, col2 = st.columns(2)

with col1:

    conductivity = st.number_input(
        "Thermal conductivity, k (W/(m·K))",
        min_value=0.001,
        value=1.5,
        step=0.1,
    )

    wall_area = st.number_input(
        "Wall area, A (m²)",
        min_value=0.001,
        value=10.0,
        step=0.5,
    )

    wall_thickness = st.number_input(
        "Wall thickness, L (m)",
        min_value=0.001,
        value=0.2,
        step=0.01,
    )


with col2:

    hot_temperature = st.number_input(
        "Hot-side temperature (°C)",
        value=100.0,
        step=5.0,
    )

    cold_temperature = st.number_input(
        "Cold-side temperature (°C)",
        value=20.0,
        step=5.0,
    )


try:

    conduction_heat_rate = calculate_conduction_heat_rate(
        conductivity,
        wall_area,
        wall_thickness,
        hot_temperature,
        cold_temperature,
    )

    st.metric(
        "Conduction Heat-Transfer Rate",
        f"{conduction_heat_rate:,.2f} W",
    )

    if conduction_heat_rate >= 0:

        st.success(
            "✓ Conduction calculation completed successfully."
        )

    else:

        st.warning(
            "The calculated heat-transfer rate is negative, "
            "indicating that heat flows in the opposite direction."
        )

except ValueError as error:

    st.error(f"Input error: {error}")


# =========================================================
# SECTION 2 — NEWTON'S LAW OF COOLING
# =========================================================

st.divider()

st.header("2. Newton's Law of Cooling")

st.markdown(
    """
    **Physical meaning:** Newton's Law of Cooling predicts how the
    temperature of an object changes as it exchanges heat with its
    surrounding environment.

    The analytical solution is:

    \[
    T(t)=T_{\\infty}
    +(T_0-T_{\\infty})
    e^{-hAt/(mc_p)}
    \]

    where:

    - **T₀** = initial object temperature, °C
    - **T∞** = ambient temperature, °C
    - **h** = convective heat-transfer coefficient, W/(m²·K)
    - **A** = exposed surface area, m²
    - **m** = object mass, kg
    - **cp** = specific heat capacity, J/(kg·K)
    """
)


col1, col2, col3 = st.columns(3)

with col1:

    initial_temperature = st.slider(
        "Initial temperature T₀ (°C)",
        min_value=-50.0,
        max_value=200.0,
        value=100.0,
        step=1.0,
    )

    ambient_temperature = st.slider(
        "Ambient temperature T∞ (°C)",
        min_value=-50.0,
        max_value=100.0,
        value=25.0,
        step=1.0,
    )


with col2:

    target_temperature = st.slider(
        "Target temperature (°C)",
        min_value=-50.0,
        max_value=200.0,
        value=50.0,
        step=1.0,
    )

    heat_transfer_coefficient = st.slider(
        "Heat-transfer coefficient h (W/(m²·K))",
        min_value=0.1,
        max_value=200.0,
        value=10.0,
        step=0.5,
    )


with col3:

    cooling_area = st.slider(
        "Exposed surface area A (m²)",
        min_value=0.01,
        max_value=20.0,
        value=2.0,
        step=0.1,
    )

    object_mass = st.slider(
        "Object mass m (kg)",
        min_value=0.1,
        max_value=100.0,
        value=5.0,
        step=0.5,
    )

    specific_heat = st.slider(
        "Specific heat cp (J/(kg·K))",
        min_value=100.0,
        max_value=5000.0,
        value=4180.0,
        step=50.0,
    )


# =========================================================
# COOLING TIME
# =========================================================

st.subheader("Cooling Time")

try:

    cooling_time = calculate_cooling_time(
        initial_temperature,
        target_temperature,
        ambient_temperature,
        heat_transfer_coefficient,
        cooling_area,
        object_mass,
        specific_heat,
    )

    minutes = cooling_time / 60

    hours = cooling_time / 3600

    time_col1, time_col2, time_col3 = st.columns(3)

    time_col1.metric(
        "Cooling Time",
        f"{cooling_time:,.1f} s",
    )

    time_col2.metric(
        "Cooling Time",
        f"{minutes:,.2f} min",
    )

    time_col3.metric(
        "Cooling Time",
        f"{hours:,.3f} h",
    )

    st.success(
        "✓ Analytical cooling-time solution calculated successfully."
    )

except ValueError as error:

    st.warning(
        f"Cooling-time calculation unavailable: {error}"
    )

    cooling_time = None


# =========================================================
# COOLING CURVE
# =========================================================

st.subheader("Interactive Cooling Curve")

if cooling_time is not None:

    maximum_time = max(
        cooling_time * 1.5,
        60,
    )

    time_values = np.linspace(
        0,
        maximum_time,
        200,
    )

    temperature_values = []

    for time in time_values:

        temperature = cooling_temperature(
            time,
            initial_temperature,
            ambient_temperature,
            heat_transfer_coefficient,
            cooling_area,
            object_mass,
            specific_heat,
        )

        temperature_values.append(
            temperature
        )

    figure, axis = plt.subplots(
        figsize=(10, 5)
    )

    axis.plot(
        time_values / 60,
        temperature_values,
        linewidth=2,
    )

    axis.axhline(
        target_temperature,
        linestyle="--",
        linewidth=1.5,
        label="Target temperature",
    )

    axis.axhline(
        ambient_temperature,
        linestyle=":",
        linewidth=1.5,
        label="Ambient temperature",
    )

    axis.set_xlabel(
        "Time (minutes)"
    )

    axis.set_ylabel(
        "Temperature (°C)"
    )

    axis.set_title(
        "Object Temperature vs Time"
    )

    axis.grid(
        True,
        alpha=0.25,
    )

    axis.legend()

    st.pyplot(figure)

    plt.close(figure)


# =========================================================
# ANALYTICAL VERIFICATION
# =========================================================

st.divider()

st.header("✅ Analytical Verification")

st.markdown(
    """
    The cooling calculation can be verified by substituting the
    calculated cooling time back into the analytical temperature
    equation.

    At the calculated time:

    \[
    T(t_{target}) \\approx T_{target}
    \]

    This provides an independent consistency check.
    """
)

if cooling_time is not None:

    verified_temperature = cooling_temperature(
        cooling_time,
        initial_temperature,
        ambient_temperature,
        heat_transfer_coefficient,
        cooling_area,
        object_mass,
        specific_heat,
    )

    verification_error = abs(
        verified_temperature - target_temperature
    )

    verification_col1, verification_col2 = st.columns(2)

    verification_col1.metric(
        "Target Temperature",
        f"{target_temperature:.4f} °C",
    )

    verification_col2.metric(
        "Temperature at Calculated Time",
        f"{verified_temperature:.4f} °C",
    )

    if verification_error < 0.01:

        st.success(
            f"✓ Verification passed. Absolute error = "
            f"{verification_error:.6f} °C"
        )

    else:

        st.warning(
            f"Verification difference = "
            f"{verification_error:.6f} °C"
        )


# =========================================================
# ENGINEERING ASSUMPTIONS
# =========================================================

with st.expander("⚙️ Engineering Assumptions"):

    st.markdown(
        """
        ### Steady-state conduction

        - One-dimensional heat conduction is assumed.
        - Thermal conductivity is constant.
        - The wall is treated as a single homogeneous layer.
        - Contact resistance is neglected.
        - Heat generation inside the wall is neglected.

        ### Newton's Law of Cooling

        - The object is treated using the lumped-capacitance model.
        - Material properties are assumed constant.
        - Ambient temperature remains constant.
        - The convective heat-transfer coefficient remains constant.
        - Radiation heat transfer is neglected.
        - Internal temperature gradients are assumed negligible.
        """
    )