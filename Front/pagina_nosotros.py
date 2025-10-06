
import streamlit as st
from PIL import Image

# --- CONFIGURACIÓN DE LA PÁGINA ---
# El layout "wide" aprovecha mejor el espacio en pantallas grandes.


# --- DATOS DEL EQUIPO ---
# Estructura: "Nombre": [imagen_path, linkedin_url, github_url, quote]
# Agrega o quita miembros del equipo aquí, y añade su frase.
TEAM_MEMBERS = {
    "Mario": {
        "img": "static/rene.jpeg",
        "linkedin": "https://www.linkedin.com/in/anagarcia",
        "github": "https://github.com/anagarcia",
        "quote": "La mejor forma de predecir el futuro es crearlo."
    },
    "Bruno Díaz": {
        "img": "static/jesus.jpeg",
        "linkedin": "https://www.linkedin.com/in/brunodiaz",
        "github": "https://github.com/brunodiaz",
        "quote": "El código es como el humor. Cuando tienes que explicarlo, es malo."
    },
    "Carla Torres": {
        "img": "static/ivan.jpeg",
        "linkedin": "https://www.linkedin.com/in/carlatorres",
        "github": "https://github.com/carlatorres",
        "quote": "La simplicidad es la máxima sofisticación."
    },
    "David Mendoza": {
        "img": "static/bruno.jpeg",
        "linkedin": "https://www.linkedin.com/in/davidmendoza",
        "github": "https://github.com/davidmendoza",
        "quote": "Siempre hay una solución, solo hay que encontrarla."
    },
    "Elena Ríos": {
        "img": "static/morgan.jpeg",
        "linkedin": "https://www.linkedin.com/in/elenarios",
        "github": "https://github.com/elenarios",
        "quote": "La curiosidad es la mecha en la vela del aprendizaje."
    },
    "Fernando Vega": {
        "img": "static/rene.jpeg",
        "linkedin": "https://www.linkedin.com/in/fernandovega",
        "github": "https://github.com/fernandovega",
        "quote": "No te preocupes si no funciona bien. Si todo lo hiciera, estarías sin trabajo."
    },
}

# --- PÁGINA PRINCIPAL ---
st.title("Nuestro Equipo")
st.write("---")

# --- LAYOUT DEL EQUIPO ---
# Dividimos la lista de miembros en filas de 3 columnas.
members_list = list(TEAM_MEMBERS.items())
num_members = len(members_list)
cols_per_row = 3
num_rows = (num_members + cols_per_row - 1) // cols_per_row # Cálculo para el número de filas

for i in range(num_rows):
    # Obtenemos los miembros para la fila actual
    row_members = members_list[i * cols_per_row:(i + 1) * cols_per_row]
    
    # Creamos las columnas para la fila
    cols = st.columns(cols_per_row)
    
    for j, (name, data) in enumerate(row_members):
        with cols[j]:
            # Contenedor para cada miembro con un borde sutil
            with st.container(border=True):
                try:
                    # Cargamos la imagen
                    st.image(data["img"], caption=name, width=450)
                except FileNotFoundError:
                    st.error(f"Imagen no encontrada para {name} en {data['img']}")
                    st.image("https://placehold.co/400x400/EEE/31343C?text=Sin+Imagen", width=1000)
                
                # Mostramos la frase célebre de cada miembro.
                # st.caption es ideal para textos pequeños y se centra automáticamente.
                st.caption(f"*{data['quote']}*")
                
                # Usamos markdown para centrar los enlaces y hacerlos más visuales
                st.markdown(
                    f"""
                    <div style='text-align: center; margin-top: 1em;'>
                        <a href="{data['linkedin']}" target="_blank">LinkedIn</a> | 
                        <a href="{data['github']}" target="_blank">GitHub</a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# Espacio extra al final
st.write("---")

