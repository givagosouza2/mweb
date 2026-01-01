import io
import numpy as np
import pandas as pd
import streamlit as st


def read_inertial_by_position(uploaded_file) -> pd.DataFrame:
    """
    Lê arquivo CSV/TXT SEM cabeçalho.
    Assume:
    col 0 -> tempo
    col 1 -> X
    col 2 -> Y
    col 3 -> Z
    """
    raw = uploaded_file.getvalue()

    # tenta encodings comuns
    text = None
    last_err = None
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
        try:
            text = raw.decode(enc)
            break
        except Exception as e:
            last_err = e

    if text is None or len(text.strip()) == 0:
        raise ValueError(f"Arquivo vazio ou encoding inválido. Último erro: {last_err}")

    # detecta separador
    sample = text[:5000]
    sep = ";" if sample.count(";") > sample.count(",") else ","

    # 🔑 header=None -> ignora cabeçalho completamente
    df = pd.read_csv(
        io.StringIO(text),
        sep=sep,
        header=None,
        engine="python"
    )

    if df.shape[1] < 4:
        raise ValueError(
            f"Arquivo possui apenas {df.shape[1]} colunas. "
            "São necessárias pelo menos 4 (Tempo, X, Y, Z)."
        )

    # usa apenas as 4 primeiras colunas
    df = df.iloc[:, :4]
    df.columns = ["Tempo", "X", "Y", "Z"]

    return df


def render():
    st.subheader("Sensor Inercial — Norma (X,Y,Z) vs Tempo")

    uploaded = st.file_uploader(
        "Selecione o arquivo CSV/TXT do smartphone",
        type=["csv", "txt"],
        key="inertial_uploader"
    )

    if uploaded is None:
        st.info("Selecione um arquivo para iniciar.")
        return

    try:
        df = read_inertial_by_position(uploaded)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return
        
    # conversão numérica segura
    t = pd.to_numeric(df["Tempo"], errors="coerce")
    x = pd.to_numeric(df["X"], errors="coerce")
    y = pd.to_numeric(df["Y"], errors="coerce")
    z = pd.to_numeric(df["Z"], errors="coerce")

    valid = t.notna() & x.notna() & y.notna() & z.notna()
    if valid.sum() < 5:
        st.error("Poucos dados numéricos válidos após conversão.")
        return

    t = t[valid].to_numpy(float)
    x = x[valid].to_numpy(float)
    y = y[valid].to_numpy(float)
    z = z[valid].to_numpy(float)
    
    t = t / 1000.0

    # cálculo da norma
    norm = np.sqrt(x**2 + y**2 + z**2)

    # gráfico
    plot_df = pd.DataFrame({
        "Tempo": t,
        "Norma": norm
    })

    st.subheader("Norma √(X² + Y² + Z²) em função do tempo")
    st.line_chart(plot_df, x="Tempo", y="Norma", use_container_width=True)
