import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Mi IA Personal", page_icon="✨")

st.title("✨ Mi Asistente IA")
st.write("Pregúntame lo que quieras sobre Lumina.")

# 2. Conexión segura con Google (La llave NO está aquí, la busca en la caja fuerte)
# Si no hay llave, mostramos un aviso.
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("Falta la API Key. Configúrala en los 'Secrets' de Streamlit.")
    st.stop()

# 3. Configuración del modelo (Gemini)
model = genai.GenerativeModel('gemini-pro')

# 4. Historial del chat (para que recuerde lo que hablan)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. El chat en sí
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Guardar y mostrar lo que tú escribiste
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta de la IA
    with st.chat_message("assistant"):
        try:
            # Aquí enviamos el historial para contexto (simplificado)
            response = model.generate_content(prompt)
            st.markdown(response.text)
            
            # Guardar respuesta de la IA
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
