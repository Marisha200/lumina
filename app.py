import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mapa de Sueños 2026", page_icon="✨")
st.title("✨ Asistente de Sueños 2026")

# --- API KEY ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Falta la API Key.")
    st.stop()

# --- MODELO CLÁSICO (El que funciona siempre) ---
# Usamos 'gemini-pro' porque es compatible con versiones anteriores
try:
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Error cargando modelo: {e}")
    st.stop()

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Cuéntame tus ideas para 2026..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
