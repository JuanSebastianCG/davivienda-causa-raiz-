import logging
import pandas as pd
import streamlit as st
from ...utils.figures import plot_line_weekday

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def temporality_section(
    df: pd.DataFrame, percentage: float, figsize: tuple = (600, 600)
):
    st.title("Temporalidad de PQRs")
    container = st.container()
    with container:
        col1, col2 = st.columns([2, 1])
        with col1:
            try:
                fig = plot_line_weekday(df, title="", threshold=percentage)
                st.plotly_chart(fig)
            except Exception as e:
                logger.error(f"Error: {e}")
                # st.error("Error al graficar la distribución temporal")
                st.markdown("<div style='color: green; font-weight: bold;'>No hay datos disponibles sobre el tema para graficar.</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(
                """
            <div style='background-color:#F0F2F6; padding: 15px; border-radius: 10px;'>
                <h4 style='color: #773dbd;'>Análisis de Picos</h4>
                """,
                unsafe_allow_html=True,
            )
            # Calculate peaks in data
            daily_totals = df.groupby(df["fecha_apertura"].dt.day)[
                "subcategory"
            ].count()
            top_days = daily_totals.nlargest(3).index.tolist()
            peak_info = "<ul>"
            for day in top_days:
                subcategories = (
                    df[df["fecha_apertura"].dt.day == day]["subcategory"]
                    .value_counts()
                    .head(3)
                    .to_dict()
                )
                peak_info += f"<li>Día {day}: Top Causas - {', '.join([f'{k} ({v})' for k, v in subcategories.items()])}</li>"
            peak_info += "</ul></div>"

            st.markdown(peak_info, unsafe_allow_html=True)


def temporality_pqr(df, percentage):
    container = st.container()
    with container:
        #for cat in ["Peticiones", "Quejas", "Reclamos"]:
        for cat in ["Quejas", "Reclamos"]:
            try:
                aa = df["category"] == cat
                print(aa.value_counts())
                if df[df["category"] == cat].empty:
                    logger.error(f"Error: {e}")  # noqa: F821
                    # st.error("Error al graficar la distribución temporal")
                    st.markdown("<div style='color: green; font-weight: bold;'>No hay datos disponibles sobre el tema para graficar.</div>", unsafe_allow_html=True)
                else:
                    fig = plot_line_weekday(
                        df[df["category"] == cat],
                        title=cat,
                        threshold=percentage,
                    )
                    st.plotly_chart(fig)
            except Exception as e:
                logger.error(f"Error: {e}")
                # st.error("Error al graficar la distribución temporal")
                st.markdown("<div style='color: green; font-weight: bold;'>No hay datos disponibles sobre el tema para graficar.</div>", unsafe_allow_html=True)

