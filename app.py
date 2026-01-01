import importlib
import streamlit as st

def image_button(img_path: str, label: str, key: str) -> bool:
    """
    "Botão com imagem" no Streamlit: mostra a imagem e um botão logo abaixo.
    """
    st.image(img_path, use_container_width=True)
    return st.button(label, key=key, use_container_width=True)

def main():
    st.set_page_config(page_title="Momentum Web", layout="wide")
    st.title("Momentum Web")

    st.write("Clique no módulo que deseja abrir:")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Troque pelo caminho da sua imagem (ex.: assets/gyro.png)
        if image_button("buttons/inertial.png", "Abrir módulo Gyro (importar arquivo)", "btn_gyro"):
            # IMPORTA o segundo arquivo SOMENTE quando clicar
            mod = importlib.import_module("gyro_module")  # <-- nome do arquivo .py (sem .py)
            mod.run()  # função do segundo arquivo
            st.stop()  # impede que o resto da tela inicial continue renderizando

    with col2:
        st.info("Outros módulos podem entrar aqui.")
    with col3:
        st.info("...")

if __name__ == "__main__":
    main()
✅ Observação: aqui o app.py não lê arquivo. Ele só mostra o botão com imagem e, ao clicar, importa o módulo e chama run().

2) gyro_module.py (segundo arquivo: upload/leitura do CSV/TXT)
python
Copiar código
import io
import pandas as pd
import streamlit as st


def _read_table(uploaded_file) -> pd.DataFrame:
    """
    Lê CSV/TXT com tentativas de encoding e separador.
    """
    raw = uploaded_file.read()

    # encodings comuns
    last_err = None
    text = None
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
        try:
            text = raw.decode(enc)
            break
        except Exception as e:
            last_err = e

    if text is None:
        raise ValueError(f"Não foi possível decodificar o arquivo. Erro: {last_err}")

    # detecta separador
    sample = text[:5000]
    sep = ";" if sample.count(";") > sample.count(",") else ","

    return pd.read_csv(io.StringIO(text), sep=sep, engine="python")


def run():
    st.header("Módulo Gyro — Importar e visualizar arquivo")

    uploaded = st.file_uploader("Selecione um arquivo CSV ou TXT", type=["csv", "txt"])

    if uploaded is None:
        st.info("Aguardando você selecionar um arquivo.")
        if st.button("⬅️ Voltar ao Momentum Web", use_container_width=True):
            st.rerun()
        return

    try:
        df = _read_table(uploaded)
        st.success("Arquivo carregado com sucesso.")

        st.write("Pré-visualização:")
        st.dataframe(df.head(30), use_container_width=True)

        st.write(f"Linhas: **{df.shape[0]}** | Colunas: **{df.shape[1]}**")

    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

    if st.button("⬅️ Voltar ao Momentum Web", use_container_width=True):
        st.rerun()
