import random
import requests
import os
import pytz
from datetime import datetime
import sys

# --- CONFIGURACIÓN ---
PHONE_NUMBER = os.environ.get('PHONE_NUMBER') 
API_KEY = os.environ.get('API_KEY')           

NOMBRE_ELLA = "Alison"
NOMBRE_EL = "Bastián"

TAREAS_BASE = [
    {"nombre": "🍳 Cocinar Almuerzo", "peso": 3},
    {"nombre": "🥗 Cocinar Cena", "peso": 2},
    {"nombre": "🍽️ Lavar Loza (Día)", "peso": 2},
    {"nombre": "🌙 Lavar Loza (Noche)", "peso": 2},
    {"nombre": "🚽 Limpiar Baño", "peso": 3},
    {"nombre": "🗑️ Sacar Basura", "peso": 1},
    {"nombre": "🧹 Barrer Áreas Comunes", "peso": 2},
    {"nombre": "🛏️ Ordenar Pieza", "peso": 1},
    {"nombre": "🐈 Mascotas/Arenero", "peso": 1}
]

def enviar_whatsapp(mensaje):
    # Usamos 'params' para que Python codifique espacios y emojis automáticamente
    url = "https://api.callmebot.com/whatsapp.php"
    payload = {
        "phone": PHONE_NUMBER,
        "text": mensaje,
        "apikey": API_KEY
    }
    
    print(f"📡 Enviando a: {PHONE_NUMBER}...")
    
    try:
        resp = requests.get(url, params=payload, timeout=20)
        
        # Verificamos si la API nos dio el dedo arriba o error
        if resp.status_code == 200 and "Message queued" in resp.text:
            print("✅ ¡ÉXITO! Mensaje entregado al bot.")
            print(f"Respuesta del servidor: {resp.text}")
        else:
            print(f"⚠️ ALERTA: El código corrió pero el bot respondió error.")
            print(f"Status Code: {resp.status_code}")
            print(f"Respuesta completa: {resp.text}")
            # Forzamos error para que GitHub se ponga rojo
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error crítico de conexión: {e}")
        sys.exit(1)

def run():
    random.shuffle(TAREAS_BASE)
    asignaciones = {NOMBRE_ELLA: [], NOMBRE_EL: []}
    peso_ella, peso_el = 0, 0
    
    for tarea in TAREAS_BASE:
        if peso_el <= peso_ella:
            asignaciones[NOMBRE_EL].append(tarea)
            peso_el += tarea['peso']
        else:
            asignaciones[NOMBRE_ELLA].append(tarea)
            peso_ella += tarea['peso']

    tz_chile = pytz.timezone('Chile/Continental')
    fecha = datetime.now(tz_chile).strftime("%d/%m")
    
    # Construimos el mensaje normal (sin codigos raros como %0A, Python lo hará solo)
    msg = f"✨ *PLAN DE EQUIPO - {fecha}* ✨\n" 
    msg += f"Hola chicos, aquí está la organización justa de hoy:\n\n"
    
    msg += f"*👸 {NOMBRE_ELLA} ({peso_ella} pts):*\n"
    for t in asignaciones[NOMBRE_ELLA]:
        msg += f"🔸 {t['nombre']}\n"
        
    msg += f"\n*🤴 {NOMBRE_EL} ({peso_el} pts):*\n"
    for t in asignaciones[NOMBRE_EL]:
        msg += f"🔹 {t['nombre']}\n"
        
    msg += "\n_💪 ¡Vamos equipo!_"
    return msg

if __name__ == "__main__":
    if not PHONE_NUMBER or not API_KEY:
        print("❌ Faltan credenciales (Secrets).")
        sys.exit(1)
        
    texto = run()
    enviar_whatsapp(texto)
