import io
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


def read_csv_clean(uploaded_file) -> pd.DataFrame:
    """
    Lê o CSV/TXT e limpa nomes das colunas (remove espaços).
    Compatível com o arquivo anexado.
    """
    raw = uploaded_file.read()

    # tenta encodings comuns
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
        try:
            text = raw.decode(enc)
            break
        except Exception:
            text = None

    if text is None:
        raise ValueError("Erro de encoding ao ler o arquivo.")

    # detecta separador
    sep = ";" if text[:5000].count(";") > text[:5000].count(",") else ","

    df = pd.read_csv(io.StringIO(text), sep=sep)

    # 🔑 remove espaços extras dos nomes das colunas
    df.columns = df.columns.str.strip()

    return df


def run():
    st.header("Sensor Inercial — Norma dos eixos (X, Y, Z)")

    uploaded = st.file_uploader(
        "Selecione o arquivo CSV do sensor inercial",
        type=["csv", "txt"]
    )

    if uploaded is None:
        st.info("Aguardando seleção do arquivo.")
        return

    try:
        df = read_csv_clean(uploaded)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return

    st.subheader("Pré-visualização do arquivo")
    st.dataframe(df.head(20), use_container_width=True)

    # --- verificação explícita das colunas esperadas ---
    required_cols = {"Tempo", "X", "Y", "Z"}
    if not required_cols.issubset(df.columns):
        st.error(
            f"Colunas esperadas não encontradas.\n"
            f"Esperado: {required_cols}\n"
            f"Encontrado: {set(df.columns)}"
        )
        return

    # --- conversão segura para numérico ---
    t = pd.to_numeric(df["Tempo"], errors="coerce")
    x = pd.to_numeric(df["X"], errors="coerce")
    y = pd.to_numeric(df["Y"], errors="coerce")
    z = pd.to_numeric(df["Z"], errors="coerce")

    valid = t.notna() & x.notna() & y.notna() & z.notna()
    if valid.sum() < 5:
        st.error("Poucos dados válidos após conversão numérica.")
        return

    t = t[valid].to_numpy()
    x = x[valid].to_numpy()
    y = y[valid].to_numpy()
    z = z[valid].to_numpy()

    # --- opção: tempo em ms → segundos ---
    st.subheader("Configuração do tempo")
    time_in_ms = st.checkbox("Tempo está em milissegundos (converter para segundos)", value=False)
    if time_in_ms:
        t = t / 1000.0

    # --- cálculo da norma ---
    norm = np.sqrt(x**2 + y**2 + z**2)

    st.subheader("Norma √(X² + Y² + Z²) em função do tempo")

    plot_df = pd.DataFrame({
        "Tempo": t,
        "Norma": norm
    })
    
    st.line_chart(
        plot_df,
        x="Tempo",
        y="Norma",
        use_container_width=True
    )
    # --- métricas rápidas ---
    st.subheader("Resumo quantitativo")
    st.metric("Amostras", len(norm))
    st.metric("Norma média", f"{np.mean(norm):.5f}")
    st.metric("Norma RMS", f"{np.sqrt(np.mean(norm**2)):.5f}")
    st.metric("Norma máxima", f"{np.max(norm):.5f}")
