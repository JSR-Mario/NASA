import streamlit as st
from pathlib import Path
import runpy

# configura página (una sola vez)
st.set_page_config(page_title="KOI Predictor - Launcher", layout="wide")

# mapea nombres legibles -> archivos en Front/
BASE = Path(__file__).resolve().parent
PAGES = {
    "Home": BASE / "home.py",
    "Predictor": BASE / "pagina_predictor.py",
    "Crear Modelo": BASE / "pagina_modelo.py",
}

# navegación en la barra lateral
st.sidebar.title("Navegación")
choice = st.sidebar.radio("Ir a:", list(PAGES.keys()), index=0)

# mostrar info básica del launcher
st.sidebar.markdown("---")
st.sidebar.write("Usa este launcher para ejecutar las páginas del proyecto.")
st.sidebar.caption("Cada página se ejecuta como un script separado (runpy).")

# Ejecutar la página seleccionada (ejecuta el script en su propio __main__ namespace)
page_file = PAGES[choice]
try:
    runpy.run_path(str(page_file), run_name="__main__")
except SystemExit:
    # algunos scripts pueden llamar a sys.exit(); lo atrapamos para no romper el launcher
    st.error("La página finalizó con SystemExit.")
except Exception as e:
    st.error(f"Error ejecutando la página {page_file.name}: {e}")

