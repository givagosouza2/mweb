import io
import numpy as np
import pandas as pd
import streamlit as st


def _read_inertial_first4cols(uploaded_file) -> pd.DataFrame:
    raw = uploaded_file.getvalue()
    if not raw:
        raise ValueError("Arquivo vazio (0 bytes).")

    # tenta ler com separadores comuns diretamente de bytes
    last_err = None
    df = None
    for sep in (";", ","):
        try:
            df = pd.read_csv(io.BytesIO(raw), sep=sep, header=None, engine="python")
            # precisa ter pelo menos 4 colunas
            if df.shape[1] >= 4:
                break
        except Exception as e:
            last_err = e
            df = None

    if df is None or df.shape[1] < 4:
        raise ValueError(f"Não consegui ler o arquivo com 4 colunas. Último erro: {last_err}")

    df = df.iloc[:, :4].copy()
    df.columns = ["Tempo", "X", "Y", "Z"]
    return df


def _to_float_series(s: pd.Series) -> pd.Series:
    """
    Converte uma série para float aceitando vírgula decimal.
    """
    # transforma tudo em string, troca vírgula por ponto, remove espaços
    s2 = s.astype(str).str.strip().str.replace(",", ".", regex=False)
    return pd.to_numeric(s2, errors="coerce")


def render():
    st.subheader("Sensor Inercial — Norma (X,Y,Z) vs Tempo")

    uploaded = st.file_uploader(
        "Selecione o arquivo CSV/TXT do smartphone",
        type=["csv", "txt"],
        key="inertial_uploader_v2"
    )

    if uploaded is None:
        st.info("Selecione um arquivo para iniciar.")
        return

    try:
        df = _read_inertial_first4cols(uploaded)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return

    # Debug mínimo (muito útil no celular)
    with st.expander("Debug (ver o que foi importado)", expanded=False):
        st.write("Tamanho do arquivo (bytes):", len(uploaded.getvalue()))
        st.write("Shape lido (linhas, colunas):", df.shape)
        st.dataframe(df.head(15), use_container_width=True)

    # converte aceitando vírgula decimal
    t = _to_float_series(df["Tempo"])
    x = _to_float_series(df["X"])
    y = _to_float_series(df["Y"])
    z = _to_float_series(df["Z"])

    # remove linhas iniciais “não-numéricas” automaticamente
    valid = t.notna() & x.notna() & y.notna() & z.notna()

    if valid.sum() < 5:
        st.error(
            "Poucos dados numéricos válidos após conversão.\n"
            "Isso geralmente acontece por separador errado ou vírgula decimal.\n"
            "Abra o Debug para ver as primeiras linhas."
        )
        return

    t = t[valid].to_numpy(float)
    x = x[valid].to_numpy(float)
    y = y[valid].to_numpy(float)
    z = z[valid].to_numpy(float)

    # tempo em ms -> s (se seu arquivo realmente for ms)
    # (mantive como você fez)
    t = t / 1000.0

    # norma
    norm = np.sqrt(x**2 + y**2 + z**2)

    # Downsample para mobile (evita travar render)
    st.subheader("Plot")
    max_points = st.slider("Máximo de pontos no gráfico (mobile friendly)", 500, 20000, 5000, step=500)
    if len(t) > max_points:
        step = int(np.ceil(len(t) / max_points))
        t_plot = t[::step]
        norm_plot = norm[::step]
    else:
        t_plot = t
        norm_plot = norm

    plot_df = pd.DataFrame({"Tempo (s)": t_plot, "Norma": norm_plot})
    st.line_chart(plot_df, x="Tempo (s)", y="Norma", use_container_width=True)

    st.caption(f"Válidos: {len(norm)} | Plotados: {len(norm_plot)}")
