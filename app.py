import streamlit as st
import inertial_file  # segundo arquivo

def main():
    st.set_page_config(page_title="Momentum Web", layout="wide")
    st.title("Momentum Web")

    if "active_module" not in st.session_state:
        st.session_state.active_module = "home"

    # --- HUB com botão (imagem + botão) ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("b1.png", width=220)
        if st.button("Sensor Inercial (Norma)", use_container_width=True):
            st.session_state.active_module = "inertial_rec"

        if st.button("Home", use_container_width=True):
            st.session_state.active_module = "home"

    # --- ÁREA PRINCIPAL (onde o gráfico vai aparecer) ---
    with col2:
        if st.session_state.active_module == "home":
            st.info("Escolha um módulo no painel à esquerda.")

        elif st.session_state.active_module == "inertial_rec":
            gyro_module.render()  # renderiza o módulo DENTRO da interface principal

if __name__ == "__main__":
    main()
