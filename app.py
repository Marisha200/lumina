import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Lumina", page_icon="✨")
st.title("✨ Lumina")

# 1. Configuración de API Key
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Falta la API Key en los Secrets.")
    st.stop()

# 2. Selección de Modelo (AQUÍ ESTÁ LA SOLUCIÓN)
# Intentamos conectar con el modelo Flash
nombre_modelo = "gemini-1.5-flash"

try:
    model = genai.GenerativeModel(nombre_modelo)
    # Hacemos una prueba silenciosa para ver si conecta
    test = model.generate_content("test")
except Exception as e:
    # SI FALLA, mostramos ayuda en pantalla para saber qué pasa
    st.warning(f"No pudimos conectar con '{nombre_modelo}'.")
    st.info("Buscando modelos disponibles para tu clave...")
    
    try:
        st.write("Estos son los modelos que Google permite usar con tu clave:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                st.code(m.name) # Te mostrará nombres como models/gemini-pro
    except:
        st.error("Error grave: Tu API Key no parece funcionar o no tiene permisos.")
    
    st.stop() # Detenemos la app hasta que se arregle el modelo

# 3. El Chat (Solo carga si lo de arriba funcionó)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! ¿En qué te ayudo con Lumina?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error respondiendo: {e}")
