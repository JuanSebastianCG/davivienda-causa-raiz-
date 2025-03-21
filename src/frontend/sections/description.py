# import sys
import pandas as pd
import streamlit as st

def description(df: pd.DataFrame, file_name:str):
    st.title("Análisis de Causa Raíz")
    st.markdown(
                f"""
                    <div style='background-color:#F0F2F6; padding: 15px; border-radius: 10px;margin-bottom: 20px; display: inline-block; '>
                        <p style='margin: 0; '>Archivo cargado: <b>{file_name}</b></p>
                    </div>
                    """,
                unsafe_allow_html=True,
            )

    # Display an introductory summary if data is loaded
    if "df" in locals():
        num_records = df.shape[0]
        num_columns = df.shape[1]

        col1, col2, col3 = st.columns([2, 1, 1])  # Adjusting for an additional column
        with col1:
            st.markdown(
                f"""
                    <div style='background-color:#F0F2F6; padding: 15px; border-radius: 10px;'>
                        <h4 style='color: #773dbd; margin: 0;'>Datos Procesados</h4>
                        <p style='margin: 0;'>Registros: <b>{num_records}</b></p>
                        <p style='margin: 0;'>Columnas: <b>{num_columns}</b></p>
                    </div>
                    """,
                unsafe_allow_html=True,
            )
        # with col2:
        #     st.markdown(
        #         """
        #             <div style='background-color:#773dbd; padding: 15px; border-radius: 10px;'>
        #                 <h2 style='color: white; text-align: center;'>80%</h2>
        #                 <p style='color: white; text-align: center; margin-top: -10px;'>Acierto Detección</p>
        #             </div>
        #             """,
        #         unsafe_allow_html=True,
        #     )
        # with col3:
        #     st.markdown(
        #         """
        #             <div style='background-color:#FFFFFF; padding: 15px; border-radius: 10px;'>
        #                 <p style='color: black; text-align: justify;'>
        #                     El acierto se calcula basado en el número de causas detectadas que coinciden con el árbol de tipificación proporcionado al modelo. 
        #                 </p>
        #             </div>
        #             """,
        #         unsafe_allow_html=True,
        #     )
