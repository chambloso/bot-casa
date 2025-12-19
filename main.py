import random
import requests
import os
import pytz
from datetime import datetime

# --- CONFIGURACIÓN ---
PHONE_NUMBER = os.environ.get('PHONE_NUMBER') 
API_KEY = os.environ.get('API_KEY')           

# Nombres personalizados
NOMBRE_ELLA = "Alison"
NOMBRE_EL = "Bastián"

# Lista de tareas con peso (1: Rápido, 3: Pajero/Lento)
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
    url = f"https://api.callmebot.com/whatsapp.php?phone={PHONE_NUMBER}&text={mensaje}&apikey={API_KEY}"
    try:
        requests.get(url, timeout=10)
        print("✅ Enviado.")
    except Exception as e:
        print(f"❌ Error: {e}")

def run():
    random.shuffle(TAREAS_BASE)
    asignaciones = {NOMBRE_ELLA: [], NOMBRE_EL: []}
    peso_ella, peso_el = 0, 0
    
    # Algoritmo de reparto equitativo
    for tarea in TAREAS_BASE:
        # Asignamos al que tenga menos carga acumulada
        if peso_el <= peso_ella:
            asignaciones[NOMBRE_EL].append(tarea)
            peso_el += tarea['peso']
        else:
            asignaciones[NOMBRE_ELLA].append(tarea)
            peso_ella += tarea['peso']

    # Fecha Chile
    tz_chile = pytz.timezone('Chile/Continental')
    fecha = datetime.now(tz_chile).strftime("%d/%m")
    
    # --- CONSTRUCCIÓN DEL MENSAJE ---
    # Usamos %0A para saltos de línea en la URL
    
    msg = f"✨ *PLAN DE EQUIPO - {fecha}* ✨%0A" 
    msg += f"Hola chicos, aquí está la organización justa de hoy:%0A%0A"
    
    # Sección Alison
    msg += f"*👸 {NOMBRE_ELLA} ({peso_ella} pts):*%0A"
    for t in asignaciones[NOMBRE_ELLA]:
        msg += f"🔸 {t['nombre']}%0A"
        
    # Sección Bastián
    msg += f"%0A*🤴 {NOMBRE_EL} ({peso_el} pts):*%0A"
    for t in asignaciones[NOMBRE_EL]:
        msg += f"🔹 {t['nombre']}%0A"
        
    msg += "%0A_💪 ¡Vamos equipo! Organizados todo sale mejor._"
    
    return msg

if __name__ == "__main__":
    if not PHONE_NUMBER or not API_KEY:
        print("❌ Faltan credenciales.")
    else:
        enviar_whatsapp(run())