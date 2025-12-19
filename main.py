import random
import requests
import os
import pytz
from datetime import datetime
import sys

# --- CONFIGURACIÓN ---
# Obtenemos las variables y limpiamos espacios por si acaso
PHONE_NUMBER = os.environ.get('PHONE_NUMBER', '').strip()
API_KEY = os.environ.get('API_KEY', '').strip()

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
    {"nombre": "🛏️ Ordenar Pieza", "peso": 1}
]

def enviar_whatsapp(mensaje):
    # --- CAMBIO IMPORTANTE: USAMOS LA API DE TEXTMEBOT ---
    url = "https://api.textmebot.com/send.php"
    
    # Aseguramos que el número tenga el formato internacional (+569...)
    # Si guardaste '569...' en el secreto, le agregamos el '+' al principio.
    numero_final = PHONE_NUMBER
    if not numero_final.startswith("+"):
        numero_final = "+" + numero_final
        
    payload = {
        "recipient": numero_final,  # TextMeBot usa 'recipient', no 'phone'
        "text": mensaje,
        "apikey": API_KEY
    }
    
    print(f"📡 Enviando a TextMeBot ({numero_final})...")
    
    try:
        # TextMeBot suele responder texto plano, no siempre JSON
        resp = requests.get(url, params=payload, timeout=20)
        
        # Verificamos si salió bien (TextMeBot suele decir "OK" o devolver 200)
        if resp.status_code == 200:
            print("✅ ¡MENSAJE ENVIADO! (Status 200)")
            print(f"Respuesta del servidor: {resp.text}")
        else:
            print(f"⚠️ ERROR: El servidor respondió {resp.status_code}")
            print(f"Detalle: {resp.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
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
    
    msg = f"✨ *PLAN DE EQUIPO - {fecha}* ✨\n" 
    msg += f"Hola chicos, aquí está la organización justa de hoy:\n\n"
    
    msg += f"*👸 {NOMBRE_ELLA} ({peso_ella} pts):*\n"
    for t in asignaciones[NOMBRE_ELLA]:
        msg += f"🔸 {t['nombre']}\n"
        
    msg += f"\n*🤴 {NOMBRE_EL} ({peso_el} pts):*\n"
    for t in asignaciones[NOMBRE_EL]:
        msg += f"🔹 {t['nombre']}\n"
        
    msg += "\n_💪 ¡Vamos Michitos!_"
    return msg

if __name__ == "__main__":
    if not PHONE_NUMBER or not API_KEY:
        print("❌ Faltan credenciales (Secrets).")
        sys.exit(1)
    
    texto = run()
    enviar_whatsapp(texto)
