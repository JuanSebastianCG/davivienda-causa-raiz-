import logging
import sys

import pandas as pd
import streamlit as st

from ...utils.figures import plot_bar_percentage, plot_pie_chart

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

sys.path.append("../../utils")


def general_section(df: pd.DataFrame, percentage: float, figsize: tuple = (600, 600)):
    with st.container():
        st.header("Categorización General de PQR", anchor="general_section")
        col1, col2 = st.columns([1, 2])
        with col1:
            try:
                fig = plot_pie_chart(df, "category", percentage, figsize=figsize)
                st.plotly_chart(fig)
            except Exception as e:
                logger.error(f"Error: {e}")
                st.error("No se pudo graficar la causa raíz. Verifique los datos.")

        with col2:
            st.markdown("#### **Tabla de Descripción de PQRs**")
            try:
                st.dataframe(
                    df[
                        ["descripcion", "category", "producto_", "segmento_comercial"]
                    ].head(100)
                )
            except Exception as e:
                logger.error(f"Error: {e}")
                st.error("No se pudo mostrar la tabla. Verifique los datos.")


def subcategories_section(
    df: pd.DataFrame,
    percentage: float,
    figsize: tuple = (600, 600),
    title: str = "Causas Raíz Identificadas",
):
    with st.container():
        st.title(title, anchor="subcategories_section")

        # Calculate subcategory percentages and sort by counts
        subcategory_counts = df["subcategory"].value_counts()
        subcategory_percentages = (subcategory_counts / subcategory_counts.sum() * 100).sort_values(ascending=False)
        cumulative_percentages = subcategory_percentages.cumsum()

        # Find subcategories making up to the given percentage of total data
        significant_subcategories = subcategory_percentages[cumulative_percentages <= percentage]
        significant_subcategory_names = significant_subcategories.index.tolist()

        # Total and significant subcategories counts
        total_subcategories = subcategory_counts.count()
        significant_count = significant_subcategories.count() - 4

        # Top 3 subcategories
        top_three_subcategories = subcategory_percentages.head(5).index.tolist()

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(
                f"""
                <div style='background-color:#F0F2F6; padding: 15px; border-radius: 10px;'>
                    <h4 style='color: #773dbd; margin: 0;'>Detalles de Categorización</h4>
                    <p style='margin: 0;'>Total de Causas: <b>{total_subcategories}</b></p>
                    <p style='margin: 0;'>Causas al {percentage}%: <b>{significant_count}</b></p>
                    <p style='margin: 0;'>Principales Causas: <b>{', '.join(top_three_subcategories)}</b></p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            try:
                fig = plot_bar_percentage(
                    df[df["subcategory"].isin(significant_subcategory_names)],
                    "subcategory",
                    title=title,
                    percentage=percentage,
                )
                st.plotly_chart(fig)
            except Exception as e:
                logger.error(f"Error: {e}")
                st.error("No se pudo graficar las subcategorías. Verifique los datos.")


def subcategories_pqr(df, percentage):
    with st.container():
        # categories = ["Peticiones", "Quejas", "Reclamos"]
        categories = ["Quejas", "Reclamos"]
        for i, cat in enumerate(categories):
            # st.subheader(cat)
            try:
                if df[df["category"] == cat].empty:
                    logger.error(f"Error: {e}")  # noqa: F821
                    st.error("Error al graficar la distribución temporal")
                else:
                    fig = plot_bar_percentage(
                        df[df["category"] == cat],
                        "subcategory",
                        title=cat,
                        percentage=percentage,
                    )
                    st.plotly_chart(fig)
            except Exception as e:
                logger.error(f"Error: {e}")
                # st.error(f"No se pudo graficar las subcategorías de {cat}. Verifique los datos.")
                st.markdown(f"<div style='color: green; font-weight: bold;'>No hay datos disponibles sobre las subcategorías de {cat} para graficar.</div>", unsafe_allow_html=True)
                
