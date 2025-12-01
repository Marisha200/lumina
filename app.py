import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Lumina", page_icon="✨")

st.title("✨ Lumina Oracle")
st.write("Estoy aquí para ayudarte a crear tu mapa y definir tus propósitos.")

# 2. Conexión segura con Google
# Busca la clave en la "caja fuerte" de Streamlit (Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Falta la API Key. Por favor, configúrala en los 'Secrets' de Streamlit.")
    st.stop()

# 3. Configuración del modelo (AQUÍ ESTÁ EL CAMBIO IMPORTANTE)
# Usamos 'gemini-1.5-flash' que es rápido y estable
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error al cargar el modelo: {e}")

# 4. Historial del chat (Memoria)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores en la pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. El chat: Capturar lo que escribes y responder
if prompt := st.chat_input("Escribe tu idea o pregunta aquí..."):
    # A. Mostrar tu mensaje
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # B. Generar respuesta de la IA
    with st.chat_message("assistant"):
        message_placeholder = st.empty() # Espacio vacío mientras piensa
        try:
            # Enviamos el historial para que tenga contexto (opcional, aquí envío solo el prompt para simplificar errores)
            response = model.generate_content(prompt)
            
            # Mostrar la respuesta
            message_placeholder.markdown(response.text)
            
            # Guardar en memoria
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            message_placeholder.error(f"Ocurrió un error: {e}")
