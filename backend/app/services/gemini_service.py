import os
from google import genai
from google.genai import types
from app.models.schemas import PermitExtractionResponse, SocialExtractionResponse

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
"""

SOCIAL_INSTRUCTIONS = """
Eres un Asistente Comunitario experto en sostenibilidad para una empresa minera.
Tu trabajo es extraer información de compromisos sociales y relacionamiento comunitario desde actas de asamblea, convenios de inversión social o minutas.
Identifica el compromiso principal, sujeta o entidades responsables. Si no logras encontrar el estado del compromiso, sugiere "En Elaboración" con is_inferred: true.
"""

async def extract_permit_data(file_bytes: bytes, mime_type: str) -> PermitExtractionResponse:
    if client is None or GEMINI_API_KEY == "dummy_key_for_testing":
        # Simulación de respuesta IA mientras no haya KEY configurada
        return PermitExtractionResponse(
            nombre_permiso={"value": "Monitoreo de Calidad de Aire Fase I", "is_inferred": False},
            referencia_legal={"value": "RCA 245/2018", "is_inferred": False},
            autoridad_competente={"value": "SEREMI SALUD", "is_inferred": False},
            vencimiento={"value": "15 Oct 2024", "is_inferred": False},
            gerencia_responsable={"value": "Minas", "is_inferred": True},
            contratista_sugerido={"value": "GESTIONA", "is_inferred": True},
            responsable={"value": "Juan Pérez", "is_inferred": False}
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
                response_schema=types.Schema.from_pydantic(PermitExtractionResponse),
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
                response_schema=types.Schema.from_pydantic(SocialExtractionResponse),
            ),
        )
        return SocialExtractionResponse.model_validate_json(response.text)
    except Exception as e:
        print(f"Error calling Gemini AI for social commit: {e}")
        raise e
