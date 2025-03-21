import pandas as pd
import streamlit as st
from ...orchestration.run_model import root_flow


def page_process():
    # Estilos CSS personalizados
    st.markdown(
        """
        <style>
            .main {
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            }
            .stButton button {
                background-color: #773dbd;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
                border-radius: 8px;
            }
            .stButton button:hover {
                background-color: white;
                color: #773dbd;
                border: 2px solid #773dbd;
            }
            .stSelectbox, .stFileUploader {
                margin-top: 20px;
            }
            .stFileUploader div[role="button"] {
                background-color: #773dbd !important;
                color: white !important;
                border-radius: 10px;
                padding: 10px;
                border: 2px dashed white;
            }
            .stFileUploader div[role="button"]:hover {
                background-color: #5b2e94 !important;
            }
            .stSelectbox div[role="combobox"] {
                background-color: #773dbd !important;
                color: white !important;
                border-radius: 10px;
                padding: 10px;
            }
            .stSelectbox div[role="combobox"]::after {
                border: none;
            }
            .stSelectbox div[role="combobox"]:hover {
                background-color: #5b2e94 !important;
            }
            .highlight {
                color: #773dbd;
                font-weight: bold;
            }
            .title {
                color: #773dbd;
                font-size: 2em;
                font-weight: bold;
            }
            .description {
                font-size: 1.2em;
                margin-bottom: 20px;
            }
            .footer {
                text-align: center;
                margin-top: 100px;
                color: #888;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.subheader('Procesamiento de Datos')

    st.markdown( "Por favor, carga un archivo en formato **Excel** y selecciona el ***tipo de base de datos*** y el ***mes*** que deseas procesar.")

    with st.container():
        col1, col2 = st.columns([3, 2], gap="large")

        with col1:
            file_ = st.file_uploader("Cargar archivo", type="xlsx")
            if file_ is not None:
                df_raw = pd.read_excel(file_)
                st.success("Archivo cargado con éxito")

        with col2:
            btn_select = st.selectbox(
                "Seleccionar tipo de base", ["Empresas", "No Fraude", "Fraude"]
            )
            btn_select_mes = st.selectbox(
                "Seleccionar el mes a procesar", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            )

        if file_ is not None and btn_select is not None and btn_select_mes is not None:
            btn = st.button("Procesar base", key="process_button")
            if btn:
                with st.spinner("Procesando..."):
                    _, file_path = root_flow(
                        base=btn_select.lower().replace(" ", "_"), mes=btn_select_mes.lower(), df=df_raw
                    )
                    st.success(
                        f"Procesamiento finalizado. el archivo se guardó en {file_path}"
                    )

    st.markdown(
        '<div class="footer">© 2024 emergia - Todos los derechos reservados.</div>',
        unsafe_allow_html=True,
    )
