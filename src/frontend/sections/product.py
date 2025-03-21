import streamlit as st

from ...configs.config import logger
from ...utils.figures import plot_joint_distribution, plot_pie_chart

CATEGORY_ORDER = [
    "BANCA PRIVADA",
    "PREMIUM PLUS",
    "PREMIUM",
    "INCLUSIÓN FINANCIERA",
    "CLÁSICO",
    "NO INFORMADO",
]


def product_section(df, figsize=(600, 350)):
    st.title("Productos más frecuentes")
    with st.container():
        # col1, col2 = st.columns(2)
        # with col1:
        try:
            fig = plot_pie_chart(
                df,
                "producto_",
                2,
                n_colors=6,
                title="Producto",
                figsize=figsize,
                legend_x= 1.1,
                legend_y= 0.1,
            )
            st.plotly_chart(fig)
        except Exception as e:
            logger.error(f"Error plotting pie chart: {e}")
            st.error("Error al graficar los productos")


def plot_distribution(df, category, figsize=(600, 600), title=None):
    try:
        fig = plot_joint_distribution(
            df[df["category"] == category],
            x="producto_",
            y="subcategory",
            label_rotation=45,
            y_label="Causa Raíz",
            x_label="Producto",
            top_y=10,
            top_x=10,
            title=title,
        )
        st.pyplot(fig)
    except Exception as e:
        logger.error(f"Error plotting {category}: {e}")
        # st.error(f"Error al graficar la categoría {category}")
        st.markdown(f"<div style='color: green; font-weight: bold;'>No hay datos disponibles sobre las categoría de {category} para graficar.</div>", unsafe_allow_html=True)
        


def map_producto(df):
    # st.title("Mapa de segmento comercial")
    with st.container():
        #for idx, category in enumerate(["Peticiones", "Quejas", "Reclamos"]):
        for idx, category in enumerate(["Quejas", "Reclamos"]):
            # st.write(f"#### {category}")
            plot_distribution(df, category, title=category)
