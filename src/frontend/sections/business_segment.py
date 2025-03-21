import pandas as pd
import streamlit as st

from ...configs.config import logger
from ...utils.figures import plot_joint_distribution, plot_pie_chart

ORDER = [
    "BANCA PRIVADA",
    "PREMIUM PLUS",
    "PREMIUM",
    "INCLUSIÓN FINANCIERA",
    "CLÁSICO",
    "NO INFORMADO",
]


def plot_distribution(df, category, segment, figsize, title):
    try:
        fig = plot_joint_distribution(
            df[df["category"] == category],
            x="segmento_comercial",
            y="subcategory",
            x_order=ORDER,
            label_rotation=45,
            y_label="Causa Raíz",
            x_label="Segmento Comercial",
            top_y=10,
            title=title,
        )
        st.pyplot(fig)
    except Exception as e:
        logger.error(f"Error plotting {category}: {e}")
        # st.error(f"Error al graficar la categoría {category}")
        st.markdown(f"<div style='color: green; font-weight: bold;'>No hay datos disponibles sobre las categoría de {category} para graficar.</div>", unsafe_allow_html=True)
        

def segmento_comercial(df: pd.DataFrame, figsize: tuple = (400, 400)):
    st.title("Segmento comercial")
    with st.container():
        try:
            fig = plot_pie_chart(
                df,
                "segmento_comercial",
                2,
                n_colors=6,
                title="Segmento comercial",
                figsize=figsize,
                legend_y=-0.4,
            )
            st.plotly_chart(fig)
        except Exception as e:
            logger.error(f"Error plotting pie chart: {e}")
            st.error("Error al graficar los segmentos comerciales")


def map_segmento_comercial(df: pd.DataFrame):
    # st.subheader("Mapa Causa raiz - Segmento comercial")
    with st.container():
        #categories = ["Peticiones", "Quejas", "Reclamos"]
        categories = ["Quejas", "Reclamos"]
        for i, cat in enumerate(categories):
            # st.write(f"#### {cat} ")
            plot_distribution(df, cat, "segmento_comercial", figsize=(600, 600), title=cat)
            st.text("")  # Salto de línea
            st.text("")  # Salto de línea
            st.text("")  # Salto de línea
