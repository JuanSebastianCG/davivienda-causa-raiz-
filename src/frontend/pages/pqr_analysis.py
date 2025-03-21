import streamlit as st
from ..sections.business_segment import map_segmento_comercial
from ..sections.general_categories import subcategories_pqr
from ..sections.product import map_producto
from ..sections.temporality import temporality_pqr


def page_pqr_analysis(df):
    
    col3, col4 = st.columns(2)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            subcategories_pqr(df, 98)
        with col2:
            temporality_pqr(df, 98)
            
    st.markdown("---")
    st.subheader("Mapa Producto -  Segmento comercial")

    with st.container():
        col3, col4 = st.columns(2)
        with col3:
            map_producto(df)
        with col4:
            map_segmento_comercial(df)
    st.markdown("---")
    """    
    with col1:
        subcategories_pqr(df, 98)
        st.markdown("---")
        st.subheader("Mapa Producto -  Segmento comercial")
        map_producto(df)
        st.markdown("---")
    with col2:
        temporality_pqr(df, 98)
        st.markdown("---")
        st.subheader("")
        map_segmento_comercial(df)
        st.markdown("---")
    """