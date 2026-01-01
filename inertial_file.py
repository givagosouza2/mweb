import io
import numpy as np
import pandas as pd
import streamlit as st


# -----------------------------
# Utilitários de leitura (mobile-safe)
# -----------------------------
def _decode_bytes(raw: bytes) -> str:
    """Decodifica bytes em texto tentando encodings comuns."""
    last_err = None
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
        try:
            text = raw.decode(enc)
            if text.strip():
                return text
        except Exception as e:
            last_err = e
    raise ValueError(f"Não foi possível decodificar o arquivo (encoding). Último erro: {last_err}")


def _infer_sep(text: str) -> str:
    """Inferência simples de separador."""
    sample = text[:8000]
    return ";" if sample.count(";") > sample.count(",") else ","


def _to_float_series(s: pd.Series) -> pd.Series:
    """Converte série para float aceitando vírgula decimal."""
    s2 = s.astype(str).str.strip().str.replace(",", ".", regex=False)
    return pd.to_numeric(s2, errors="coerce")


def _drop_non_numeric_header_like_rows(df4: pd.DataFrame) -> pd.DataFrame:
    """
    Remove linhas iniciais tipo cabeçalho/texto (sem depender de header).
    Estratégia: mantém apenas linhas onde Tempo,X,Y,Z conseguem virar número.
    """
    t = _to_float_series(df4.iloc[:, 0])
    x = _to_float_series(df4.iloc[:, 1])
    y = _to_float_series(df4.iloc[:, 2])
    z = _to_float_series(df4.iloc[:, 3])
    valid = t.notna() & x.notna() & y.notna() & z.notna()
    return df4.loc[valid].copy()


@st.cache_data(show_spinner=False)
def _load_first4cols_cached(raw: bytes) -> pd.DataFrame:
    """
    Lê o arquivo sem cabeçalho e retorna dataframe com colunas [Tempo,X,Y,Z]
    usando as 4 primeiras colunas por posição.
    Cacheado para não reprocessar em reruns.
    """
    text = _decode_bytes(raw)
    sep = _infer_sep(text)

    # header=None: ignora cabeçalho; engine python para tolerar formatos
    df = pd.read_csv(io.StringIO(text), sep=sep, header=None, engine="python")

    if df.shape[1] < 4:
        raise ValueError(f"O arquivo tem {df.shape[1]} colunas; preciso de pelo menos 4 (Tempo, X, Y, Z).")

    df4 = df.iloc[:, :4].copy()
    df4 = _drop_non_numeric_header_like_rows(df4)

    if df4.empty:
        raise ValueError("Após limpeza, não sobraram linhas numéricas válidas nas 4 primeiras colunas.")

    df4.columns = ["Tempo", "X", "Y", "Z"]
    return df4


# -----------------------------
# Módulo (render)
# -----------------------------
def render():
    st.subheader("Sensor Inercial — Norma (X,Y,Z) vs Tempo (mobile-safe)")

    uploaded = st.file_uploader(
        "Selecione o arquivo CSV/TXT do smartphone",
        type=["csv", "txt"],
        key="inertial_uploader_v2",
    )

    if uploaded is None:
        st.info("Selecione um arquivo para iniciar.")
        return

    # ✅ Não processar automaticamente: evita travar no mobile
    process = st.button("Processar e Plotar", type="primary", use_container_width=True)

    # Mantém bytes em session_state para sobreviver a reruns
    if "inertial_raw" not in st.session_state:
        st.session_state.inertial_raw = None

    if uploaded is not None:
        st.session_state.inertial_raw = uploaded.getvalue()

    if not process:
        st.caption("Dica: no celular, clique em **Processar e Plotar** depois do upload para evitar timeout.")
        return

    raw = st.session_state.inertial_raw
    if not raw:
        st.error("Não consegui acessar os bytes do arquivo. Tente reenviar.")
        return

    # Carrega (cacheado)
    try:
        df = _load_first4cols_cached(raw)
    except Exception as e:
        st.error(f"Erro ao ler/processar o arquivo: {e}")
        return

    # Debug opcional
    with st.expander("Debug (opcional)", expanded=False):
        st.write("Tamanho (bytes):", len(raw))
        st.write("Linhas válidas:", df.shape[0])
        st.dataframe(df.head(25), use_container_width=True)

    # Conversão numérica (agora por colunas nomeadas, já limpas)
    t = _to_float_series(df["Tempo"])
    x = _to_float_series(df["X"])
    y = _to_float_series(df["Y"])
    z = _to_float_series(df["Z"])

    valid = t.notna() & x.notna() & y.notna() & z.notna()
    if valid.sum() < 5:
        st.error("Poucos pontos numéricos válidos após conversão. Verifique o arquivo.")
        return

    t = t[valid].to_numpy(float)
    x = x[valid].to_numpy(float)
    y = y[valid].to_numpy(float)
    z = z[valid].to_numpy(float)

    # Configuração de tempo
    st.markdown("### Configuração")
    colA, colB = st.columns(2)
    with colA:
        time_unit = st.selectbox("Unidade do tempo", ["ms", "s", "frames"], index=0)
    with colB:
        fps = None
        if time_unit == "frames":
            fps = st.number_input("FPS (para frames → segundos)", min_value=1.0, max_value=1000.0, value=30.0, step=1.0)

    if time_unit == "ms":
        t_sec = t / 1000.0
    elif time_unit == "s":
        t_sec = t
    else:  # frames
        t_sec = t / float(fps)

    # Norma
    norm = np.sqrt(x * x + y * y + z * z)

    # Downsample para mobile
    st.markdown("### Plot")
    max_points = st.slider("Máximo de pontos no gráfico (recomendado para celular)", 500, 20000, 5000, step=500)

    n = len(t_sec)
    if n > max_points:
        step = int(np.ceil(n / max_points))
        t_plot = t_sec[::step]
        norm_plot = norm[::step]
    else:
        t_plot = t_sec
        norm_plot = norm

    plot_df = pd.DataFrame({"Tempo (s)": t_plot, "Norma": norm_plot})
    st.line_chart(plot_df, x="Tempo (s)", y="Norma", use_container_width=True)

    # Resumo
    st.caption(f"Válidos: {n} | Plotados: {len(norm_plot)}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Média", f"{float(np.mean(norm)):.4f}")
    c2.metric("RMS", f"{float(np.sqrt(np.mean(norm**2))):.4f}")
    c3.metric("Máx", f"{float(np.max(norm)):.4f}")
    c4.metric("Mín", f"{float(np.min(norm)):.4f}")
