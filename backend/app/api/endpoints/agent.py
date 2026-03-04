from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import PermitExtractionResponse, SocialExtractionResponse, CommitmentExtractionResponse
from app.services.gemini_service import extract_permit_data, extract_social_data, extract_commitment_data

router = APIRouter()

@router.post("/extract-permit", response_model=PermitExtractionResponse)
async def extract_permit(file: UploadFile = File(...)):
    """
    Recibe un PDF o Imagen y extrae los campos clave usando el Agente IA.
    """
    if not file.content_type.startswith("image/") and file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solamente se permiten archivos PDF o Imágenes.")
    
    contents = await file.read()
    
    try:
        data = await extract_permit_data(contents, file.content_type)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract-commitment", response_model=CommitmentExtractionResponse)
async def extract_commitment(file: UploadFile = File(...)):
    """
    Recibe un PDF o Imagen (RCA o EIA) y extrae datos específicos de un COMPROMISO u obligación de hacer, mapeándolo al diseño del formulario UI.
    """
    if not file.content_type.startswith("image/") and file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solamente se permiten archivos PDF o Imágenes.")
    
    contents = await file.read()
    
    try:
        data = await extract_commitment_data(contents, file.content_type)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract-social", response_model=SocialExtractionResponse)
async def extract_social(file: UploadFile = File(...)):
    """
    Recibe un PDF o Imagen (ej. Acta de Asamblea) y extrae detalles del compromiso social usando el Agente IA.
    """
    if not file.content_type.startswith("image/") and file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solamente se permiten archivos PDF o Imágenes.")
    
    contents = await file.read()
    
    try:
        data = await extract_social_data(contents, file.content_type)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
