from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import agent

app = FastAPI(
    title="Agente IA Minero API",
    description="API para extracción y autocompletado de permisos mineros usando IA",
    version="1.0.0",
)

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
