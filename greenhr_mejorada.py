import streamlit as st
import pypdf
import pandas as pd
import matplotlib.pyplot as plt
import random
import os

# -------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -------------------------------------------------------
st.set_page_config(page_title="GreenHR", page_icon="🌿", layout="wide")

DB_FILE = "usuarios.csv"
UPLOAD_FOLDER = "archivos_subidos"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# -------------------------------------------------------
# ARCHIVO CSV SI NO EXISTE
# -------------------------------------------------------
if not os.path.exists(DB_FILE):
    df_init = pd.DataFrame(columns=["usuario", "eco_puntos", "departamento", "sede"])
    df_init.to_csv(DB_FILE, index=False)

# -------------------------------------------------------
# CARGAR BASE DE DATOS
# -------------------------------------------------------
df_users = pd.read_csv(DB_FILE)

# -------------------------------------------------------
# CABECERA CON LOGOS
# -------------------------------------------------------
st.markdown("""
    <div style='background-color:#E8F5E9; padding:15px; border-radius:10px; display:flex; align-items:center; justify-content:space-between;'>
        <img src="https://i.pinimg.com/280x280_RS/03/23/c7/0323c7a2425e7ffe1b82344c8a413518.jpg" width="100">
        <h2 style='color:#2E7D32; margin: 0;'>🌿 GreenHR - Plataforma Digital Sostenible</h2>
        <img src="https://logos-world.net/wp-content/uploads/2024/11/UPN-Logo.jpg" width="200">
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <p style='color:#2E7D32; font-size:16px;'>
    Bienvenido a GreenHR, la plataforma digital de la Universidad Privada del Norte para promover la sostenibilidad en nuestros procesos.<br>
    Únete a nuestro compromiso con el planeta reduciendo papel, ahorrando recursos y sumando eco-puntos.<br>
    ¡Juntos generamos un impacto positivo!
    </p>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------
if "usuario" not in st.session_state:
    st.session_state.usuario = None
    st.session_state.departamento = None
    st.session_state.sede = None

# -------------------------------------------------------
# FORMULARIO DE INGRESO
# -------------------------------------------------------
if st.session_state.usuario is None:
    with st.form("form_user"):
        usuario = st.text_input("👤 Ingresa tu nombre o correo:")

        departamento = st.selectbox(
            "🏢 Departamento / Área:",
            [
                "-",
                "Recursos Humanos",
                "Académico",
                "Bienestar Universitario",
                "Comunicaciones",
                "Finanzas",
                "Marketing",
                "Logística",
                "Tecnología de la Información (TI)",
                "Dirección General"
            ]
        )

        sede = st.selectbox(
            "📍 Sede:",
            [
                "-",
                "Los Olivos",
                "Comas",
                "Trujillo",
                "Cajamarca",
                "Lima Norte",
                "Chiclayo"
            ]
        )

        submitted = st.form_submit_button("Ingresar")

    if submitted and usuario and departamento != "-" and sede != "-":
        st.session_state.usuario = usuario
        st.session_state.departamento = departamento
        st.session_state.sede = sede

        if usuario not in df_users["usuario"].values:
            new_row = pd.DataFrame(
                [[usuario, 0, departamento, sede]],
                columns=["usuario", "eco_puntos", "departamento", "sede"]
            )
            df_users = pd.concat([df_users, new_row], ignore_index=True)
            df_users.to_csv(DB_FILE, index=False)

else:
    usuario = st.session_state.usuario
    departamento = st.session_state.departamento
    sede = st.session_state.sede

    df_users = pd.read_csv(DB_FILE)
    puntos_actuales = int(df_users[df_users["usuario"] == usuario]["eco_puntos"].values[0])

    # SIDEBAR
    st.sidebar.image(
        "https://i.pinimg.com/280x280_RS/03/23/c7/0323c7a2425e7ffe1b82344c8a413518.jpg",
        width=100
    )
    st.sidebar.title("🌿 GreenHR Panel")

    badge = "🌱 Eco-Novato"
    if puntos_actuales >= 500:
        badge = "🥇 Guardián del Planeta"
    elif puntos_actuales >= 100:
        badge = "🥈 Eco-Avanzado"

    st.sidebar.markdown(f"""
    👤 **Usuario:** {usuario}  
    🏢 **Departamento:** {departamento}  
    📍 **Sede:** {sede}  
    ⭐ **Eco-puntos:** {puntos_actuales}  
    🏅 **Badge:** {badge}
    """)

    st.sidebar.markdown("---")
    st.sidebar.markdown("✅ **Tips de Sostenibilidad**")
    st.sidebar.info("♻️ Imprime solo lo necesario.")
    st.sidebar.info("💧 Ahorra agua cerrando bien los grifos.")
    st.sidebar.info("🌳 Planta un árbol cada año.")
    st.sidebar.markdown("---")

    if st.sidebar.button("🔒 Cerrar Sesión"):
        for key in st.session_state.keys():
            st.session_state[key] = None
        st.experimental_rerun()

    # -------------------------------------------------------
    # DASHBOARD METRICS
    # -------------------------------------------------------
    st.markdown("## 🌍 Impacto Global GreenHR")

    total_eco_puntos = df_users["eco_puntos"].sum()
    total_paginas = total_eco_puntos / 10
    total_co2 = total_paginas * 5
    total_agua = total_paginas * 10
    total_arboles = total_paginas / 8333
    total_dinero = total_paginas * 0.05

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🌳 Árboles salvados", f"{total_arboles:.2f}")
    with col2:
        st.metric("💧 Litros de Agua Ahorrados", f"{total_agua:.2f}")
    with col3:
        st.metric("🌿 CO₂ Evitado (g)", f"{total_co2:.2f}")
    with col4:
        st.metric("💰 Dinero Ahorrado (S/)", f"{total_dinero:.2f}")

    st.markdown("---")

    # -------------------------------------------------------
    # TABS
    # -------------------------------------------------------
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📄 Documentos",
        "📚 Biblioteca Digital",
        "🎥 Videos",
        "🧩 Quiz Verde",
        "🏆 Ranking",
        "📊 Reportes Globales"
    ])

    # TAB 1: Subir Documentos
    with tab1:
        st.subheader("📄 Subir documento PDF")

        uploaded_file = st.file_uploader("Selecciona tu archivo PDF", type=["pdf"])

        if uploaded_file:
            reader = pypdf.PdfReader(uploaded_file)
            num_pages = len(reader.pages)

            co2 = num_pages * 5
            agua = num_pages * 10
            arboles = num_pages / 8333
            dinero = num_pages * 0.05
            eco_puntos = num_pages * 10

            st.success(f"✅ Tu PDF tiene {num_pages} páginas.")
            st.info(f"🌿 Ahorras **{co2} g** de CO₂")
            st.info(f"💧 Ahorras **{agua} litros** de agua")
            st.info(f"🌳 Salvaste **{arboles:.4f} árboles**")
            st.info(f"💰 Ahorro estimado: **S/ {dinero:.2f}**")
            st.success(f"Ganaste **{eco_puntos} eco-puntos** 🎉")

            df_users.loc[df_users["usuario"] == usuario, "eco_puntos"] += eco_puntos
            df_users.to_csv(DB_FILE, index=False)

            st.subheader("🔎 Impacto Ambiental Evitado")

            labels = ["CO₂ (g)", "Agua (L)", "Árboles", "Dinero (S/)"]
            values = [co2, agua, arboles, dinero]
            colors = ["#81C784", "#64B5F6", "#388E3C", "#FFD54F"]

            fig, ax = plt.subplots()
            ax.bar(labels, values, color=colors)
            ax.set_title("Impacto Ambiental Evitado")
            st.pyplot(fig)

    # TAB 2: Biblioteca Digital
    with tab2:
        st.subheader("📚 Biblioteca Digital GreenHR")

        uploaded_file = st.file_uploader("Sube un archivo PDF a la biblioteca", type=["pdf"], key="biblioteca")

        if uploaded_file:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ Archivo **{uploaded_file.name}** guardado exitosamente.")
            df_users.loc[df_users["usuario"] == usuario, "eco_puntos"] += 50
            df_users.to_csv(DB_FILE, index=False)
            st.info("🎉 ¡Ganaste 50 eco-puntos por compartir conocimiento!")

        file_list = os.listdir(UPLOAD_FOLDER)

        if file_list:
            st.write("📚 **Archivos Disponibles en la Biblioteca:**")
            for file_name in file_list:
                file_path = os.path.join(UPLOAD_FOLDER, file_name)
                with open(file_path, "rb") as f:
                    st.download_button(
                        label=f"📥 Descargar {file_name}",
                        data=f,
                        file_name=file_name,
                        mime="application/pdf"
                    )
        else:
            st.info("❗ No hay archivos en la biblioteca todavía.")

    # TAB 3: Videos
    with tab3:
        st.subheader("🎥 Videos inspiradores sobre sostenibilidad")

        lista_videos = [
            {
                "titulo": "¿Qué es sostenibilidad?",
                "link": "https://youtu.be/5yCsjASSd1M?si=PEM0iAGbFScPYgf1"
            },
            {
                "titulo": "Identificar tachos según color (residuos sólidos)",
                "link": "https://youtu.be/0i99_Lkvjm0?si=Fr72Z_94uwGueaYS"
            },
            {
                "titulo": "Cortometraje Lemon - daño ambiental a animales",
                "link": "https://youtu.be/c8c0sYQ87m8?si=sojhByBmDpIWY2hp"
            }
        ]

        st.write("✅ Videos recomendados para ti:")

        for video in lista_videos:
            st.write(f"### 🎬 {video['titulo']}")
            st.video(video["link"])
            if st.button(f"✅ He visto: {video['titulo']}"):
                puntos_video = 50
                st.success(f"¡Has ganado {puntos_video} eco-puntos por ver este video!")
                df_users.loc[df_users["usuario"] == usuario, "eco_puntos"] += puntos_video
                df_users.to_csv(DB_FILE, index=False)

    # TAB 4: Quiz Verde
    with tab4:
        st.subheader("🧩 ¡Juega y gana eco-puntos!")

        preguntas = [
            {
                "pregunta": "¿Cuánta agua se gasta para producir una hoja de papel?",
                "opciones": ["1 litro", "10 litros", "50 litros"],
                "respuesta": "10 litros"
            },
            {
                "pregunta": "¿Cuántos árboles se salvan al evitar 8,333 hojas?",
                "opciones": ["1 árbol", "5 árboles", "10 árboles"],
                "respuesta": "1 árbol"
            },
            {
                "pregunta": "¿Qué es más sostenible?",
                "opciones": ["Imprimir mucho", "Usar PDF", "Tirar papel"],
                "respuesta": "Usar PDF"
            }
        ]

        pregunta = random.choice(preguntas)
        st.write(pregunta["pregunta"])
        eleccion = st.radio("Elige una respuesta:", pregunta["opciones"])

        if st.button("Responder"):
            if eleccion == pregunta["respuesta"]:
                st.success("✅ ¡Correcto! Ganaste 20 eco-puntos 🌟")
                df_users.loc[df_users["usuario"] == usuario, "eco_puntos"] += 20
                df_users.to_csv(DB_FILE, index=False)
            else:
                st.error("❌ Respuesta incorrecta. ¡Sigue aprendiendo!")

    # TAB 5: Ranking
    with tab5:
        st.subheader("🏆 Ranking Ecológico")

        df_users = pd.read_csv(DB_FILE)

        df_rank = df_users.sort_values("eco_puntos", ascending=False).reset_index(drop=True)
        st.dataframe(df_rank, use_container_width=True)

        puntos_finales = int(df_users[df_users["usuario"] == usuario]["eco_puntos"].values[0])
        st.info(f"🌿 Ahora tienes un total de **{puntos_finales} eco-puntos.**")

    # TAB 6: Reportes Globales
    with tab6:
        st.subheader("📊 Reportes Globales de Ahorro")

        grouped = df_users.groupby("departamento")["eco_puntos"].sum().reset_index()
        grouped["paginas"] = grouped["eco_puntos"] / 10
        grouped["co2"] = grouped["paginas"] * 5
        grouped["agua"] = grouped["paginas"] * 10
        grouped["arboles"] = grouped["paginas"] / 8333
        grouped["dinero"] = grouped["paginas"] * 0.05

        st.write("### 🌿 Ahorro por Departamento")
        st.dataframe(grouped[["departamento", "co2", "agua", "arboles", "dinero"]])

        fig, ax = plt.subplots(figsize=(8,4))
        ax.bar(grouped["departamento"], grouped["co2"], color="#81C784")
        ax.set_title("CO₂ Evitado por Departamento (g)")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

        grouped_sede = df_users.groupby("sede")["eco_puntos"].sum().reset_index()
        grouped_sede["paginas"] = grouped_sede["eco_puntos"] / 10
        grouped_sede["co2"] = grouped_sede["paginas"] * 5

        st.write("### 🌍 Ahorro por Sede")
        st.dataframe(grouped_sede[["sede", "co2"]])

        fig2, ax2 = plt.subplots(figsize=(8,4))
        ax2.bar(grouped_sede["sede"], grouped_sede["co2"], color="#64B5F6")
        ax2.set_title("CO₂ Evitado por Sede (g)")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig2)

    
