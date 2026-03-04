import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Cargar parámetros de días de alerta desde el entorno (con defaults)
ALERT_T30 = int(os.environ.get("ALERT_T30", 30))
ALERT_T7 = int(os.environ.get("ALERT_T7", 7))
ALERT_T1 = int(os.environ.get("ALERT_T1", 1))

def simulate_fetch_expiring_commitments():
    """
    Mock de base de datos.
    Simula devolver compromisos o permisos que están pronto a vencer.
    Para propósitos de prueba de concepto, creamos fechas relativas a hoy.
    """
    today = datetime.now()
    return [
        {
            "id": "COMP-001",
            "name": "Reporte de Polvo Semestral",
            "due_date": today + timedelta(days=ALERT_T30),
            "status": "Pendiente",
            "contractor": "DISEP",
            "manager": "Gerencia Mina"
        },
        {
            "id": "COMP-002",
            "name": "Monitoreo de Aguas Claras",
            "due_date": today + timedelta(days=ALERT_T7),
            "status": "Pendiente",
            "contractor": "GESTIONA",
            "manager": "Medioambiente"
        },
        {
            "id": "COMP-003",
            "name": "Entrega Acta Comunidad Coyo",
            "due_date": today + timedelta(days=ALERT_T1),
            "status": "Pendiente",
            "contractor": "N/A",
            "manager": "Asuntos Sociales"
        }
    ]

def evaluate_and_trigger_alerts():
    """
    Lógica periódica que corre todos los días a las 00:00 (o cada minuto en pruebas).
    Cruza los vencimientos actuales con los días configurados.
    """
    print(f"\n[CEREBRO PROACTIVO] 🧠 Iniciando auditoría de plazos...")
    print(f"Parámetros de ventana configurados: T-{ALERT_T30}, T-{ALERT_T7}, T-{ALERT_T1}\n")

    commitments = simulate_fetch_expiring_commitments()
    today = datetime.now().date()

    for commit in commitments:
        due_date = commit['due_date'].date()
        days_left = (due_date - today).days

        # Regla T-30: Pedir reportes iniciales al contratista silenciosamente
        if days_left == ALERT_T30:
            print(f"🟡 [T-30 Días] Compromiso '{commit['name']}':")
            print(f"   => Acción IA: Enviando correo automático y silencioso al Contratista {commit['contractor']} solicitando las evidencias...\n")
            
        # Regla T-7: Auditoría de documentos subidos. Si falta, escalar a Gerencia.
        elif days_left == ALERT_T7:
            print(f"🟠 [T-7 Días] Compromiso '{commit['name']}':")
            print(f"   => Acción IA: Audité la carpeta. Faltan los reportes de IoT del contratista {commit['contractor']}.")
            print(f"   => 🚨 ALERTA ROJA ENVIADA A {commit['manager']}: 'Favor intervenir de inmediato, riesgo de rechazo por informe incompleto'.\n")
            
        # Regla T-1: Último filtro. Si sigue pendiente, SMS a Gerente General.
        elif days_left == ALERT_T1:
            print(f"🔴 [T-1 Días] Compromiso '{commit['name']}':")
            print(f"   => Acción IA: El compromiso sigue estado '{commit['status']}'.")
            print(f"   => 📱 SMS DE EMERGENCIA ENVIADO AL GERENTE GENERAL: 'Riesgo inminente de incumplimiento y multa por {commit['name']}'.\n")
            
    print("[CEREBRO PROACTIVO] ✅ Auditoría finalizada.")

def start_scheduler_service():
    """
    Solo para uso de prueba manual
    """
    evaluate_and_trigger_alerts()
