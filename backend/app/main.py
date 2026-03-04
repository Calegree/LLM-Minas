from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from app.api.endpoints import agent
from app.services.scheduler_service import evaluate_and_trigger_alerts

# Inicializar APScheduler
scheduler = BackgroundScheduler()
from app.api.endpoints import agent

app = FastAPI(
    title="Agente IA Minero API",
    description="API para extracción y autocompletado de permisos mineros usando IA",
    version="1.0.0",
)

@app.on_event("startup")
def start_scheduler():
    # En un entorno real, ejecutaría diariamente a medianoche: trigger='cron', hour=0, minute=0
    # Por ahora, programamos para que corra cada 12 horas en background
    scheduler.add_job(evaluate_and_trigger_alerts, 'interval', hours=12)
    scheduler.start()
    print("[SERVER] 🚀 Sistema de Alertas Proactivas Iniciado (Cron Job).")

@app.on_event("shutdown")
def stop_scheduler():
    scheduler.shutdown()
    print("[SERVER] 🛑 Sistema de Alertas Proactivas Detenido.")

# Configurar CORS para permitir que React (Vite) se conecte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica el dominio ej. "http://localhost:5173"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(agent.router, prefix="/api/v1/agent", tags=["agent"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API del Agente IA Minero"}

@app.post("/api/v1/trigger-alerts-demo", tags=["demo"])
def trigger_alerts_demo(background_tasks: BackgroundTasks):
    """
    Endpoint manual para que el usuario pueda forzar la ejecución del "Cerebro Proactivo" 
    y ver el resultado de las Alertas Rojas en la terminal de inmediato.
    """
    background_tasks.add_task(evaluate_and_trigger_alerts)
    return {"message": "¡Auditoría Proactiva iniciada! Revisa la terminal de Python (Visual Studio Code o PowerShell) para ver los logs de las Alertas (T-30, T-7, T-1)."}
