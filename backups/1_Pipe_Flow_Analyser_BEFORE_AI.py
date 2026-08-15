"""Pipe Flow Analyser - FluidFlow Engineering Suite."""

import io
import math

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from engineering import Fluid, Pipe
from calculations import calculate_pipe_flow
from validation import (
    colebrook_friction_factor,
    compare_friction_factors,
)


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Pipe Flow Analyser",
    page_icon="💧",
    layout="wide",
)


# ---------------------------------------------------------
# CUSTOM STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.6rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.05rem;
        opacity: 0.75;
        margin-bottom: 1.5rem;
    }

    .metric-card {
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 1rem;
    }

    .verification {
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">💧 Pipe Flow Analyser</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
    Darcy-Weisbach pipe-flow analysis with Reynolds-number
    classification, friction-factor calculation, pressure-loss
    prediction and independent engineering verification.
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# FLUID DATABASE
# ---------------------------------------------------------

FLUID_DATABASE = {
    "Water": {
        "density": 998.2,
        "viscosity": 0.001002,
    },
    "Air": {
        "density": 1.225,
        "viscosity": 1.81e-5,
    },
    "Crude Oil": {
        "density": 850.0,
        "viscosity": 0.025,
    },
}


# ---------------------------------------------------------
# SIDEBAR INPUTS
# ---------------------------------------------------------

st.sidebar.header("Fluid Properties")

fluid_choice = st.sidebar.selectbox(
    "Select fluid",
    [
        "Water",
        "Air",
        "Crude Oil",
        "User-defined",
    ],
)

if fluid_choice == "User-defined":

    density = st.sidebar.number_input(
        "Density (kg/m³)",
        min_value=0.0001,
        value=1000.0,
        step=1.0,
    )

    viscosity = st.sidebar.number_input(
        "Dynamic viscosity (Pa·s)",
        min_value=0.000001,
        value=0.001,
        format="%.6f",
    )

else:

    density = FLUID_DATABASE[fluid_choice]["density"]
    viscosity = FLUID_DATABASE[fluid_choice]["viscosity"]

    st.sidebar.info(
        f"""
        **{fluid_choice} properties**

        Density: {density:g} kg/m³

        Dynamic viscosity: {viscosity:g} Pa·s
        """
    )


st.sidebar.header("Pipe Parameters")

diameter = st.sidebar.number_input(
    "Internal diameter (m)",
    min_value=0.0001,
    value=0.05,
    step=0.005,
)

length = st.sidebar.number_input(
    "Pipe length (m)",
    min_value=0.01,
    value=100.0,
    step=10.0,
)

roughness = st.sidebar.number_input(
    "Absolute roughness (m)",
    min_value=0.0,
    value=0.000045,
    format="%.7f",
)

flow_rate = st.sidebar.number_input(
    "Volumetric flow rate (m³/s)",
    min_value=0.0,
    value=0.002,
    step=0.0001,
    format="%.6f",
)


# ---------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------

try:

    fluid = Fluid(
        fluid_choice,
        density,
        viscosity,
    )

    pipe = Pipe(
        diameter,
        length,
        roughness,
    )

    if flow_rate <= 0:

        st.warning(
            "Enter a flow rate greater than zero to perform "
            "the pipe-flow analysis."
        )

        st.stop()

    results = calculate_pipe_flow(
        fluid,
        pipe,
        flow_rate,
    )

except ValueError as error:

    st.error(f"Input error: {error}")
    st.stop()

except Exception as error:

    st.error(
        "The calculation could not be completed. "
        f"Technical detail: {error}"
    )
    st.stop()


# ---------------------------------------------------------
# RESULT VARIABLES
# ---------------------------------------------------------

velocity = results["velocity"]
reynolds_number = results["reynolds_number"]
flow_regime = results["flow_regime"]
friction_factor = results["friction_factor"]
pressure_drop = results["pressure_drop"]


# ---------------------------------------------------------
# MAIN RESULTS
# ---------------------------------------------------------

st.subheader("Analysis Results")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Velocity",
    f"{velocity:.3f} m/s",
)

col2.metric(
    "Reynolds Number",
    f"{reynolds_number:,.0f}",
)

col3.metric(
    "Flow Regime",
    flow_regime,
)

col4.metric(
    "Friction Factor",
    f"{friction_factor:.5f}",
)

col5.metric(
    "Pressure Drop",
    f"{pressure_drop / 1000:.3f} kPa",
)


# ---------------------------------------------------------
# FLOW REGIME WARNING
# ---------------------------------------------------------

if flow_regime == "Laminar":

    st.success(
        "Laminar flow: viscous effects dominate the flow behavior."
    )

elif flow_regime == "Transitional":

    st.warning(
        "Transitional flow detected. Friction-factor correlations "
        "are less reliable in this region."
    )

else:

    st.info(
        "Turbulent flow detected. The turbulent friction-factor "
        "correlation and Colebrook verification are applicable."
    )


# ---------------------------------------------------------
# ENGINEERING EQUATIONS
# ---------------------------------------------------------

with st.expander("📐 Governing Engineering Equations"):

    st.markdown(
        r"""
### Cross-sectional area

\[
A=\frac{\pi D^2}{4}
\]

### Average velocity

\[
V=\frac{Q}{A}
\]

### Reynolds number

\[
Re=\frac{\rho VD}{\mu}
\]

### Darcy-Weisbach pressure loss

\[
\Delta P =
f\frac{L}{D}\frac{\rho V^2}{2}
\]

For laminar flow:

\[
f=\frac{64}{Re}
\]

For turbulent flow, the primary calculation uses the
Swamee-Jain explicit approximation, while the result is
independently checked against the Colebrook-White equation.
        """
    )


# ---------------------------------------------------------
# ENGINEERING VERIFICATION
# ---------------------------------------------------------

st.subheader("Engineering Verification")

if reynolds_number > 4000:

    try:

        verified_factor = colebrook_friction_factor(
            reynolds_number,
            roughness,
            diameter,
        )

        comparison = compare_friction_factors(
            friction_factor,
            verified_factor,
        )

        difference = comparison["percentage_difference"]

        vcol1, vcol2, vcol3 = st.columns(3)

        vcol1.metric(
            "Primary friction factor",
            f"{friction_factor:.6f}",
        )

        vcol2.metric(
            "Colebrook friction factor",
            f"{verified_factor:.6f}",
        )

        vcol3.metric(
            "Difference",
            f"{difference:.3f}%",
        )

        if difference <= 2:

            st.success(
                "✓ Verification passed. The primary friction-factor "
                "calculation agrees closely with the independent "
                "Colebrook solution."
            )

        else:

            st.warning(
                "Verification difference exceeds 2%. "
                "Review the input conditions and correlation assumptions."
            )

    except (ValueError, RuntimeError) as error:

        st.warning(
            f"Colebrook verification unavailable: {error}"
        )

else:

    st.info(
        "Colebrook verification is applied only to turbulent flow "
        "(Re > 4000)."
    )


# ---------------------------------------------------------
# PRESSURE DROP CURVE
# ---------------------------------------------------------

st.subheader("Pressure Drop vs Flow Rate")

minimum_flow = max(flow_rate * 0.1, 1e-7)
maximum_flow = max(flow_rate * 2.0, minimum_flow * 2)

flow_values = [
    minimum_flow
    + i * (maximum_flow - minimum_flow) / 39
    for i in range(40)
]

pressure_values = []

for q in flow_values:

    try:

        curve_result = calculate_pipe_flow(
            fluid,
            pipe,
            q,
        )

        pressure_values.append(
            curve_result["pressure_drop"] / 1000
        )

    except ValueError:

        pressure_values.append(float("nan"))


figure, axis = plt.subplots(figsize=(10, 5))

axis.plot(
    flow_values,
    pressure_values,
    linewidth=2,
)

axis.scatter(
    [flow_rate],
    [pressure_drop / 1000],
    s=70,
)

axis.set_title("Pressure Drop vs Volumetric Flow Rate")
axis.set_xlabel("Flow Rate (m³/s)")
axis.set_ylabel("Pressure Drop (kPa)")
axis.grid(True, alpha=0.25)

st.pyplot(figure)

plt.close(figure)


# ---------------------------------------------------------
# RESULT TABLE
# ---------------------------------------------------------

st.subheader("Detailed Results")

result_table = pd.DataFrame(
    {
        "Parameter": [
            "Fluid",
            "Density",
            "Dynamic viscosity",
            "Pipe diameter",
            "Pipe length",
            "Pipe roughness",
            "Flow rate",
            "Velocity",
            "Reynolds number",
            "Flow regime",
            "Darcy friction factor",
            "Pressure drop",
        ],
        "Value": [
            fluid.name,
            f"{fluid.density:.3f} kg/m³",
            f"{fluid.viscosity:.6g} Pa·s",
            f"{pipe.diameter:.4f} m",
            f"{pipe.length:.2f} m",
            f"{pipe.roughness:.7f} m",
            f"{flow_rate:.6f} m³/s",
            f"{velocity:.5f} m/s",
            f"{reynolds_number:.2f}",
            flow_regime,
            f"{friction_factor:.7f}",
            f"{pressure_drop:.2f} Pa",
        ],
    }
)

st.dataframe(
    result_table,
    use_container_width=True,
    hide_index=True,
)


# ---------------------------------------------------------
# CSV EXPORT
# ---------------------------------------------------------

st.subheader("Export Results")

csv_buffer = io.StringIO()

result_table.to_csv(
    csv_buffer,
    index=False,
)

st.download_button(
    label="⬇️ Download Pipe Flow Results",
    data=csv_buffer.getvalue(),
    file_name="pipe_flow_results.csv",
    mime="text/csv",
)


# ---------------------------------------------------------
# ASSUMPTIONS
# ---------------------------------------------------------

with st.expander("⚙️ Engineering Assumptions"):

    st.markdown(
        """
- Steady internal pipe flow is assumed.
- The pipe is circular and has a constant internal diameter.
- Fluid properties are treated as constant during the calculation.
- Pressure loss represents frictional loss along the pipe.
- Minor losses from valves, bends and fittings are not included.
- The Darcy-Weisbach equation is used for pressure loss.
- Laminar flow uses the analytical Darcy friction factor.
- Turbulent flow uses an explicit friction-factor correlation and
  independent Colebrook verification.
- Transitional flow is flagged because friction-factor prediction
  is less certain in that region.
        """
    )