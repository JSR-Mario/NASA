
# Front/home.py
import streamlit as st
from pathlib import Path
import pandas as pd
import altair as alt
import numpy as np

st.set_page_config(page_title="Minima accion - Explorando exoplanetas", layout="wide")

st.markdown(
    """
    <style>
    :root{
        --card-bg: #f7f7f9;
        --card-border: #e6e6e6;
        --card-text: #111827;
        --muted: #6c757d;
        --hero-text: #0f172a;
    }

    /* Dark mode */
    @media (prefers-color-scheme: dark) {
        :root{
            --card-bg: #0f1724;        /* card dark bg */
            --card-border: #24303b;    /* subtle border */
            --card-text: #e6eef8;      /* light text */
            --muted: #9aa6b2;
            --hero-text: #ffffff;
        }
    }

    .hero { font-size:30px; font-weight:700; color:var(--hero-text); }
    .muted { color: var(--muted); }
    .card {
        background-color: var(--card-bg);
        padding:12px;
        border-radius:8px;
        border:1px solid var(--card-border);
        color: var(--card-text);
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .metric-value { font-size:26px; font-weight:700; color: var(--card-text); }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- Header / Hero ---
st.markdown('<div class="hero">KOI Predictor — Hunting for Exoplanets with AI</div>', unsafe_allow_html=True)
st.markdown("### Un vistazo visual a los candidatos y sus propiedades")
st.write("")

# --- Importance text ---
st.markdown("#### ¿Por qué importa esto?")
st.write(
    "La búsqueda de exoplanetas requiere analizar grandes volúmenes de señales de tránsito y "
    "detectar patrones sutiles en datos fotométricos y orbitales. Un flujo reproducible que "
    "transforme los datos, aplique modelos de clasificación y visualice resultados facilita tanto "
    "la exploración científica como la validación rápida de nuevos candidatos."
)

st.write("---")

# --- Load CSV (ruta relativa desde Front/) ---
DATA_PATH = Path(__file__).resolve().parent.parent.joinpath("Back", "predicciones.csv")
st.markdown(f"**Fuente de datos:** `{DATA_PATH}`")

df = None
if DATA_PATH.exists():
    try:
        df = pd.read_csv(DATA_PATH, low_memory=False)
        st.success(f"CSV cargado: {len(df):,} filas, {len(df.columns):,} columnas")
    except Exception as e:
        st.error(f"Error leyendo CSV: {e}")
else:
    st.warning("No se encontró `Back/predicciones.csv`. Genera el CSV y colócalo en Back/.")


# -------------------------
# Modelo / Métricas (visual)
# -------------------------
st.markdown("## Resumen del modelo y métricas")

# Leaderboard (hardcoded a partir del texto que pegaste)
leaderboard_df = pd.DataFrame({
    "model": [
        "WeightedEnsemble_L2",
        "CatBoost_BAG_L1/T4",
        "CatBoost_BAG_L1/T1"
    ],
    "score_test": [0.985270, 0.984847, 0.984673],
    "score_val": [0.979885, 0.978945, 0.978919],
    "fit_time": [46.082008, 14.649281, 5.968385],
    "stack_level": [2, 1, 1],
})

# Key metrics (inyectadas)
roc_auc = 0.9853
pr_auc = 0.9653
tn, fp, fn, tp = 1981, 65, 93, 731
accuracy = (tp + tn) / (tn + fp + fn + tp)
support_total = tn + fp + fn + tp

# Layout: leaderboard + metric cards
col1, col2 = st.columns([2, 3])

with col1:
    st.markdown("#### Leaderboard (top modelos)")
    # ordenar por score_test y mostrar
    st.dataframe(leaderboard_df.sort_values("score_test", ascending=False).reset_index(drop=True).style.format({
        "score_test": "{:.6f}",
        "score_val": "{:.6f}",
        "pred_time_test": "{:.3f}",
        "pred_time_val": "{:.3f}",
        "fit_time": "{:.1f}"
    }))

with col2:
    # Métricas visuales (tarjetas sencillas)
    mcol1, mcol2 = st.columns(2)
    st.write("")
    mcol3, mcol4 = st.columns(2) 
    mcol1.markdown('<div class="card"><div style="font-size:12px;color:#6c757d">ROC-AUC (eval metric)</div>'
                   f'<div class="metric-value">{roc_auc:.4f}</div></div>', unsafe_allow_html=True)
    mcol2.markdown('<div class="card"><div style="font-size:12px;color:#6c757d">PR-AUC</div>'
                   f'<div class="metric-value">{pr_auc:.4f}</div></div>', unsafe_allow_html=True)
    mcol3.markdown('<div class="card"><div style="font-size:12px;color:#6c757d">Falsos Negativos</div>'
                   f'<div class="metric-value">{fn:,}</div></div>', unsafe_allow_html=True)
    mcol4.markdown('<div class="card"><div style="font-size:12px;color:#6c757d">Falsos Positivos</div>'
                   f'<div class="metric-value">{fp:,}</div></div>', unsafe_allow_html=True)
    st.write("")
    st.markdown("**Nota:** el predictor fue entrenado con `eval_metric='roc_auc'` para maximizar ROC-AUC.")
    st.write("")  # espacio

st.write("---")

# -------------------------
# Top features (importancia)
# -------------------------
st.markdown("## Top features (importancia)")

# Top features (mostramos top 5 que proporcionaste)
fi_df = pd.DataFrame({
    "feature": ["koi_model_snr", "koi_count", "koi_prad", "duration_anomaly", "koi_dicco_mdec"],
    "importance": [0.039159, 0.004997, 0.004494, 0.003061, 0.002622]
}).sort_values("importance", ascending=True)  # orden ascendente para barh

# gráfico de barras horizontales (Altair)
bar = alt.Chart(fi_df).mark_bar().encode(
    x=alt.X("importance:Q", title="Importancia"),
    y=alt.Y("feature:N", sort='-x', title="Feature"),
    tooltip=[alt.Tooltip("feature:N"), alt.Tooltip("importance:Q", format=".6f")]
).properties(height=220)
st.altair_chart(bar, use_container_width=True)

# mostrar tabla simple con top features
st.dataframe(fi_df.sort_values("importance", ascending=False).reset_index(drop=True).style.format({"importance": "{:.6f}"}))

st.write("---")

# --- Stacked plots (uno encima del otro), puntos más grandes ---
st.markdown("## Exploracion de Resultados visual")

if df is None:
    st.info("Sube o genera `Back/predicciones.csv` y recarga la página para ver las gráficas.")
else:
    # ---------- Top: Kepler vs G-band ----------
    st.markdown("### Kepler Magnitude vs G-band Magnitude")

    x_col = "koi_kepmag"
    y_col = "koi_gmag"
    color_col = "koi_steff"  # temperatura para colorear
    size_col = "koi_model_snr"

    missing = [c for c in (x_col, y_col) if c not in df.columns]
    if missing:
        st.error(f"Faltan columnas para la gráfica: {missing}.")
    else:
        plot_df = df[[x_col, y_col]].copy()
        for c in (color_col, size_col, "kepid", "target", "prediction"):
            if c in df.columns:
                plot_df[c] = df[c]
        plot_df = plot_df.dropna(subset=[x_col, y_col])

        tooltip_fields = ["kepid", x_col, y_col]
        if color_col in plot_df.columns:
            tooltip_fields.append(color_col)
        if size_col in plot_df.columns:
            tooltip_fields.append(size_col)
        if "target" in plot_df.columns:
            tooltip_fields.append("target")
        if "prediction" in plot_df.columns:
            tooltip_fields.append("prediction")

        base = alt.Chart(plot_df).mark_circle(opacity=0.9, size=80).encode(
            x=alt.X(f"{x_col}:Q", title="Kepler Magnitude"),
            y=alt.Y(f"{y_col}:Q", title="G-band Magnitude"),
            tooltip=[alt.Tooltip(f"{t}", format=".4f") if plot_df[t].dtype.kind in "fi" else alt.Tooltip(f"{t}") for t in tooltip_fields]
        )

        if color_col in plot_df.columns:
            chart = base.encode(color=alt.Color(f"{color_col}:Q", title="Teff (K)", scale=alt.Scale(scheme="viridis")))
        else:
            chart = base

        chart = chart.properties(width=900, height=500).interactive()
        st.altair_chart(chart, use_container_width=True)

    st.write("---")

    # ---------- Bottom: Spatial Distribution (RA vs Dec) ----------
    st.markdown("### Spatial Distribution (RA vs Dec)")

    ra_col = "ra"
    dec_col = "dec"
    color_spatial = "target"
    size_spatial = "koi_model_snr"

    missing_sp = [c for c in (ra_col, dec_col) if c not in df.columns]
    if missing_sp:
        st.error(f"No se puede mostrar la distribución espacial; faltan columnas: {missing_sp}")
    else:
        sp_df = df[[ra_col, dec_col]].copy()
        sp_df[ra_col] = pd.to_numeric(sp_df[ra_col], errors="coerce")
        sp_df[dec_col] = pd.to_numeric(sp_df[dec_col], errors="coerce")

        for c in ("kepid", color_spatial, size_spatial, "prediction"):
            if c in df.columns:
                sp_df[c] = df[c]

        sp_df = sp_df.dropna(subset=[ra_col, dec_col])
        if len(sp_df) == 0:
            st.warning("No hay filas con RA/Dec válidos después de la conversión.")
        else:
            ra_min, ra_max = float(sp_df[ra_col].min()), float(sp_df[ra_col].max())
            dec_min, dec_max = float(sp_df[dec_col].min()), float(sp_df[dec_col].max())

            tooltip_sp = ["kepid", ra_col, dec_col]
            if color_spatial in sp_df.columns:
                tooltip_sp.append(color_spatial)
            if size_spatial in sp_df.columns:
                tooltip_sp.append(size_spatial)
            if "prediction" in sp_df.columns:
                tooltip_sp.append("prediction")

            base_sp = alt.Chart(sp_df).mark_circle(opacity=0.9, size=80).encode(
                x=alt.X(f"{ra_col}:Q", title="Right Ascension (deg)"),
                y=alt.Y(f"{dec_col}:Q", title="Declination (deg)"),
                tooltip=[alt.Tooltip(f"{t}", format=".3f") if sp_df[t].dtype.kind in "fi" else alt.Tooltip(f"{t}") for t in tooltip_sp]
            )

            # asegurar target como string para evitar mismatch de tipo en domain/color
            if color_spatial in sp_df.columns:
                sp_df[color_spatial] = sp_df[color_spatial].astype(str).fillna("nan")
                unique_vals = list(sp_df[color_spatial].dropna().unique())
                if len(unique_vals) == 2:
                    try:
                        sorted_vals = sorted(unique_vals, key=lambda v: float(v))
                    except Exception:
                        sorted_vals = sorted(unique_vals, key=lambda v: str(v))
                    domain = [str(v) for v in sorted_vals]
                    range_colors = ["#1f77b4", "#d62728"]
                    chart_sp = base_sp.encode(
                        color=alt.Color(f"{color_spatial}:N", title="Target",
                                        scale=alt.Scale(domain=domain, range=range_colors))
                    )
                else:
                    if sp_df[color_spatial].nunique() <= 12:
                        chart_sp = base_sp.encode(color=alt.Color(f"{color_spatial}:N", title="Target", legend=alt.Legend(orient="right")))
                    else:
                        chart_sp = base_sp.encode(color=alt.Color(f"{color_spatial}:Q", title="Target (numeric)", scale=alt.Scale(scheme="viridis")))
            else:
                chart_sp = base_sp

            # aplicar zoom si hay intersección con los datos
            zoom_x = [280, 304]
            zoom_y = [41, 49]
            x_ok = not (ra_max < zoom_x[0] or ra_min > zoom_x[1])
            y_ok = not (dec_max < zoom_y[0] or dec_min > zoom_y[1])

            if x_ok and y_ok:
                x_scale = alt.Scale(domain=zoom_x)
                y_scale = alt.Scale(domain=zoom_y)
            else:
                x_scale = alt.Scale(domain=[ra_min, ra_max])
                y_scale = alt.Scale(domain=[dec_min, dec_max])

            chart_sp = chart_sp.properties(width=900, height=600).encode(
                x=alt.X(f"{ra_col}:Q", scale=x_scale, title="Right Ascension (deg)"),
                y=alt.Y(f"{dec_col}:Q", scale=y_scale, title="Declination (deg)")
            ).interactive()

            st.altair_chart(chart_sp, use_container_width=True)
st.write("---")


# --- Explanation about the interface ---
st.markdown("## Sobre la interfaz")
st.write(
    "Esta interfaz combina herramientas para transformar automáticamente CSVs KOI y para ejecutar "
    "modelos de clasificación entrenados con AutoGluon. En el panel de predicción puedes subir "
    "un CSV, aplicar las transformaciones necesarias y obtener predicciones en CSV; en el panel "
    "de entrenamiento puedes crear/derivar un target, ajustar parámetros de entrenamiento y "
    "reentrenar un predictor localmente."
)
st.write(
    "Debajo encontrarás accesos rápidos a las páginas principales del proyecto (predicción y entrenamiento)."
)

# --- Quick links to other pages (instructions) ---
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Interfaz de predicción**")
    st.code("cd Front\nstreamlit run pagina_predictor.py", language="bash")
with col2:
    st.markdown("**Interfaz de entrenamiento**")
    st.code("cd Front\nstreamlit run pagina_modelo.py", language="bash")

st.write("---")

# --- Footer ---
st.markdown("<div style='font-size:12px;color:#6c757d'>© Proyecto KOI Predictor — Visualización y herramientas para exploración de candidatos. Datos cargados desde `Back/predicciones.csv`.</div>", unsafe_allow_html=True)


