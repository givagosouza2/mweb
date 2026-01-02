import streamlit as st
import inertial_file
# Módulos futuros (criar depois)
# import static_balance
# import tug_test
# import gait_4m
# import finger_tapping
# import hand_tremor
# import jump_test
# import y_test


def main():
    st.set_page_config(page_title="Momentum Web app", layout="wide")

    # =========================
    # CSS (layout + botões)
    # =========================
    st.markdown(
        """
        <style>
        header[data-testid="stHeader"] { display: none; }

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

        .mw-content {
            padding: 1rem 1rem 0 1rem;
        }

        /* BOTÕES */
        .mw-btn-wrap div.stButton > button {
            width: 100%;
            background: #ffffff;
            color: #c00000;
            border: 2px solid #1f4aff;
            border-radius: 12px;
            padding: 0.7rem 0.9rem;
            font-size: 0.95rem;
            font-weight: 700;
            text-align: left;
            transition: all 0.18s ease-in-out;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
            margin-bottom: 0.4rem;
        }

        .mw-btn-wrap div.stButton > button:hover {
            background: #f5f7ff;
            color: #a00000;
            border-color: #1638c9;
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.10);
        }

        .mw-btn-wrap[data-active="true"] div.stButton > button {
            background: #1f4aff;
            color: #ffffff;
            border-color: #1f4aff;
            box-shadow: 0 8px 20px rgba(31, 74, 255, 0.25);
        }

        .mw-btn-wrap[data-active="true"] div.stButton > button:hover {
            background: #1638c9;
        }

        .mw-menu-card {
            background: rgba(255,255,255,0.75);
            border: 1px solid rgba(0,0,0,0.06);
            border-radius: 14px;
            padding: 0.8rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        }

        .mw-side-title {
            font-weight: 800;
            margin-bottom: 0.75rem;
            font-size: 1.05rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # Banner
    # =========================
    st.markdown('<div class="mw-banner">', unsafe_allow_html=True)
    st.image("mwebv2.png", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="mw-content">', unsafe_allow_html=True)

    if "active_module" not in st.session_state:
        st.session_state.active_module = "home"

    col1, col2 = st.columns([0.65, 2.0], gap="large")

    # =========================
    # MENU
    # =========================
    with col1:
        #st.markdown('<div class="mw-menu-card">', unsafe_allow_html=True)
        st.markdown('<div class="mw-side-title">Menu</div>', unsafe_allow_html=True)

        def menu_button(label, module_key):
            active = (st.session_state.active_module == module_key)
            st.markdown(
                f'<div class="mw-btn-wrap" data-active="{str(active).lower()}">',
                unsafe_allow_html=True
            )
            if st.button(label, use_container_width=True, key=f"btn_{module_key}"):
                st.session_state.active_module = module_key
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # Botões
        menu_button("🏠 Home", "home")
        menu_button("📱 Sensor Inercial", "inertial_rec")
        menu_button("⚖️ Equilíbrio Estático", "static_balance")
        menu_button("🚶 Timed Up and Go (TUG)", "tug")
        menu_button("🚶‍♂️ Caminhada 4 m", "gait_4m")
        menu_button("👆 Finger Tapping Test", "finger_tapping")
        menu_button("✋ Tremor de Mão", "hand_tremor")
        menu_button("🦘 Salto", "jump")
        menu_button("⭐ Teste Y", "y_test")

        st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # CONTEÚDO PRINCIPAL
    # =========================
    with col2:
        if st.session_state.active_module == "home":
            st.markdown("### Bem-vindo ao Momentum Web")
            st.info(
                "Selecione um teste no menu à esquerda para iniciar a avaliação."
            )

        elif st.session_state.active_module == "inertial_rec":
            inertial_file.render()

        elif st.session_state.active_module == "static_balance":
            st.warning("Módulo de Equilíbrio Estático em desenvolvimento.")

        elif st.session_state.active_module == "tug":
            st.warning("Módulo Timed Up and Go (TUG) em desenvolvimento.")

        elif st.session_state.active_module == "gait_4m":
            st.warning("Módulo Caminhada de 4 m em desenvolvimento.")

        elif st.session_state.active_module == "finger_tapping":
            st.warning("Módulo Finger Tapping Test em desenvolvimento.")

        elif st.session_state.active_module == "hand_tremor":
            st.warning("Módulo Tremor de Mão em desenvolvimento.")

        elif st.session_state.active_module == "jump":
            st.warning("Módulo Salto em desenvolvimento.")

        elif st.session_state.active_module == "y_test":
            st.warning("Módulo Teste Y em desenvolvimento.")

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
