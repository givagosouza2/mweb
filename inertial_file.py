import io
import os
import pandas as pd
import streamlit as st


# Ajuste aqui se você quiser “pré-carregar” o arquivo que veio em anexo
DEFAULT_FILEPATH = "/mnt/data/teste momentum 01_gyroData_20251227_135824.csv"


def _read_table(uploaded_file) -> pd.DataFrame:
    """
    Lê CSV/TXT tentando separar e encoding comuns.
    """
    raw = uploaded_file.read()

    # tenta alguns encodings comuns (inclui casos com BOM e latin1)
    last_err = None
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
        try:
            text = raw.decode(enc)
            break
        except Exception as e:
            last_err = e
            text = None
    if text is None:
        raise ValueError(f"Não foi possível decodificar o arquivo. Erro: {last_err}")

    # tenta detectar separador: ; ou ,
    sample = text[:5000]
    sep = ";" if sample.count(";") > sample.count(",") else ","

    # lê com pandas
    df = pd.read_csv(io.StringIO(text), sep=sep, engine="python")
    return df


def _image_button(img_path: str, label: str, key: str) -> bool:
    """
    Simula "botão com imagem": mostra imagem e um botão logo abaixo.
    Retorna True se clicou.
    """
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.caption(f"(Imagem não encontrada: {img_path})")

    return st.button(label, key=key, use_container_width=True)


def run():
    st.set_page_config(page_title="Momentum Web", layout="wide")

    st.title("Momentum Web")

    st.write("Escolha um módulo (exemplo: abrir e visualizar um CSV/TXT).")

    # --- “Botões com imagem” (você pode trocar os caminhos das imagens) ---
    col1, col2, col3 = st.columns(3)

    with col1:
        clicked_gyro = _image_button(
            img_path="assets/gyro.png",   # coloque sua imagem aqui
            label="📈 Abrir Gyro CSV/TXT",
            key="btn_gyro",
        )

    with col2:
        clicked_other = _image_button(
            img_path="assets/acc.png",
            label="(exemplo) Outro módulo",
            key="btn_other",
        )

    with col3:
        clicked_dummy = _image_button(
            img_path="assets/tug.png",
            label="(exemplo) TUG módulo",
            key="btn_tug",
        )

    # --- Roteamento simples ---
    if "screen" not in st.session_state:
        st.session_state.screen = "home"

    if clicked_gyro:
        st.session_state.screen = "gyro"
    elif clicked_other:
        st.session_state.screen = "other"
    elif clicked_dummy:
        st.session_state.screen = "tug"

    st.divider()

    # --- Telas ---
    if st.session_state.screen == "home":
        st.info("Clique em um botão acima para abrir um módulo.")

    elif st.session_state.screen == "gyro":
        st.subheader("Leitura de arquivo (CSV/TXT) — exemplo Gyro")

        uploaded = st.file_uploader("Carregar arquivo CSV/TXT", type=["csv", "txt"])

        # Se não fizer upload, tenta abrir o arquivo “em anexo” (DEFAULT_FILEPATH)
        use_default = (uploaded is None) and os.path.exists(DEFAULT_FILEPATH)

        try:
            if uploaded is not None:
                df = _read_table(uploaded)
                st.success("Arquivo carregado via upload.")
            elif use_default:
                with open(DEFAULT_FILEPATH, "rb") as f:
                    class _FakeUpload:
                        def __init__(self, b): self._b = b
                        def read(self): return self._b
                    df = _read_table(_FakeUpload(f.read()))
                st.success(f"Arquivo carregado do caminho padrão: {DEFAULT_FILEPATH}")
            else:
                st.warning("Envie um arquivo ou coloque um arquivo no caminho padrão.")
                df = None

            if df is not None:
                st.write("Pré-visualização:")
                st.dataframe(df.head(30), use_container_width=True)

                st.write("Resumo:")
                st.write(f"- Linhas: **{df.shape[0]}**  |  Colunas: **{df.shape[1]}**")
                st.write("Tipos de dados:")
                st.dataframe(df.dtypes.astype(str).to_frame("dtype"), use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

        if st.button("⬅️ Voltar", use_container_width=True):
            st.session_state.screen = "home"

    elif st.session_state.screen == "other":
        st.warning("Módulo exemplo ainda não implementado.")
        if st.button("⬅️ Voltar", use_container_width=True):
            st.session_state.screen = "home"

    elif st.session_state.screen == "tug":
        st.warning("Módulo exemplo ainda não implementado.")
        if st.button("⬅️ Voltar", use_container_width=True):
            st.session_state.screen = "home"
