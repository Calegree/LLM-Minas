from pydantic import BaseModel, Field
from typing import Optional

class FieldWithInference(BaseModel):
    value: str
    is_inferred: bool = False

class PermitExtractionResponse(BaseModel):
    nombre_permiso: FieldWithInference = Field(..., description="El título del permiso, ej. 'Monitoreo de Calidad de Aire Fase I'")
    referencia_legal: FieldWithInference = Field(..., description="Número en el encabezado oficial, ej. 'RCA 245/2018'")
    autoridad_competente: FieldWithInference = Field(..., description="Entidad que emite, ej. 'SEREMI SALUD'")
    vencimiento: FieldWithInference = Field(..., description="Fecha de vencimiento calculada o explícita, ej. '15 Oct 2024'")
    gerencia_responsable: FieldWithInference = Field(..., description="Gerencia a cargo (Minas, Asuntos Sociales, etc.)")
    contratista_sugerido: FieldWithInference = Field(..., description="Contratista deducido para el trabajo, ej. 'GESTIONA'")
    responsable: FieldWithInference = Field(..., description="Nombre del empleado responsable")

class SocialExtractionResponse(BaseModel):
    compromiso: FieldWithInference = Field(..., description="Descripción del compromiso, ej. 'Pavimentar 15 km de la Ruta C-34'")
    estado_sugerido: FieldWithInference = Field(..., description="Estado inicial sugerido, ej. 'En Elaboración'")
    fecha_limite: FieldWithInference = Field(..., description="Fecha límite si la hay")
    responsables: FieldWithInference = Field(..., description="Personas o entidades responsables")
