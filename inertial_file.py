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
