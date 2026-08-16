\# FluidFlow Engineering Suite



\## Engineering Calculation, Verification, Data Analysis \& AI Interpretation Platform



FluidFlow Engineering Suite is a Streamlit-based engineering application designed to combine \*\*deterministic engineering calculations\*\*, \*\*engineering data analysis\*\*, \*\*independent verification\*\*, and \*\*AI-assisted technical interpretation\*\* in one platform.



The application is designed around an important engineering principle:



> \*\*Numerical engineering results should come from deterministic calculation functions, while AI is primarily used to explain and interpret those verified results.\*\*



This separation reduces the risk of unsupported AI-generated engineering calculations.



\---



\## 1. Core Capabilities



\### Pipe Flow Analyser



The Pipe Flow Analyser performs engineering calculations including:



\* Volumetric flow rate

\* Pipe velocity

\* Reynolds number

\* Flow-regime classification

\* Darcy friction factor

\* Pressure drop

\* Pipe roughness effects



The calculations are implemented using deterministic Python functions.



\### Heat Transfer Calculator



The Heat Transfer module provides:



\* Steady-state conduction calculations

\* Fourier's law heat-transfer calculations

\* Cooling-time estimation

\* Transient cooling-temperature calculations

\* Independent temperature verification

\* Verification-error reporting



\### Rock \& Fluid Data Dashboard



The data-analysis module allows users to:



\* Upload engineering CSV datasets

\* Preview uploaded data

\* Identify numerical columns

\* Generate summary statistics

\* Filter data using porosity

\* Visualize porosity distributions

\* Analyze porosity-permeability relationships

\* Download filtered datasets



\### AI Engineering Assistant



The AI Engineering Assistant uses Google's Gemini API to provide engineering explanations and interpretation.



Its engineering domains include:



\* Fluid mechanics

\* Pipe-flow engineering

\* Heat transfer

\* Petroleum engineering

\* Rock and fluid fundamentals



The assistant can receive verified results from the engineering modules and use them as context when answering engineering questions.



\---



\## 2. Numerical Integrity Architecture



FluidFlow deliberately separates \*\*calculation\*\* from \*\*AI interpretation\*\*.



\### Deterministic calculation layer



Engineering calculations are performed by Python functions in the application.



Examples include:



\* Reynolds number

\* Velocity

\* Friction factor

\* Pressure drop

\* Conduction heat-transfer rate

\* Cooling time

\* Cooling temperature



These functions do not depend on Gemini to produce their numerical results.



\### Verification layer



Independent verification functions are provided for selected calculations.



For example, turbulent pipe-flow friction factors can be independently evaluated using the Colebrook-White equation.



The application can compare calculated and independently verified friction factors using absolute and percentage differences.



\### AI interpretation layer



Gemini receives verified engineering results through the application's engineering-results bridge.



The AI is instructed to:



\* Treat supplied numerical results as authoritative

\* Explain physical meaning

\* Discuss engineering assumptions

\* Explain equations

\* Provide engineering context

\* Avoid inventing numerical results

\* Distinguish calculated results from AI interpretation



\---



\## 3. Engineering Results Bridge



The application currently connects verified results from three modules to the AI Engineering Assistant.



\### Pipe Flow → AI



The assistant can receive:



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



\### Heat Transfer → AI



The assistant can receive:



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



\### Rock \& Fluid Data → AI



The assistant can receive:



\* Dataset row count

\* Number of numerical columns

\* Dataset-derived summary statistics



The AI is explicitly instructed to interpret these values rather than replace the deterministic calculation engine.



\---



\## 4. Project Structure



```text

FLUID\_FLOW\_ENGINEERING\_SUITE/

│

├── app.py

├── engineering.py

├── calculations.py

├── heat\_transfer.py

├── validation.py

├── ai\_assistant.py

│

├── pages/

│   ├── 1\_Pipe\_Flow\_Analyser.py

│   ├── 2\_Heat\_Transfer\_Calculator.py

│   ├── 3\_Rock\_Fluid\_Data\_Dashboard.py

│   └── 4\_AI\_Engineering\_Assistant.py

│

├── data/

│

├── backups/

│

├── docs/

│   └── ai\_usage.md

│

├── tests/

│   └── test\_engineering\_calculations.py

│

├── sample\_rock\_data.csv

├── requirements.txt

├── README.md

└── .gitignore

```



\---



\## 5. Object-Oriented Engineering Components



The project includes engineering classes in `engineering.py`.



\### Fluid



Represents physical properties of a working fluid:



\* Name

\* Density

\* Dynamic viscosity



\### Pipe



Represents circular pipe geometry:



\* Diameter

\* Length

\* Absolute roughness



The class also provides the pipe's internal cross-sectional area.



\### HeatTransferWall



Represents a flat wall used for conduction calculations:



\* Thickness

\* Area

\* Thermal conductivity



Input validation is performed when engineering objects are created.



\---



\## 6. Engineering Calculation Modules



\### `calculations.py`



Contains deterministic pipe-flow calculations including:



```text

calculate\_velocity()

calculate\_reynolds\_number()

determine\_flow\_regime()

calculate\_friction\_factor()

calculate\_pressure\_drop()

calculate\_pipe\_flow()

```



\### `heat\_transfer.py`



Contains deterministic heat-transfer calculations including:



```text

calculate\_conduction\_heat\_rate()

calculate\_cooling\_time()

cooling\_temperature()

```



\### `validation.py`



Contains independent verification functions including:



```text

colebrook\_friction\_factor()

compare\_friction\_factors()

```



\---



\## 7. Automated Testing



The project includes an automated test suite using `pytest`.



The test suite covers:



\* Velocity calculation

\* Reynolds number

\* Laminar flow classification

\* Turbulent flow classification

\* Laminar friction factor

\* Pressure-drop calculation

\* Complete pipe-flow calculation

\* Colebrook friction factor

\* Friction-factor comparison

\* Conduction heat-transfer rate

\* Cooling-time calculation

\* Cooling-temperature calculation



Current test status:



```text

12 passed

```



Run the tests with:



```bash

python -m pytest tests -v

```



\---



\## 8. Installation



\### Clone the repository



```bash

git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

cd FLUID\_FLOW\_ENGINEERING\_SUITE

```



\### Create a virtual environment



Windows:



```cmd

python -m venv .venv

```



Activate it:



```cmd

.venv\\Scripts\\activate

```



\### Install dependencies



```cmd

python -m pip install -r requirements.txt

```



\---



\## 9. Gemini API Configuration



The AI Engineering Assistant requires a Gemini API key.



The application expects the following environment variable:



```text

GEMINI\_API\_KEY

```



\### Windows Command Prompt



Set the variable for the current terminal session:



```cmd

set GEMINI\_API\_KEY=YOUR\_API\_KEY

```



Then start Streamlit from the same terminal.



For permanent environment configuration, use Windows Environment Variables rather than placing the API key directly inside Python source code.



\*\*Never commit API keys, passwords, or credentials to GitHub.\*\*



\---



\## 10. Running the Application Locally



Activate the virtual environment:



```cmd

.venv\\Scripts\\activate

```



Then run:



```cmd

streamlit run app.py

```



Streamlit will provide a local URL, normally:



```text

http://localhost:8501

```



Keep the terminal running while using the local application.



\---



\## 11. Technology Stack



\### Application



\* Python

\* Streamlit



\### Scientific Computing



\* NumPy

\* SciPy



\### Data Analysis



\* Pandas



\### Visualization



\* Matplotlib

\* Plotly



\### Artificial Intelligence



\* Google Gemini

\* Google GenAI Python SDK



\### Testing



\* Pytest



\### Version Control



\* Git

\* GitHub



\---



\## 12. Dependencies



The runtime dependencies are maintained in:



```text

requirements.txt

```



Current direct dependencies include:



```text

streamlit==1.61.1

pandas==3.0.5

numpy==2.5.2

scipy==1.18.0

matplotlib==3.11.1

plotly==6.9.0

google-genai==2.18.1

```



\---



\## 13. AI Development and Verification



The AI Engineering Assistant was developed using an explicit separation between deterministic engineering computation and AI interpretation.



Three major AI development objectives were addressed:



\### Prompt 1 — Engineering reasoning



The assistant was configured for:



\* Petroleum engineering

\* Fluid mechanics

\* Thermal engineering

\* Rock/fluid fundamentals



Engineering assumptions and terminology were explicitly defined.



\### Prompt 2 — Numerical integrity



The assistant was instructed that numerical engineering results should originate from deterministic calculation functions whenever possible.



Verified results are passed to Gemini as engineering context.



\### Prompt 3 — Engineering communication



The assistant was configured to provide:



\* Equations

\* Units

\* Assumptions

\* Physical interpretation

\* Professional engineering explanations



Further AI-development details are documented in:



```text

docs/ai\_usage.md

```



\---



\## 14. Engineering Safety and Limitations



FluidFlow Engineering Suite is an engineering education, analysis, and decision-support application.



Results depend on:



\* Input quality

\* Engineering assumptions

\* Model validity

\* Fluid properties

\* Geometry

\* Boundary conditions

\* Applicable correlations



The application should not be treated as a substitute for professional engineering design review, applicable codes and standards, laboratory measurements, or field validation.



AI-generated explanations should also be reviewed by a qualified engineer when used for real engineering decisions.



\---



\## 15. Version Control



The project uses Git for version control.



Development checkpoints include separate commits for:



\* Initial AI integration

\* Pipe Flow → AI integration

\* Heat Transfer → AI integration

\* Rock \& Fluid → AI integration

\* Calculation test suite

\* Runtime dependencies



This provides a traceable development history and allows earlier versions to be recovered when necessary.



\---



\## 16. Backup Strategy



Important engineering pages are backed up under:



```text

backups/

```



These backups provide recovery points before major AI integration changes.



\---



\## 17. Deployment



The application is designed for deployment using Streamlit Community Cloud.



The deployment process requires:



1\. A GitHub repository

2\. `app.py` as the application entry point

3\. `requirements.txt`

4\. A configured Gemini API secret

5\. The repository connected to Streamlit Community Cloud



The Gemini API key should be configured through the deployment platform's secret-management system rather than committed to the repository.



\---



\## 18. Development Status



Current major components:



| Component                  | Status      |

| -------------------------- | ----------- |

| Pipe Flow Analyser         | Complete    |

| Heat Transfer Calculator   | Complete    |

| Rock \& Fluid Dashboard     | Complete    |

| AI Engineering Assistant   | Complete    |

| Pipe Flow AI Bridge        | Complete    |

| Heat Transfer AI Bridge    | Complete    |

| Rock \& Fluid AI Bridge     | Complete    |

| Engineering OOP layer      | Complete    |

| Calculation validation     | Complete    |

| Automated tests            | Complete    |

| Runtime dependencies       | Complete    |

| README documentation       | In progress |

| GitHub deployment          | Pending     |

| Streamlit Cloud deployment | Pending     |



\---



\## 19. Author



\*\*FluidFlow Engineering Suite\*\*



Engineering-focused software combining deterministic computational methods, verification, data analysis, and AI-assisted engineering interpretation.



