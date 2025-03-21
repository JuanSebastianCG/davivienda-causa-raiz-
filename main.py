import streamlit as st
from streamlit_option_menu import option_menu
from src.frontend.pages.process_base import page_process
from src.frontend.pages.general_analysis import page_rootcauses, load_file
from src.frontend.pages.pqr_analysis import page_pqr_analysis

st.set_page_config(page_title="Davivienda Causa Raíz", layout="wide")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .css-18e3th9 {padding-top: 0rem;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def interface():
    st.markdown(
        """
        <style>
            /* Estilo para los tabs */
            .st-eb .stTab {
                background-color: #773dbd !important;
                color: white !important;
                border-radius: 10px 10px 0 0 !important;
                margin-right: 4px !important;
                padding: 12px 12px !important;
                font-size: 16px !important;
                font-weight: bold !important;
                display: flex;
                align-items: center;
            }

            /* Estilo para el tab activo */
            .st-eb .stTab.stTabActive {
                background-color: #5b2e94 !important;
            }

            /* Estilo para el icono dentro del tab */
            .st-eb .stTab .icon {
                margin-right: 8px;
            }

            .block-container
            {
                padding-top: 0rem;
                padding-bottom: 0rem;
                margin-top: 0.5rem;
            }
            .footer {
                position: fixed;        
                bottom: 0;              
                width: 100%;            
                text-align: center;     
                padding: -10px 10px;        
                color: #888;            
                background-color: #fff; 
                border-top: 1px solid #ddd; 
            }
        </style>
    """,
        unsafe_allow_html=True,
    )
    css = """
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:1.25rem;
        }
    </style>
    """  # noqa: F841
       
    if st.session_state.get('switch_button', False):
        st.session_state['menu_option'] = (st.session_state.get('menu_option', 0) + 1) % 3
        manual_select = st.session_state['menu_option']
    else:
        manual_select = None

    # Verificar si el df ya existe en session_state
    if 'df' not in st.session_state:
        st.session_state['df'] = None  # Inicializar df si no existe
        st.session_state['file_name'] = None

    selected3 = option_menu(
        menu_title=None,
        options=["Procesar base", "Análisis de Causa Raíz", "PQRs"],
        icons=["upload", "bar-chart", "list-task"],
        orientation="horizontal",
        manual_select=manual_select,
        key='menu_4',
        styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        
        "nav-link": {"font-size": "18px"},
        "nav-link-selected": {"background-color": "#773dbd"},
    }
    )    

    if selected3 == "Procesar base":
        path_file_proccesed = page_process()  # noqa: F841
    
    elif selected3 == "Análisis de Causa Raíz":
        
        df, file_name = load_file()
        
        if df is not None:
             # Guardamos el df en session_state
            st.session_state['df'] = df
            st.session_state['file_name'] = file_name
            page_rootcauses(st.session_state['df'],st.session_state['file_name'])
            df = None
            file_name = None            

        elif st.session_state['df'] is not None:
            page_rootcauses(st.session_state['df'],st.session_state['file_name'])

        
        st.markdown(
            '<div class="footer">© 2024 emergia - Todos los derechos reservados.</div>',
            unsafe_allow_html=True,
        )

    elif selected3 == "PQRs":
        if st.session_state['df'] is not None:
            page_pqr_analysis(st.session_state['df'])
            df = None
        else:
            st.warning("Por favor, cargue un documento en la sección de Análisis de Causa Raíz.")

        st.markdown(
        '<div class="footer">© 2024 emergia - Todos los derechos reservados.</div>',
        unsafe_allow_html=True,
    )

    aa = """
    st.markdown(css, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Procesar base", "Análisis de Causa Raíz", "PQRs"])

    with tab1:
        path_file_proccesed = page_process()

    with tab2:
        df = page_rootcauses()

    with tab3:
        if df is not None:
            page_pqr_analysis(df)
    """ # noqa: F841

if __name__ == "__main__":
    interface()
