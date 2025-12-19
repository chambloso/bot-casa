import random
import requests
import os
import pytz
from datetime import datetime
import sys

# --- CONFIGURACIÓN BLINDADA ---
# .strip() elimina espacios en blanco y 'enters' que se hayan colado al copiar
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
    {"nombre": "🛏️ Ordenar Pieza", "peso": 1},
    {"nombre": "🐈 Mascotas/Arenero", "peso": 1}
]

def enviar_whatsapp(mensaje):
    # Imprimir diagnóstico (Ocultando datos sensibles por seguridad)
    print("--- 🔍 DIAGNÓSTICO DE VARIABLES ---")
    if not API_KEY:
        print("❌ ERROR CRÍTICO: La API_KEY está vacía. Revisa los Secrets de GitHub.")
        sys.exit(1)
        
    largo_key = len(API_KEY)
    inicio_key = API_KEY[:2] if largo_key > 2 else "??"
    fin_key = API_KEY[-2:] if largo_key > 2 else "??"
    
    print(f"✅ API Key detectada: Comienza con '{inicio_key}...', termina con '...{fin_key}' (Largo: {largo_key})")
    print(f"✅ Teléfono detectado: {PHONE_NUMBER}")
    print("-------------------------------------")

    url = "https://api.callmebot.com/whatsapp.php"
    payload = {
        "phone": PHONE_NUMBER,
        "text": mensaje,
        "apikey": API_KEY
    }
    
    print(f"📡 Enviando petición al servidor...")
    
    try:
        resp = requests.get(url, params=payload, timeout=20)
        
        if resp.status_code == 200 and "Message queued" in resp.text:
            print("✅ ¡ÉXITO TOTAL! Mensaje entregado.")
            print(f"Respuesta: {resp.text}")
        else:
            print(f"⚠️ EL SERVIDOR RECHAZÓ LA CLAVE.")
            print(f"Código: {resp.status_code}")
            print(f"Error detallado: {resp.text}")
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
        
    msg += "\n_💪 ¡Vamos equipo!_"
    return msg

if __name__ == "__main__":
    texto = run()
    enviar_whatsapp(texto)
