import streamlit as st #importar la libreria
from groq import Groq

#configuración de la ventana de la web
st.set_page_config(page_title = "Ruffina IA", page_icon= "🐱")

#Titulo de la pagina
st.title("Ruffina IA, una nueva inteligencia")

#Ingreso de dato del usuario
nombre = st.text_input("¿Cuál es tu nombre?")

#Creamos boton con funcionalidad
if st.button("Saludar") :
    st.write(f"¡Hola {nombre}! Bienvenido ¿Puedo ayudarte en algo?")

MODELO = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key = clave_secreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
      model=modelo,
      messages=[{"role": "user", "content": mensajeDeEntrada}],
      stream=True
)

#Simula un historial de mensajes #Siempre se guarda en streamlit
def inicializar_estado(): 
    #Si mensajes no esta en st.session_state
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] #Memoria de mensajes

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar": avatar}
    )

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]): st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height= 400, border= True) 
    with contenedorDelChat: mostrar_historial()        

def configurar_pagina():
    st.title("Miau CHAT") #Titulo
    st.sidebar.title("Configuración") #Menu lateral
    elegirModelo = st.sidebar.selectbox(
        "Elegí un modulo", #titulo
        MODELO, #Opciones del menu
        index = 2 #valorDefecto
    )
    return elegirModelo

def generar_respuestas(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo: 
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content

    return respuesta_completa

def main():
    modelo = configurar_pagina() #Llamamos a la función
    clienteUsuario = crear_usuario_groq()
    inicializar_estado() 
    area_chat()
    mensaje = st.chat_input("Escribí un mensaje: ")
    
    if mensaje:
        actualizar_historial("user", mensaje, "😺")
        
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuestas(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "😸" )
                st.rerun()

if __name__ == "__main__":
    main()