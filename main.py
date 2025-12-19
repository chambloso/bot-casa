import random
import requests
import os
import pytz
from datetime import datetime
import sys
import time

# --- CONFIGURACIÓN ---
# Obtenemos la API Key de los secretos del repositorio
API_KEY = os.environ.get('API_KEY', '').strip()

# Configuración de nombres
NOMBRE_ELLA = "Alison"
NOMBRE_EL = "Bastián"

# Lista de tareas y su "peso" (esfuerzo)
TAREAS_BASE = [
    {"nombre": "🍳 Cocinar Almuerzo", "peso": 3},
    {"nombre": "🥗 Hacer la Oncesita", "peso": 2},
    {"nombre": "🍽️ Lavar Loza (Día)", "peso": 2},
    {"nombre": "🌙 Lavar Loza (Noche)", "peso": 2},
    {"nombre": "🚽 Limpiar Baño", "peso": 3},
    {"nombre": "🗑️ Sacar Basura", "peso": 1},
    {"nombre": "🧹 Barrer", "peso": 2},
    {"nombre": "🛏️ Ordenar Pieza", "peso": 1}
]

def obtener_numeros():
    """Recupera los números de teléfono de las variables de entorno."""
    numeros = []
    # Número tuyo
    if os.environ.get('PHONE_NUMBER'): 
        numeros.append(os.environ.get('PHONE_NUMBER').strip())
    # Número de ella
    if os.environ.get('PHONE_NUMBER_ELLA'):
        numeros.append(os.environ.get('PHONE_NUMBER_ELLA').strip())
    return numeros

def enviar_whatsapp(mensaje, destinatario):
    """Envía el mensaje usando la API de TextMeBot."""
    url = "https://api.textmebot.com/send.php"
    
    # Asegurar formato internacional (+)
    numero_final = destinatario
    if not numero_final.startswith("+"):
        numero_final = "+" + numero_final
        
    payload = {
        "recipient": numero_final,
        "text": mensaje,
        "apikey": API_KEY,
        "json": "yes"  # Pedimos respuesta en JSON para mejor lectura
    }
    
    print(f"📡 Enviando a {numero_final}...")
    
    try:
        resp = requests.get(url, params=payload, timeout=20)
        
        if resp.status_code == 200:
            print("✅ ¡ENVIADO CORRECTAMENTE!")
        else:
            print(f"⚠️ El servidor respondió con error: {resp.status_code}")
            print(f"Detalle: {resp.text}")
            
    except Exception as e:
        print(f"❌ Error crítico de conexión: {e}")

def generar_plan():
    """Distribuye las tareas equitativamente según el peso."""
    random.shuffle(TAREAS_BASE)
    asignaciones = {NOMBRE_ELLA: [], NOMBRE_EL: []}
    peso_ella, peso_el = 0, 0
    
    # Algoritmo de distribución equitativa
    for tarea in TAREAS_BASE:
        # Se asigna la tarea a quien tenga menos carga acumulada
        if peso_el <= peso_ella:
            asignaciones[NOMBRE_EL].append(tarea)
            peso_el += tarea['peso']
        else:
            asignaciones[NOMBRE_ELLA].append(tarea)
            peso_ella += tarea['peso']

    # Obtener fecha actual en Chile
    tz_chile = pytz.timezone('Chile/Continental')
    fecha = datetime.now(tz_chile).strftime("%d/%m")
    
    # Construcción del mensaje
    msg = f"✨ *PLAN DE EQUIPO - {fecha}* ✨\n" 
    msg += f"Hola equipo, la IA organizó la casa hoy para que todo sea justo:\n\n"
    
    msg += f"*👸 {NOMBRE_ELLA} ({peso_ella} pts):*\n"
    for t in asignaciones[NOMBRE_ELLA]:
        msg += f"🔸 {t['nombre']}\n"
        
    msg += f"\n*🤴 {NOMBRE_EL} ({peso_el} pts):*\n"
    for t in asignaciones[NOMBRE_EL]:
        msg += f"🔹 {t['nombre']}\n"
        
    msg += "\n_🤖 Atte. El Bot de la MichiCasa_"
    
    return msg

def main():
    # 1. Validaciones iniciales
    if not API_KEY:
        print("❌ Error: No se encontró la API_KEY en los Secrets.")
        sys.exit(1)
    
    lista_numeros = obtener_numeros()
    if not lista_numeros:
        print("❌ Error: No hay números configurados en los Secrets.")
        sys.exit(1)

    # 2. Generar el texto
    texto_final = generar_plan()
    print("--- MENSAJE GENERADO ---")
    print(texto_final)
    print("------------------------")
    
    # 3. Enviar mensajes con PAUSA DE SEGURIDAD
    for i, num in enumerate(lista_numeros):
        enviar_whatsapp(texto_final, num)
        
        # Si no es el último número, hacemos la pausa obligatoria
        if i < len(lista_numeros) - 1:
            print("⏳ Esperando 6 segundos por seguridad de la API...")
            time.sleep(6) 

if __name__ == "__main__":
    main()
