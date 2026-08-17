\# AI Usage Documentation



\## FluidFlow Engineering Suite



This document describes how artificial intelligence was used during the development and operation of the FluidFlow Engineering Suite.



The application uses Google's Gemini API through the Google GenAI Python SDK to provide engineering explanations and technical interpretation.



A central design principle of the project is:



> \*\*Deterministic engineering calculations produce numerical results, while artificial intelligence primarily explains and interprets those verified results.\*\*



This separation is intended to reduce the risk of relying on unsupported AI-generated engineering calculations.



\---



\## 1. Purpose of AI Integration



The AI Engineering Assistant was developed to provide an interactive technical assistant for engineering students and users working with:



\* Fluid mechanics

\* Pipe-flow engineering

\* Heat transfer

\* Petroleum engineering

\* Rock and fluid fundamentals



The assistant can answer conceptual engineering questions, explain equations, interpret calculated results, discuss assumptions, and provide engineering context.



The AI is not intended to replace the deterministic calculation engine.



\---



\## 2. AI Technology Used



The application uses:



\* Google Gemini

\* Google GenAI Python SDK

\* Streamlit

\* Python



The Gemini API is accessed through the application's AI assistant module.



The API key is not stored in the source code or committed to GitHub.



For local development, the application can read the `GEMINI\_API\_KEY` environment variable.



For Streamlit Community Cloud deployment, the API key is stored using Streamlit's secret-management system.



The application supports both mechanisms through:



```python

api\_key = st.secrets.get("GEMINI\_API\_KEY") or os.getenv("GEMINI\_API\_KEY")

```



This allows the same application to operate securely in both local and deployed environments.



\---



\## 3. AI Development Prompt 1 — Engineering Reasoning



The first major AI-development objective was to configure the assistant for engineering-focused reasoning.



The assistant was instructed to work primarily within the following domains:



\* Fluid mechanics

\* Pipe-flow engineering

\* Heat transfer

\* Petroleum engineering

\* Rock and fluid fundamentals



The assistant was also instructed to use appropriate engineering terminology and explain engineering concepts in a technically understandable manner.



\### Development objective



The objective was to create an AI assistant capable of providing useful engineering explanations rather than behaving as a general-purpose chatbot.



The assistant should:



\* Explain engineering concepts

\* Explain relevant equations

\* Define technical terminology

\* Discuss physical meaning

\* Identify important assumptions

\* Provide appropriate engineering context



\---



\## 4. AI Development Prompt 2 — Numerical Integrity



The second major AI-development objective was numerical integrity.



The assistant was designed around the principle that numerical engineering results should originate from deterministic calculation functions whenever possible.



For example, the Pipe Flow Analyser performs calculations such as:



\* Velocity

\* Reynolds number

\* Flow regime

\* Darcy friction factor

\* Pressure drop



These calculations are performed by Python calculation functions rather than being delegated to Gemini.



Similarly, the Heat Transfer module performs deterministic calculations for:



\* Conduction heat-transfer rate

\* Cooling time

\* Cooling temperature



The AI receives the resulting engineering values and is primarily used to interpret them.



\### AI numerical-integrity instructions



The assistant is expected to:



1\. Treat supplied verified engineering results as authoritative context.

2\. Explain the physical meaning of supplied results.

3\. Explain equations when appropriate.

4\. Discuss assumptions and limitations.

5\. Distinguish calculated values from AI interpretation.

6\. Avoid inventing unsupported numerical results.

7\. Avoid replacing deterministic calculations with unsupported estimates.



This architecture reduces the possibility that an AI-generated numerical answer will silently replace a deterministic engineering calculation.



\---



\## 5. AI Development Prompt 3 — Engineering Communication



The third major AI-development objective was professional engineering communication.



The assistant was configured to provide explanations that can include:



\* Engineering equations

\* Units

\* Assumptions

\* Physical interpretation

\* Engineering context

\* Limitations



The goal was to make the output useful for engineering learning and technical interpretation.



A good response should explain not only what a result is, but also what the result means physically.



For example, when given a Reynolds number, the assistant can explain:



\* What Reynolds number represents

\* Which flow regime the result indicates

\* The physical significance of the regime

\* Relevant assumptions

\* Why the result matters to pipe-flow analysis



\---



\## 6. Engineering Results Bridge



The application includes an engineering-results bridge between deterministic calculation modules and the AI Engineering Assistant.



\### Pipe Flow → AI



The AI can receive engineering results including:



\* Fluid

\* Density

\* Viscosity

\* Pipe diameter

\* Pipe length

\* Pipe roughness

\* Flow rate

\* Velocity

\* Reynolds number

\* Flow regime

\* Friction factor

\* Pressure drop



These values originate from the deterministic Pipe Flow calculation module.



\---



\### Heat Transfer → AI



The AI can receive:



\* Thermal conductivity

\* Wall area

\* Wall thickness

\* Hot-side temperature

\* Cold-side temperature

\* Conduction heat-transfer rate

\* Initial temperature

\* Ambient temperature

\* Target temperature

\* Heat-transfer coefficient

\* Cooling area

\* Object mass

\* Specific heat capacity

\* Cooling time

\* Verified temperature

\* Verification error



These values originate from the deterministic Heat Transfer module.



\---



\### Rock \& Fluid Data → AI



The AI can receive dataset-derived information including:



\* Dataset row count

\* Number of numerical columns

\* Summary statistics

\* Relevant dataset analysis results



The AI is expected to interpret the supplied dataset information rather than inventing measurements that are not present in the dataset.



\---



\## 7. Numerical Verification



The project includes an independent engineering verification layer.



For turbulent pipe flow, the main calculation uses the Swamee-Jain explicit approximation for the Darcy friction factor.



An independent Colebrook-White iterative calculation is also implemented in `validation.py`.



The application can compare the primary calculated friction factor against the independently evaluated value.



The comparison includes:



\* Absolute difference

\* Percentage difference



This provides an additional numerical integrity check.



The Colebrook verification function is restricted to turbulent flow because the Colebrook equation is intended for turbulent pipe-flow friction-factor calculations.



\---



\## 8. AI Safety and Engineering Limitations



The AI Engineering Assistant is a decision-support and educational component.



AI-generated explanations should not automatically be treated as professional engineering design approval.



Engineering results depend on factors including:



\* Input quality

\* Fluid properties

\* Geometry

\* Boundary conditions

\* Model assumptions

\* Correlation validity

\* Applicable engineering standards

\* Measurement uncertainty



The application therefore communicates that engineering results should be reviewed by a qualified engineer when used for real engineering decisions.



The AI should not be considered a replacement for:



\* Professional engineering review

\* Applicable codes and standards

\* Laboratory measurements

\* Field measurements

\* Engineering design calculations

\* Safety reviews



\---



\## 9. API Key Security



The Gemini API key is treated as a secret.



The key should never be:



\* Written directly into Python source code

\* Added to `README.md`

\* Committed to Git

\* Uploaded to GitHub

\* Included in screenshots

\* Shared publicly



For local development, the application can use the `GEMINI\_API\_KEY` environment variable.



For Streamlit deployment, the secret is stored through Streamlit's secret-management system.



This prevents the credential from becoming part of the public source repository.



\---



\## 10. AI Failure Handling



The application checks whether a Gemini API key is available before creating the Gemini client.



If the key is unavailable, the application does not silently assume that AI functionality is available.



Instead, the user is informed that the Gemini API key needs to be configured.



This provides a clearer failure mode than allowing an API configuration error to appear as an unexplained application failure.



\---



\## 11. Testing and Verification



The project contains an automated `pytest` test suite.



The current engineering test suite contains 12 tests covering:



1\. Velocity calculation

2\. Reynolds number calculation

3\. Laminar-flow classification

4\. Turbulent-flow classification

5\. Laminar friction factor

6\. Pressure-drop calculation

7\. Complete pipe-flow calculation

8\. Colebrook friction-factor verification

9\. Friction-factor comparison

10\. Conduction heat-transfer calculation

11\. Cooling-time calculation

12\. Cooling-temperature calculation



The current test result is:



```text

12 passed

```



The tests verify deterministic engineering calculations independently of Gemini.



This distinction is important because the AI layer should not be responsible for validating the mathematical correctness of the core engineering calculation engine.



\---



\## 12. Separation of Responsibilities



The application's architecture can be summarized as follows:



```text

User Input

&#x20;   |

&#x20;   v

Deterministic Engineering Calculations

&#x20;   |

&#x20;   v

Engineering Results

&#x20;   |

&#x20;   +----> Independent Verification

&#x20;   |

&#x20;   v

Engineering Results Bridge

&#x20;   |

&#x20;   v

Gemini AI

&#x20;   |

&#x20;   v

Technical Explanation and Interpretation

```



This architecture gives each component a specific responsibility.



\### Deterministic calculation layer



Responsible for numerical engineering calculations.



\### Verification layer



Responsible for independent checking of selected calculations.



\### AI layer



Responsible primarily for:



\* Explanation

\* Interpretation

\* Context

\* Communication

\* Engineering reasoning



\---



\## 13. AI Development Philosophy



The project follows a human-in-the-loop engineering philosophy.



AI is used to improve accessibility and interpretation of engineering information while deterministic mathematical functions remain responsible for core numerical calculations.



This approach recognizes both the usefulness and limitations of generative AI in engineering applications.



The system therefore aims to combine:



\* Engineering equations

\* Deterministic computation

\* Independent verification

\* Data analysis

\* Artificial intelligence

\* Human engineering judgment



\---



\## 14. Future AI Improvements



Potential future improvements include:



\* Retrieval-augmented engineering references

\* Engineering standards integration

\* More extensive numerical verification

\* Uncertainty analysis

\* Automated engineering-report generation

\* Engineering calculation provenance tracking

\* Improved dataset interpretation

\* More advanced petroleum-engineering workflows

\* Domain-specific evaluation datasets

\* AI response quality benchmarking



These improvements would be implemented while maintaining the separation between deterministic engineering calculations and AI interpretation.



\---



\## 15. Conclusion



The AI Engineering Assistant is an integrated component of the FluidFlow Engineering Suite rather than the numerical calculation engine itself.



The project deliberately separates:



\*\*calculation → verification → interpretation\*\*



This architecture provides a more controlled approach to using generative AI in an engineering application.



The resulting system combines deterministic engineering computation, independent verification, engineering data analysis, and AI-assisted technical interpretation within a single Streamlit application.



