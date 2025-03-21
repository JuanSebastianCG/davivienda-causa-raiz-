import os
import pandas as pd
import streamlit as st
from ...utils.figures import convert_columns_names, process_product_column
from ..sections.business_segment import segmento_comercial
from ..sections.description import description
from ..sections.general_categories import general_section, subcategories_section
from ..sections.product import product_section
from ..sections.temporality import temporality_section


def load_file():
    st.subheader("Análisis general")
    st.markdown("Por favor, cargue o seleccione un archivo en formato **Excel** para continuar. Asegúrese de que el archivo esté en el formato **.xlsx.**")
    col1, col2 = st.columns(2)
    with col1:
        df = st.file_uploader("Cargar archivo", type=["csv", "xlsx"])
        if df is not None:
            df = pd.read_excel(df)
            file_name = df.Name
            st.success("Archivo cargado con éxito")
            return df, file_name
    with col2:
        df_path = st.selectbox("Seleccionar archivo", [None] + os.listdir("./results"))
        if df_path is not None:
            df = pd.read_excel(f"./results/{df_path}")
            st.success("Archivo cargado con éxito")
        return df, df_path
    return None, None

def page_rootcauses(df, file_name): 
    if df is not None:
        df = convert_columns_names(df)
        df = process_product_column(df)

        st.markdown("---")
        description(df, file_name)
        st.markdown("---")
        general_section(df, 1, figsize=(400, 400))
        st.markdown("---")
        subcategories_section(df, 98, figsize=(400, 400))
        st.markdown("---")
        temporality_section(df, 98, figsize=(400, 400))
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            segmento_comercial(df)
        with col2:
            product_section(df)
        st.markdown("---")
    else:
        print('None')
    return df
