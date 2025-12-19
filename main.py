import random
import requests
import os
import pytz
from datetime import datetime
import sys
import time

# --- CONFIGURACIÓN ---
API_KEY = os.environ.get('API_KEY', '').strip()

# Obtenemos los dos números. Si alguno no existe, lo ignora.
NUMEROS = []
if os.environ.get('PHONE_NUMBER'): 
    NUMEROS.append(os.environ.get('PHONE_NUMBER').strip()) # Tu número
if os.environ.get('PHONE_NUMBER_ELLA'):
    NUMEROS.append(os.environ.get('PHONE_NUMBER_ELLA').strip()) # Su número

NOMBRE_ELLA = "Alison"
NOMBRE_EL = "Bastián"

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

def enviar_whatsapp(mensaje, destinatario):
    url = "https://api.textmebot.com/send.php"
    
    # Formato internacional
    numero_final = destinatario
    if not numero_final.startswith("+"):
        numero_final = "+" + numero_final
        
    payload = {
        "recipient": numero_final,
        "text": mensaje,
        "apikey": API_KEY
    }
    
    print(f"📡 Enviando a {numero_final}...")
    
    try:
        resp = requests.get(url, params=payload, timeout=20)
        if resp.status_code == 200:
            print("✅ ¡ENVIADO!")
        else:
            print(f"⚠️ Error enviando a este número: {resp.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

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
    msg += f"Hola equipo, la IA organizó la casa hoy para que nadie pelee:\n\n"
    
    msg += f"*👸 {NOMBRE_ELLA} ({peso_ella} pts):*\n"
    for t in asignaciones[NOMBRE_ELLA]:
        msg += f"🔸 {t['nombre']}\n"
        
    msg += f"\n*🤴 {NOMBRE_EL} ({peso_el} pts):*\n"
    for t in asignaciones[NOMBRE_EL]:
        msg += f"🔹 {t['nombre']}\n"
        
    msg += "\n_🤖 Atte. El Bot de la MichiCasa_"
    return msg

if __name__ == "__main__":
    if not API_KEY:
        print("❌ Faltan credenciales (Secrets).")
        sys.exit(1)
    
    if not NUMEROS:
        print("❌ No hay números configurados.")
        sys.exit(1)

    texto_final = run()
    
    # Enviar a todos los números de la lista
    for num in NUMEROS:
        enviar_whatsapp(texto_final, num)
        time.sleep(2) # Espera 2 segundos entre mensajes para no saturar
