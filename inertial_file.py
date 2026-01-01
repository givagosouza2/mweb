import io
import numpy as np
import pandas as pd
import streamlit as st


def _read_csv_clean(uploaded_file) -> pd.DataFrame:
    # ✅ mais robusto do que .read() em reruns
    raw = uploaded_file.getvalue()

    # encodings comuns
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

    # separador (vírgula vs ponto-e-vírgula)
    sample = text[:5000]
    sep = ";" if sample.count(";") > sample.count(",") else ","

    df = pd.read_csv(io.StringIO(text), sep=sep, engine="python")
    df.columns = df.columns.astype(str).str.strip()  # remove espaços em nomes
    return df


def render():
    st.subheader("Sensor Inercial — Norma (X,Y,Z) vs Tempo")

    uploaded = st.file_uploader(
        "Selecione um CSV/TXT do smartphone",
        type=["csv", "txt"],
        key="gyro_uploader",
    )

    if uploaded is None:
        st.info("Selecione um arquivo para visualizar o dado.")
        return

    try:
        df = _read_csv_clean(uploaded)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return

    

    # tenta usar o padrão Tempo, X, Y, Z
    default_map = {"Tempo": None, "X": None, "Y": None, "Z": None}
    for k in default_map.keys():
        if k in df.columns:
            default_map[k] = k

    time_col = st.selectbox("Tempo", cols, index=cols.index(default_map["Tempo"]) if default_map["Tempo"] in cols else 0)
    x_col = st.selectbox("X", cols, index=cols.index(default_map["X"]) if default_map["X"] in cols else min(1, len(cols)-1))
    y_col = st.selectbox("Y", cols, index=cols.index(default_map["Y"]) if default_map["Y"] in cols else min(2, len(cols)-1))
    z_col = st.selectbox("Z", cols, index=cols.index(default_map["Z"]) if default_map["Z"] in cols else min(3, len(cols)-1))

    # conversão numérica
    t = pd.to_numeric(df["Tempo"], errors="coerce")
    x = pd.to_numeric(df["X"], errors="coerce")
    y = pd.to_numeric(df["Y"], errors="coerce")
    z = pd.to_numeric(df["Z"], errors="coerce")

    valid = t.notna() & x.notna() & y.notna() & z.notna()
    if valid.sum() < 5:
        st.error("Poucos pontos numéricos válidos. Verifique as colunas escolhidas (ou separador/decimal).")
        return

    t = t[valid].to_numpy(float)
    x = x[valid].to_numpy(float)
    y = y[valid].to_numpy(float)
    z = z[valid].to_numpy(float)

    t = t / 1000.0

    norm = np.sqrt(x**2 + y**2 + z**2)

    plot_df = pd.DataFrame({"Tempo": t, "Norma": norm})
    st.line_chart(plot_df, x="Tempo", y="Norma", use_container_width=True)
