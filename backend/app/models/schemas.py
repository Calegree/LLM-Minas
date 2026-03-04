from pydantic import BaseModel, Field
from typing import Optional

class FieldWithInference(BaseModel):
    value: str
    is_inferred: bool = False

class PermitExtractionResponse(BaseModel):
    nombre_permiso: FieldWithInference = Field(..., description="El título del permiso, ej. 'Monitoreo de Calidad de Aire Fase I'")
    referencia_legal: FieldWithInference = Field(..., description="Número en el encabezado oficial, ej. 'RCA 245/2018'")
    estado_gestion: FieldWithInference = Field(..., description="Estado de gestión del permiso, ej. 'PENDIENTE' o 'VIGENTE'")
    autoridad_competente: FieldWithInference = Field(..., description="Entidad que emite, ej. 'SEREMI SALUD'")
    gerencia_responsable: FieldWithInference = Field(..., description="Gerencia a cargo (Minas, Asuntos Sociales, etc.)")
    contratista_sugerido: FieldWithInference = Field(..., description="Contratista deducido para el trabajo, ej. 'GESTIONA'")
    tipo_permiso: FieldWithInference = Field(..., description="Tipo de permiso, ej. 'Ambiental', 'Sectorial'")
    responsable: FieldWithInference = Field(..., description="Nombre del empleado responsable")
    periodo: FieldWithInference = Field(..., description="Año o periodo anual que cubre, ej. '2024'")
    vencimiento: FieldWithInference = Field(..., description="Fecha de vencimiento calculada o explícita, ej. '15 Oct 2024'")
    vigencia_acotada: FieldWithInference = Field(..., description="'Verdadero' si tiene fecha de vencimiento o fin, 'Falso' si es permanente o no aplica")

class SocialExtractionResponse(BaseModel):
    compromiso: FieldWithInference = Field(..., description="Descripción del compromiso, ej. 'Pavimentar 15 km de la Ruta C-34'")
    estado_sugerido: FieldWithInference = Field(..., description="Estado inicial sugerido, ej. 'En Elaboración'")
    fecha_limite: FieldWithInference = Field(..., description="Fecha límite si la hay")
    responsables: FieldWithInference = Field(..., description="Personas o entidades responsables")

class CommitmentExtractionResponse(BaseModel):
    id_compromiso: FieldWithInference = Field(..., description="ID del compromiso, ej. 'RCA-123' o correlativo")
    descripcion_compromiso: FieldWithInference = Field(..., description="Detalle de la obligación normativa que impone el EIA o la RCA")
    origen_fuente: FieldWithInference = Field(..., description="Origen o fuente, ej. 'RCA 254/2018' o EIA")
    tipo_compromiso: FieldWithInference = Field(..., description="Tipo de compromiso, ej. 'Ambiental', 'Social', 'Legal'")
    gerencia_responsable: FieldWithInference = Field(..., description="Gerencia a cargo o sugerida, ej. 'Mina'")
    area_instalacion: FieldWithInference = Field(..., description="Lugar donde aplica, ej. 'Rajo Norte, Tranque'")
    empresa_contratista: FieldWithInference = Field(..., description="Tercero o contratista sugerido")
    responsable: FieldWithInference = Field(..., description="Nombre del empleado encargado")
    estado_inicial: FieldWithInference = Field(..., description="Estado del compromiso, ej. 'Pendiente', 'Cumplido'")
    autoridad_fiscalizadora: FieldWithInference = Field(..., description="Entidad que fiscaliza, ej. 'SMA', 'DGA', 'SEA'")
    vigencia_acotada: FieldWithInference = Field(..., description="'Verdadero' si tiene fecha de vencimiento o fin, 'Falso' si es permanente")
    fecha_vencimiento: FieldWithInference = Field(..., description="Fecha si hay un plazo estipulado")
