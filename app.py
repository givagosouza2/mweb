import streamlit as st
import inertial_file


def main():
    st.set_page_config(page_title="Momentum Web app", layout="wide")

    # -------------------------
    # CSS (banner + layout + botões)
    # -------------------------
    st.markdown(
        """
        <style>
        /* Esconde header padrão */
        header[data-testid="stHeader"] { display: none; }

        /* Remove padding/margens do container para permitir banner full-bleed */
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

        /* Banner full-bleed */
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

        /* Padding do conteúdo abaixo do banner */
        .mw-content {
            padding: 1rem 1rem 0 1rem;
        }

        /* -----------------------------
           BOTÕES MOMENTUM (card-style)
           ----------------------------- */
        .mw-btn-wrap div.stButton > button {
            width: 100%;
            background: #ffffff;
            color: #c00000;              /* vermelho */
            border: 2px solid #1f4aff;   /* azul */
            border-radius: 12px;
            padding: 0.75rem 0.9rem;
            font-size: 1.0rem;
            font-weight: 700;
            text-align: left;            /* estilo “menu” */
            transition: all 0.18s ease-in-out;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        }

        .mw-btn-wrap div.stButton > button:hover {
            background: #f5f7ff;
            color: #a00000;
            border-color: #1638c9;
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.10);
        }

        .mw-btn-wrap div.stButton > button:active {
            transform: translateY(0px);
            background: #eef2ff;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        }

        .mw-btn-wrap div.stButton > button:focus {
            outline: none;
            box-shadow: 0 0 0 3px rgba(31, 74, 255, 0.25);
        }

        /* Botão ativo (destacado) */
        .mw-btn-wrap[data-active="true"] div.stButton > button {
            background: #1f4aff;
            color: #ffffff;
            border-color: #1f4aff;
            box-shadow: 0 8px 20px rgba(31, 74, 255, 0.25);
        }

        .mw-btn-wrap[data-active="true"] div.stButton > button:hover {
            background: #1638c9;
            border-color: #1638c9;
        }

        /* Título/área lateral */
        .mw-side-title {
            font-weight: 800;
            margin: 0.25rem 0 0.75rem 0;
            font-size: 1.05rem;
        }

        /* Caixa do menu (opcional) */
        .mw-menu-card {
            background: rgba(255,255,255,0.75);
            border: 1px solid rgba(0,0,0,0.06);
            border-radius: 14px;
            padding: 0.8rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # -------------------------
    # Banner
    # -------------------------
    st.markdown('<div class="mw-banner">', unsafe_allow_html=True)
    st.image("mwebv2.png", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------
    # Conteúdo (com padding)
    # -------------------------
    st.markdown('<div class="mw-content">', unsafe_allow_html=True)

    if "active_module" not in st.session_state:
        st.session_state.active_module = "home"

    col1, col2 = st.columns([0.55, 2.0], gap="large")

    # -------------------------
    # Menu lateral
    # -------------------------
    with col1:
        st.markdown('<div class="mw-menu-card">', unsafe_allow_html=True)
        st.markdown('<div class="mw-side-title">Menu</div>', unsafe_allow_html=True)

        # HOME
        is_active = (st.session_state.active_module == "home")
        st.markdown(f'<div class="mw-btn-wrap" data-active="{str(is_active).lower()}">', unsafe_allow_html=True)
        if st.button("🏠 Home", use_container_width=True, key="btn_home"):
            st.session_state.active_module = "home"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # SENSOR INERCIAL
        is_active = (st.session_state.active_module == "inertial_rec")
        st.markdown(f'<div class="mw-btn-wrap" data-active="{str(is_active).lower()}">', unsafe_allow_html=True)
        if st.button("📱 Sensor Inercial", use_container_width=True, key="btn_inertial"):
            st.session_state.active_module = "inertial_rec"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------
    # Área principal
    # -------------------------
    with col2:
        if st.session_state.active_module == "home":
            st.markdown("### Bem-vindo ao Momentum Web")
            st.info("Selecione um módulo no menu à esquerda para começar.")

            st.markdown(
                """
                **Momentum Web** é uma aplicação web para análise de registros do **Momentum Sensors**.
                
                - Upload de arquivos do smartphone
                - Visualização de sinais
                - Processamento leve (mobile-friendly)
                """
            )

        elif st.session_state.active_module == "inertial_rec":
            inertial_file.render()

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
