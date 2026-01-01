import importlib
import streamlit as st

def image_button(img_path: str, label: str, key: str) -> bool:
    """
    "Botão com imagem" no Streamlit: mostra a imagem e um botão logo abaixo.
    """
    st.image(img_path, use_container_width=True, width=50)
    return st.button(label, key=key, use_container_width=True)

def main():
    st.set_page_config(page_title="Momentum Web", layout="wide")
    st.title("Momentum Web")

    st.write("Clique no módulo que deseja abrir:")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        # Troque pelo caminho da sua imagem (ex.: assets/gyro.png)
        if image_button("b1.png", "Abrir módulo Gyro (importar arquivo)", "btn_gyro"):
            # IMPORTA o segundo arquivo SOMENTE quando clicar
            mod = importlib.import_module("inertial_file")  # <-- nome do arquivo .py (sem .py)
            mod.run()  # função do segundo arquivo
            st.stop()  # impede que o resto da tela inicial continue renderizando

    with col2:
        st.info("Outros módulos podem entrar aqui.")
    with col3:
        st.info("...")

if __name__ == "__main__":
    main()
