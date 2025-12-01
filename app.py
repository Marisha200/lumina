import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Lumina", page_icon="✨")
st.title("✨ Lumina")
st.write("Cuéntame tus metas y diseñemos juntos tu 2026.")

# --- CONEXIÓN CON GOOGLE (SEGURIDAD) ---
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Falta la API Key en los Secrets de Streamlit.")
    st.stop()

# --- CEREBRO DE LA IA ---
# Usamos el modelo exacto que encontraste en la lista
# Nota: Le quitamos el prefijo 'models/' para que funcione mejor
nombre_modelo = "gemini-1.5-flash"

try:
    model = genai.GenerativeModel(nombre_modelo)
except Exception as e:
    st.error(f"Error al cargar el modelo {nombre_modelo}: {e}")
    st.stop()

# --- MEMORIA DEL CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial en pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INTERACCIÓN ---
if prompt := st.chat_input("Escribe aquí tu idea, sueño o duda..."):
    # 1. Mostrar lo que tú escribiste
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generar respuesta de la IA
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Enviamos el mensaje a Google
            response = model.generate_content(prompt)
            
            # Mostramos la respuesta
            message_placeholder.markdown(response.text)
            
            # Guardamos en memoria
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            message_placeholder.error(f"Error de conexión: {e}")
