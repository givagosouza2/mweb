import streamlit as st
import inertial_file  # segundo arquivo

def main():
    st.set_page_config(page_title="Momentum Web", layout="wide")
    st.title("Momentum Web, uma aplicação Web para o Momentum Sensors")

    if "active_module" not in st.session_state:
        st.session_state.active_module = "home"

    # --- HUB com botão (imagem + botão) ---
    col1, col2 = st.columns([0.4, 2])

    with col1:
        if st.button("Home", use_container_width=True):
            st.session_state.active_module = "home"

        if st.button("Sensor Inercial Livre", use_container_width=True):
            st.session_state.active_module = "inertial_rec"

        
    # --- ÁREA PRINCIPAL (onde o gráfico vai aparecer) ---
    with col2:
        if st.session_state.active_module == "home":
            st.info("Bem-vindo Momentum Web")

        elif st.session_state.active_module == "inertial_rec":
            inertial_file.render()

if __name__ == "__main__":
    main()
