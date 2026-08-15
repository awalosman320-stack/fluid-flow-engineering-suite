import streamlit as st

st.set_page_config(
    page_title="FluidFlow Engineering Suite",
    page_icon="⚙️",
    layout="wide",
)

st.title("⚙️ FluidFlow Engineering Suite")

st.subheader("Engineering Computation & Analysis Platform")

st.write(
    """
    A professional engineering suite for pipe-flow analysis,
    heat-transfer calculations, and rock/fluid data analysis.
    """
)

st.info(
    "Select a module from the navigation menu on the left."
)

st.markdown(
    """
    ### Available Engineering Modules

    **💧 Pipe Flow Analyser**

    Analyse internal pipe flow using Reynolds number,
    friction-factor correlations and Darcy-Weisbach pressure loss.

    **🔥 Heat Transfer**

    Calculate conduction through flat walls and transient
    Newton's-law cooling.

    **🪨 Rock & Fluid Dashboard**

    Upload and analyse engineering datasets.

    **🤖 AI Engineering Assistant**

    Get engineering explanations and interpretation of results.
    """
)