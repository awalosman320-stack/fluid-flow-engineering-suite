"""Rock and Fluid Data Dashboard.

This Streamlit page allows users to upload engineering CSV data,
inspect summary statistics, filter samples, visualize porosity data,
and download the filtered dataset.
"""

import io

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Rock & Fluid Data Dashboard",
    page_icon="🪨",
    layout="wide",
)


st.title("🪨 Rock & Fluid Data Dashboard")

st.markdown(
    """
    Upload a CSV containing rock or fluid measurements.

    The dashboard provides:
    - Data preview
    - Summary statistics
    - Porosity filtering
    - Porosity distribution analysis
    - Porosity–permeability relationship
    - Filtered CSV download
    """
)


# =========================================================
# FILE UPLOAD
# =========================================================

st.header("1. Upload Engineering Data")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"],
    help=(
        "Upload a CSV containing numerical engineering data. "
        "For the visualization section, columns named Porosity "
        "and Permeability are required."
    ),
)


if uploaded_file is None:

    st.info(
        "Upload a CSV file to begin the rock and fluid data analysis."
    )

    st.markdown(
        """
        ### Recommended columns

        Your CSV can contain engineering measurements such as:

        - Porosity (%)
        - Permeability (mD)
        - Bulk Density (g/cm³)
        - Gamma Ray (API)
        - Water Saturation (%)
        """
    )

    st.stop()


# =========================================================
# LOAD DATA
# =========================================================

try:

    data = pd.read_csv(uploaded_file)

except Exception as error:

    st.error(
        f"Unable to read the CSV file: {error}"
    )

    st.stop()


if data.empty:

    st.warning(
        "The uploaded CSV contains no rows."
    )

    st.stop()


st.success(
    f"CSV loaded successfully: {len(data):,} rows "
    f"and {len(data.columns):,} columns."
)


# =========================================================
# DATA PREVIEW
# =========================================================

st.header("2. Data Preview")

st.dataframe(
    data,
    use_container_width=True,
    height=350,
)


# =========================================================
# SUMMARY STATISTICS
# =========================================================

st.header("3. Summary Statistics")

numeric_data = data.select_dtypes(
    include="number"
)


if numeric_data.empty:

    st.warning(
        "No numerical columns were detected in the uploaded file."
    )

else:

    summary_statistics = numeric_data.describe().T

    summary_statistics = summary_statistics[
        [
            "count",
            "mean",
            "std",
            "min",
            "25%",
            "50%",
            "75%",
            "max",
        ]
    ]

    summary_statistics.columns = [
        "Count",
        "Mean",
        "Std. Dev.",
        "Minimum",
        "25th Percentile",
        "Median",
        "75th Percentile",
        "Maximum",
    ]

    st.dataframe(
        summary_statistics.round(4),
        use_container_width=True,
    )


# =========================================================
# FILTERING
# =========================================================

st.header("4. Engineering Data Filtering")

porosity_columns = [
    column
    for column in data.columns
    if "porosity" in column.lower()
]


if not porosity_columns:

    st.warning(
        "No porosity column was detected. "
        "Filtering and porosity charts require a column "
        "whose name contains 'Porosity'."
    )

    filtered_data = data.copy()

else:

    porosity_column = st.selectbox(
        "Select the porosity column",
        porosity_columns,
    )

    numeric_porosity = pd.to_numeric(
        data[porosity_column],
        errors="coerce",
    )

    valid_porosity = numeric_porosity.dropna()


    if valid_porosity.empty:

        st.warning(
            "The selected porosity column contains no "
            "valid numerical values."
        )

        filtered_data = data.copy()

    else:

        minimum_porosity = float(
            valid_porosity.min()
        )

        maximum_porosity = float(
            valid_porosity.max()
        )

        if minimum_porosity == maximum_porosity:

            threshold = minimum_porosity

            st.info(
                "All valid porosity values are identical, "
                "so the filter threshold is fixed."
            )

        else:

            threshold = st.slider(
                "Show samples where porosity is greater than:",
                min_value=minimum_porosity,
                max_value=maximum_porosity,
                value=minimum_porosity,
                step=(
                    maximum_porosity
                    - minimum_porosity
                ) / 100,
            )


        filtered_data = data[
            numeric_porosity > threshold
        ].copy()


        filter_col1, filter_col2, filter_col3 = st.columns(3)

        filter_col1.metric(
            "Original Samples",
            f"{len(data):,}",
        )

        filter_col2.metric(
            "Filtered Samples",
            f"{len(filtered_data):,}",
        )

        filter_col3.metric(
            "Samples Removed",
            f"{len(data) - len(filtered_data):,}",
        )


st.subheader("Filtered Dataset")

st.dataframe(
    filtered_data,
    use_container_width=True,
    height=300,
)


# =========================================================
# CHART PREPARATION
# =========================================================

st.header("5. Engineering Visualizations")


# ---------------------------------------------------------
# POROSITY HISTOGRAM
# ---------------------------------------------------------

if porosity_columns:

    porosity_values = pd.to_numeric(
        data[porosity_column],
        errors="coerce",
    ).dropna()


    if not porosity_values.empty:

        st.subheader("Porosity Distribution")

        figure, axis = plt.subplots(
            figsize=(10, 5)
        )

        axis.hist(
            porosity_values,
            bins=15,
            edgecolor="black",
        )

        axis.set_xlabel(
            f"{porosity_column}"
        )

        axis.set_ylabel(
            "Number of Samples"
        )

        axis.set_title(
            "Porosity Distribution"
        )

        axis.grid(
            axis="y",
            alpha=0.25,
        )

        st.pyplot(
            figure,
            use_container_width=True,
        )

        plt.close(figure)

    else:

        st.warning(
            "A porosity histogram cannot be created because "
            "there are no valid numerical porosity values."
        )


# ---------------------------------------------------------
# POROSITY-PERMEABILITY CROSSPLOT
# ---------------------------------------------------------

permeability_columns = [
    column
    for column in data.columns
    if "permeability" in column.lower()
]


if porosity_columns and permeability_columns:

    permeability_column = st.selectbox(
        "Select the permeability column",
        permeability_columns,
    )

    plot_data = pd.DataFrame(
        {
            "Porosity": pd.to_numeric(
                data[porosity_column],
                errors="coerce",
            ),
            "Permeability": pd.to_numeric(
                data[permeability_column],
                errors="coerce",
            ),
        }
    ).dropna()


    if plot_data.empty:

        st.warning(
            "No valid numerical porosity-permeability "
            "pairs are available for plotting."
        )

    else:

        st.subheader(
            "Porosity–Permeability Crossplot"
        )

        figure, axis = plt.subplots(
            figsize=(10, 5)
        )

        axis.scatter(
            plot_data["Porosity"],
            plot_data["Permeability"],
            alpha=0.7,
        )

        axis.set_xlabel(
            f"{porosity_column}"
        )

        axis.set_ylabel(
            f"{permeability_column}"
        )

        axis.set_title(
            "Porosity vs Permeability"
        )

        axis.grid(
            True,
            alpha=0.25,
        )

        st.pyplot(
            figure,
            use_container_width=True,
        )

        plt.close(figure)

else:

    st.warning(
        "The porosity–permeability crossplot requires "
        "both a Porosity column and a Permeability column."
    )


# =========================================================
# DOWNLOAD FILTERED DATA
# =========================================================

st.header("6. Download Filtered Data")

csv_buffer = io.StringIO()

filtered_data.to_csv(
    csv_buffer,
    index=False,
)

csv_bytes = csv_buffer.getvalue().encode(
    "utf-8"
)


st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv_bytes,
    file_name="filtered_rock_fluid_data.csv",
    mime="text/csv",
)


st.caption(
    f"Download contains {len(filtered_data):,} samples."
)