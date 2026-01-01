import io
import numpy as np
import pandas as pd
import streamlit as st


def _read_csv_clean(uploaded_file) -> pd.DataFrame:
    raw = uploaded_file.read()

    # encodings comuns
    text = None
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
        try:
            text = raw.decode(enc)
            break
        except Exception:
            pass
    if text is None:
        raise ValueError("Não foi possível decodificar o arquivo (encoding).")

    # separador
    sep = ";" if text[:5000].count(";") > text[:5000].count(",") else ","
    df = pd.read_csv(io.StringIO(text), sep=sep)

    # limpa nomes (resolve ' X',' Y',' Z')
    df.columns = df.columns.str.strip()
    return df


def render():
    st.subheader("Sensor Inercial — Norma (X,Y,Z) vs Tempo")

    uploaded = st.file_uploader("Selecione um CSV/TXT", type=["csv", "txt"], key="gyro_uploader")

    if uploaded is None:
        st.info("Selecione um arquivo para visualizar o gráfico.")
        return

    df = _read_csv_clean(uploaded)

    required = {"Tempo", "X", "Y", "Z"}
    if not required.issubset(df.columns):
        st.error(f"Colunas esperadas: {required}. Encontrado: {set(df.columns)}")
        return

    t = pd.to_numeric(df["Tempo"], errors="coerce")
    x = pd.to_numeric(df["X"], errors="coerce")
    y = pd.to_numeric(df["Y"], errors="coerce")
    z = pd.to_numeric(df["Z"], errors="coerce")

    valid = t.notna() & x.notna() & y.notna() & z.notna()
    t, x, y, z = t[valid].to_numpy(float), x[valid].to_numpy(float), y[valid].to_numpy(float), z[valid].to_numpy(float)

    # opcional: ms -> s
    if st.checkbox("Tempo em milissegundos (converter para s)", value=False, key="gyro_ms"):
        t = t / 1000.0

    norm = np.sqrt(x**2 + y**2 + z**2)

    plot_df = pd.DataFrame({"Tempo": t, "Norma": norm})
    st.line_chart(plot_df, x="Tempo", y="Norma", use_container_width=True)

    st.caption(f"N={len(norm)} | Média={norm.mean():.4f} | RMS={np.sqrt((norm**2).mean()):.4f}")
