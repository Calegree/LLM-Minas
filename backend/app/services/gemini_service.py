import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from app.models.schemas import PermitExtractionResponse, SocialExtractionResponse, CommitmentExtractionResponse

# Cargar variables desde el archivo .env
load_dotenv()

# Leer API KEY desde variables de entorno
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "dummy_key_for_testing")

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception:
    client = None

PERMIT_INSTRUCTIONS = """
Eres el Asistente Legal experto de una empresa minera. Tu trabajo es extraer información clave de documentos oficiales (Resoluciones Exentas, RCA, etc.) para rellenar un formulario de permisos en la aplicación React.
Extrae los datos solicitados y devuélvelos respetando el esquema JSON especificado.
Si debes adivinar o inferir un dato que no está explícitamente en el texto, debes marcar la propiedad "is_inferred" como true en ese elemento particular.

Reglas Especiales (Prompting Oculto):
- Si el documento habla de polvo o agua, la "gerencia_responsable" debe ser sugerida como "Minas" (con is_inferred en true si no es explícito).
- Si el documento habla de comunidades indígenas, la "gerencia_responsable" debe ser "Gerencia de Asuntos Sociales" (con is_inferred en true si no es explícito).
- Si no encuentras el contratista en el documento, sugiere "GESTIONA" como contratista marcando "is_inferred" como true (es tu deducción basada en historial).
- Si el documento habla de medio ambiente o RCA, el "tipo_permiso" debe sugerirse como "Ambiental".
- Si no encuentras un estado claro en el documento, sugiere "PENDIENTE" en "estado_gestion".
- Infiere el "periodo" al año actual o el año mencionado en el documento si aplica.
- Si el documento no especifica fecha de fin o de vencimiento, establece "vigencia_acotada" como "Falso" y "is_inferred" en true.
"""

SOCIAL_INSTRUCTIONS = """
Eres un Asistente Comunitario experto en sostenibilidad para una empresa minera.
Tu trabajo es leer documentos sociales que pueden ser de tres tipos:
1. Acuerdo Comunitario (o Convenio de Inversión Social)
2. Minuta de Reunión (o Acta de Asamblea)
3. Sección Social de una RCA (Resolución de Calificación Ambiental)

Instrucciones de Extracción:
- Identifica y extrae el compromiso principal o la acción a realizar (Ej: "El titular deberá pavimentar los 15 kilómetros de la Ruta C-34").
- Nombra a las entidades responsables o la contraparte comunitaria.
- Si no logras encontrar el estado actual del compromiso en el texto, sugiere siempre "En Elaboración" con el flag `is_inferred: true`.
- Extrae cualquier fecha límite o plazo mencionado.
"""

COMMITMENT_INSTRUCTIONS = """
Eres el Analista de Cumplimiento experto de una empresa minera.
Tu trabajo es distinguir estrictamente entre un "PERMISO" (una autorización de la autoridad para operar, como SEREMI) y un "COMPROMISO" (una obligación de hacer algo que el proyecto debe cumplir, nacida de una RCA o EIA).
Debes extraer únicamente la información correspondiente a COMPROMISOS (Ej: Pavimentar, financiar, monitorear polvo, reportar aguas). 

Instrucciones de Extracción:
- Extrae la descripción o detalle de la obligación normativa.
- Extrae el Origen o fuente que impone el compromiso (EIA, número de RCA).
- Infiere el Tipo de Compromiso (Ambiental, Social, Legal, etc.).
- Si está relacionado con polvo/agua, asigna "Mina" en Gerencia Responsable con is_inferred: true.
- Sugiere a la Entidad Fiscalizadora lógica para ese tipo de compromiso (Ej: SMA, DGA, SEA).
- Si no hay estado claro en el texto, sugiere "Pendiente" con is_inferred: true.
- Si el documento no especifica fecha de fin, establece "vigencia_acotada" como "Falso" y `is_inferred`: true.
"""

async def extract_permit_data(file_bytes: bytes, mime_type: str) -> PermitExtractionResponse:
    if client is None or GEMINI_API_KEY == "dummy_key_for_testing":
        # Simulación de respuesta IA mientras no haya KEY configurada
        return PermitExtractionResponse(
            nombre_permiso={"value": "Monitoreo de Calidad de Aire Fase I", "is_inferred": False},
            referencia_legal={"value": "RCA 245/2018", "is_inferred": False},
            estado_gestion={"value": "PENDIENTE", "is_inferred": True},
            autoridad_competente={"value": "SEREMI SALUD", "is_inferred": False},
            gerencia_responsable={"value": "Minas", "is_inferred": True},
            contratista_sugerido={"value": "GESTIONA", "is_inferred": True},
            tipo_permiso={"value": "Ambiental", "is_inferred": True},
            responsable={"value": "Juan Pérez", "is_inferred": False},
            periodo={"value": "2024", "is_inferred": True},
            vencimiento={"value": "15 Oct 2024", "is_inferred": False},
            vigencia_acotada={"value": "Verdadero", "is_inferred": True}
        )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                "Por favor lee este documento y extrae la información requerida.",
            ],
            config=types.GenerateContentConfig(
                system_instruction=PERMIT_INSTRUCTIONS,
                response_mime_type="application/json",
                response_schema=PermitExtractionResponse,
            ),
        )
        return PermitExtractionResponse.model_validate_json(response.text)
    except Exception as e:
        print(f"Error calling Gemini AI: {e}")
        raise e

async def extract_social_data(file_bytes: bytes, mime_type: str) -> SocialExtractionResponse:
    if client is None or GEMINI_API_KEY == "dummy_key_for_testing":
        # Simulación
        return SocialExtractionResponse(
            compromiso={"value": "Pavimentar 15 km de la Ruta C-34", "is_inferred": False},
            estado_sugerido={"value": "En Elaboración", "is_inferred": True},
            fecha_limite={"value": "Diciembre 2024", "is_inferred": False},
            responsables={"value": "Comunidad de Coyo", "is_inferred": False}
        )
        
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                "Por favor extrae el compromiso social detallado.",
            ],
            config=types.GenerateContentConfig(
                system_instruction=SOCIAL_INSTRUCTIONS,
                response_mime_type="application/json",
                response_schema=SocialExtractionResponse,
            ),
        )
        return SocialExtractionResponse.model_validate_json(response.text)
    except Exception as e:
        print(f"Error calling Gemini AI for social commit: {e}")
        raise e

async def extract_commitment_data(file_bytes: bytes, mime_type: str) -> CommitmentExtractionResponse:
    if client is None or GEMINI_API_KEY == "dummy_key_for_testing":
        # Simulación de respuesta mockeada
        return CommitmentExtractionResponse(
            id_compromiso={"value": "Autogenerado", "is_inferred": True},
            descripcion_compromiso={"value": "Implementar programa de monitoreo de polvo", "is_inferred": False},
            origen_fuente={"value": "RCA 245/2018", "is_inferred": False},
            tipo_compromiso={"value": "Ambiental", "is_inferred": True},
            gerencia_responsable={"value": "Mina", "is_inferred": True},
            area_instalacion={"value": "Rajo Abierto", "is_inferred": False},
            empresa_contratista={"value": "GESTIONA", "is_inferred": True},
            responsable={"value": "Ingeniero de Medioambiente", "is_inferred": True},
            estado_inicial={"value": "Pendiente", "is_inferred": True},
            autoridad_fiscalizadora={"value": "SMA", "is_inferred": True},
            vigencia_acotada={"value": "Falso", "is_inferred": True},
            fecha_vencimiento={"value": "Permanente", "is_inferred": True}
        )
        
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                "Extrae los datos de esta obligación/compromiso y clasifícalos según la estructura requerida.",
            ],
            config=types.GenerateContentConfig(
                system_instruction=COMMITMENT_INSTRUCTIONS,
                response_mime_type="application/json",
                response_schema=CommitmentExtractionResponse,
            ),
        )
        return CommitmentExtractionResponse.model_validate_json(response.text)
    except Exception as e:
        print(f"Error calling Gemini AI for commitment extraction: {e}")
        raise e
