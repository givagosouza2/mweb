import streamlit as st
import inertial_file

def main():
    st.set_page_config(page_title="Momentum Web app", layout="wide")

    st.markdown(
        """
        <style>
        header[data-testid="stHeader"] {display: none;}
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
        }
        section.main > div {
            padding: 0rem !important;
        }
        html, body, [data-testid="stAppViewContainer"] {
            margin: 0 !important;
            padding: 0 !important;
        }
        .mw-banner img {
            width: 100vw !important;
            max-width: 100vw !important;
            height: auto !important;
            display: block !important;
        }
        .mw-banner {
            margin-left: calc(-50vw + 50%) !important;
            margin-right: calc(-50vw + 50%) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="mw-banner">', unsafe_allow_html=True)
    st.image("assets/banner_momentum_web.png", width='stretch')
    st.markdown("</div>", unsafe_allow_html=True)

    # Padding só para o conteúdo (menu e páginas)
    st.markdown('<div style="padding: 1rem 1rem 0 1rem;">', unsafe_allow_html=True)

    if "active_module" not in st.session_state:
        st.session_state.active_module = "home"

    col1, col2 = st.columns([0.4, 2])

    with col1:
        if st.button("Home", use_container_width=True):
            st.session_state.active_module = "home"
        if st.button("Sensor Inercial", use_container_width=True):
            st.session_state.active_module = "inertial_rec"

    with col2:
        if st.session_state.active_module == "home":
            st.info("Bem-vindo ao Momentum Web")
        elif st.session_state.active_module == "inertial_rec":
            inertial_file.render()

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
