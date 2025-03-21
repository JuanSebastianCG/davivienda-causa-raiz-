import pandas as pd
import streamlit as st

from ...utils.figures import convert_columns_names, process_product_column


def load_and_process_data(uploaded_file):
    df = pd.read_excel(uploaded_file)
    df = convert_columns_names(df)
    df = process_product_column(df)
    return df


def slidebar():
    with st.sidebar:
        uploaded_file = st.file_uploader(
            "Cargar archivo XLSX", type="xlsx", label_visibility="collapsed"
        )
        if uploaded_file is not None:
            df = load_and_process_data(uploaded_file)
            return df
        else:
            return None
