"""
AI Engineering Assistant
FluidFlow Engineering Suite

Gemini-powered assistant specializing in:
- Fluid mechanics
- Pipe-flow engineering
- Heat transfer
- Petroleum engineering
- Rock/fluid fundamentals

Numerical engineering calculations remain deterministic.
Gemini is used primarily for explanation and interpretation.
"""

import os

import streamlit as st
from google import genai


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Engineering Assistant",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "gemini-3.6-flash"

SYSTEM_INSTRUCTION = """
You are the AI Engineering Assistant for the FluidFlow Engineering Suite.

You specialize in:

1. Fluid mechanics
2. Pipe-flow engineering
3. Heat transfer
4. Petroleum engineering
5. Reservoir fundamentals
6. Rock-fluid fundamentals
7. Engineering data interpretation

Your role is to help engineering students and users understand
engineering concepts, equations, assumptions, calculated results,
and physical meaning.

IMPORTANT ENGINEERING RULES:

- Do not invent numerical results.
- Do not pretend that an AI-generated estimate is a verified
  engineering calculation.
- Numerical results supplied by the application's deterministic
  calculation engine must be treated as authoritative for
  interpretation.
- Clearly distinguish between calculated results and AI interpretation.
- State assumptions when they materially affect an answer.
- Use SI units unless the user requests another unit system.
- Explain equations and variables clearly.
- If information is insufficient, say what information is missing.
- Do not make unsupported engineering claims.

FLUID MECHANICS TOPICS:

- Continuity
- Flow rate
- Velocity
- Mass flow rate
- Reynolds number
- Laminar flow
- Transitional flow
- Turbulent flow
- Darcy-Weisbach equation
- Darcy friction factor
- Pipe roughness
- Pressure loss
- Head loss
- Fluid viscosity
- Fluid density

HEAT TRANSFER TOPICS:

- Fourier's law
- Thermal conduction
- Convection
- Newton's law of cooling
- Thermal resistance
- Steady-state heat transfer
- Transient heat transfer
- Thermal conductivity
- Heat-transfer coefficient
- Temperature differences
- Energy balances

PETROLEUM ENGINEERING TOPICS:

- Reservoir fundamentals
- Porosity
- Permeability
- Darcy's law
- Rock-fluid relationships
- Reservoir pressure
- Fluid flow through porous media
- Basic production engineering
- Petroleum fluid properties

DATA INTERPRETATION:

- Explain statistical summaries.
- Identify possible trends.
- Distinguish correlation from causation.
- Identify missing or suspicious data.
- Avoid unsupported conclusions.

COMMUNICATION STYLE:

- Be professional.
- Be technically accurate.
- Use headings and bullet points when useful.
- Show equations where helpful.
- Explain the physical meaning of results.
- Give practical engineering interpretation.
- Keep answers understandable to an engineering student.

ENGINEERING DISCLAIMER:

You are an engineering education and analysis assistant.
Professional engineering judgment, laboratory measurements,
field validation, and applicable engineering standards should
be used for real-world engineering decisions.
"""


# ============================================================
# GEMINI CLIENT
# ============================================================

@st.cache_resource
def create_gemini_client():
    """Create a reusable Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    return genai.Client(
        api_key=api_key,
        http_options={"api_version": "v1"},
    )


client = create_gemini_client()


# ============================================================
# SESSION STATE
# ============================================================

if "engineering_messages" not in st.session_state:
    st.session_state.engineering_messages = []

if "gemini_interaction_id" not in st.session_state:
    st.session_state.gemini_interaction_id = None

if "engineering_context" not in st.session_state:
    st.session_state.engineering_context = None


# ============================================================
# HEADER
# ============================================================

st.title("🤖 AI Engineering Assistant")

st.markdown(
    """
    ### Petroleum • Fluid • Thermal Engineering

    Ask engineering questions, request explanations, or interpret
    verified engineering results from the FluidFlow Engineering Suite.
    """
)


# ============================================================
# API STATUS
# ============================================================

if client is None:

    st.error(
        """
        **Gemini API key not detected.**

        Make sure the `GEMINI_API_KEY` environment variable is
        configured before starting Streamlit.
        """
    )

    st.stop()

else:

    st.success(
        "Gemini AI connection is configured • Gemini 3.6 Flash"
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Engineering Assistant")

    st.markdown(
        """
        **Specialization**

        💧 Fluid Mechanics

        🔧 Pipe Flow

        🌡️ Heat Transfer

        🛢️ Petroleum Engineering

        🪨 Rock & Fluid Fundamentals

        📊 Engineering Data
        """
    )

    st.divider()

    st.subheader("Quick Questions")

    quick_questions = [
        "Explain Reynolds number.",
        "Why does pressure drop increase when pipe diameter decreases?",
        "Explain the Darcy-Weisbach equation.",
        "What is the difference between laminar and turbulent flow?",
        "Explain Fourier's law of heat conduction.",
        "Explain Newton's law of cooling.",
        "What is the difference between porosity and permeability?",
    ]

    selected_question = st.selectbox(
        "Choose a question",
        ["Select a question"] + quick_questions,
    )

    if selected_question != "Select a question":

        if st.button(
            "Ask Selected Question",
            use_container_width=True,
        ):

            st.session_state.pending_question = selected_question


    st.divider()

    if st.button(
        "Clear Conversation",
        use_container_width=True,
    ):

        st.session_state.engineering_messages = []
        st.session_state.gemini_interaction_id = None
        st.session_state.engineering_context = None

        st.rerun()


# ============================================================
# ENGINEERING CONTEXT
# ============================================================

if st.session_state.engineering_context:

    with st.expander(
        "Current Engineering Context",
        expanded=True,
    ):

        st.code(
            st.session_state.engineering_context,
            language="text",
        )

        if st.button("Clear Engineering Context"):

            st.session_state.engineering_context = None

            st.rerun()


# ============================================================
# DISPLAY PREVIOUS CHAT
# ============================================================

for message in st.session_state.engineering_messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# USER INPUT
# ============================================================

user_prompt = st.chat_input(
    "Ask your engineering question..."
)


# Quick-question support
if "pending_question" in st.session_state:

    if st.session_state.pending_question:

        user_prompt = st.session_state.pending_question

        st.session_state.pending_question = None


# ============================================================
# GEMINI INTERACTION
# ============================================================

if user_prompt:

    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    st.session_state.engineering_messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(user_prompt)


    # --------------------------------------------------------
    # Build current request
    # --------------------------------------------------------

    current_input = user_prompt

    if st.session_state.engineering_context:

        current_input = f"""
ENGINEERING RESULTS CONTEXT:

{st.session_state.engineering_context}

USER QUESTION:

{user_prompt}
"""


    # --------------------------------------------------------
    # Generate response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Analyzing engineering question..."
        ):

            try:

                # First interaction
                if st.session_state.gemini_interaction_id is None:

                    interaction = client.interactions.create(
                        model=MODEL_NAME,
                        input=current_input,
                        system_instruction=SYSTEM_INSTRUCTION,
                    )

                # Continue existing conversation
                else:

                    interaction = client.interactions.create(
                        model=MODEL_NAME,
                        previous_interaction_id=(
                            st.session_state.gemini_interaction_id
                        ),
                        input=current_input,
                        system_instruction=SYSTEM_INSTRUCTION,
                    )


                # ------------------------------------------------
                # Extract response
                # ------------------------------------------------

                answer = interaction.output_text

                if not answer:

                    answer = (
                        "Gemini did not return a text response. "
                        "Please try the question again."
                    )


                # ------------------------------------------------
                # Save interaction state
                # ------------------------------------------------

                st.session_state.gemini_interaction_id = (
                    interaction.id
                )


                # ------------------------------------------------
                # Display answer
                # ------------------------------------------------

                st.markdown(answer)


                # ------------------------------------------------
                # Save answer
                # ------------------------------------------------

                st.session_state.engineering_messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )


            except Exception as error:

                error_text = str(error)

                if "429" in error_text:

                    error_message = (
                        "Gemini API quota has been reached. "
                        "Please check your Gemini API quota."
                    )

                elif "403" in error_text:

                    error_message = (
                        "Gemini rejected the request. "
                        "Please check the API key permissions."
                    )

                elif "401" in error_text:

                    error_message = (
                        "Gemini authentication failed. "
                        "Please check GEMINI_API_KEY."
                    )

                elif "404" in error_text:

                    error_message = (
                        "The selected Gemini model or API endpoint "
                        "is unavailable. The application is configured "
                        "for Gemini 3.6 Flash through the Interactions API."
                    )

                else:

                    error_message = (
                        "The engineering assistant could not "
                        "complete the request."
                    )

                st.error(error_message)

                with st.expander("Technical Details"):

                    st.code(
                        error_text,
                        language="text",
                    )


# ============================================================
# ENGINEERING AI PRINCIPLES
# ============================================================

with st.expander(
    "Engineering AI Principles"
):

    st.markdown(
        """
        ### Calculation integrity

        Numerical engineering calculations should be performed
        by deterministic Python calculation functions whenever
        possible.

        Gemini is primarily used to:

        - Explain engineering concepts
        - Interpret verified results
        - Explain equations
        - Discuss assumptions
        - Provide engineering context

        ### Important distinction

        **Calculated Result**

        Produced by the engineering calculation engine.

        **AI Interpretation**

        Explanation generated by Gemini from the supplied result.

        These roles are deliberately separated to reduce the risk
        of unsupported numerical answers.
        """
    )


# ============================================================
# MODULE D DOCUMENTATION
# ============================================================

with st.expander(
    "AI Development & Verification Record"
):

    st.markdown(
        """
        ### Prompt 1 — Engineering reasoning

        **Verified:** The assistant was configured for petroleum,
        fluid, and thermal engineering.

        **Correction:** Engineering assumptions and terminology
        were explicitly defined in the system instruction.

        ---

        ### Prompt 2 — Numerical integrity

        **Verified:** Numerical results should originate from
        deterministic engineering calculations.

        **Correction:** Gemini was instructed to distinguish
        calculated results from AI interpretation.

        ---

        ### Prompt 3 — Engineering communication

        **Verified:** The assistant uses equations, units,
        assumptions, and engineering explanations.

        **Correction:** The response style was constrained to
        professional, technically meaningful explanations.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "FluidFlow Engineering Suite • AI Engineering Assistant • "
    "Gemini 3.6 Flash"
)