"""
╔══════════════════════════════════════════════════════════════╗
║   🧠 DMENTE DIGITAL - Lead Qualifier Module                 ║
║   "No es azar, es propósito"                                ║
║   Sistema de Calificación Inteligente de Leads             ║
╚══════════════════════════════════════════════════════════════╝
"""

from typing import Dict, List, Optional
import pandas as pd

# ─── SECTOR TEMPLATES ────────────────────────────────────────

SECTOR_TEMPLATES = {
    "odontologia": {
        "nombre": "🦷 Odontología",
        "descripcion": "Clínicas dentales, consultorio odontológico",
        "criterios_calificacion": {
            "sitio_web": 20,
            "reviews": 15,
            "rating": 25,
            "telefono": 15,
            "redes_sociales": 10,
            "ubicacion": 15
        },
        "puntuacion_minima": 60,
        "palabras_clave": ["dental", "odonto", "dentista", "ortodoncia", "endodoncia"]
    },

    "medicina": {
        "nombre": "⚕️ Medicina",
        "descripcion": "Clínicas médicas, hospitales, centros de salud",
        "criterios_calificacion": {
            "sitio_web": 20,
            "reviews": 15,
            "rating": 25,
            "telefono": 15,
            "redes_sociales": 10,
            "ubicacion": 15
        },
        "puntuacion_minima": 60,
        "palabras_clave": ["clínica", "hospital", "médico", "doctor", "consultorio"]
    },

    "gastronomia": {
        "nombre": "🍽️ Gastronomía",
        "descripcion": "Restaurantes, cafeterías, bares, delivery",
        "criterios_calificacion": {
            "sitio_web": 15,
            "reviews": 20,
            "rating": 25,
            "telefono": 15,
            "redes_sociales": 15,
            "ubicacion": 10
        },
        "puntuacion_minima": 55,
        "palabras_clave": ["restaurante", "café", "bar", "comida", "delivery"]
    },

    "pyme_general": {
        "nombre": "🏪 PYME General",
        "descripcion": "Pequeñas y medianas empresas, comercios",
        "criterios_calificacion": {
            "sitio_web": 18,
            "reviews": 15,
            "rating": 20,
            "telefono": 18,
            "redes_sociales": 14,
            "ubicacion": 15
        },
        "puntuacion_minima": 55,
        "palabras_clave": ["empresa", "tienda", "comercio", "negocio", "pyme"]
    },

    "manufactura": {
        "nombre": "🏭 Manufactura",
        "descripcion": "Industrias, fábricas, plantas de producción",
        "criterios_calificacion": {
            "sitio_web": 25,
            "reviews": 10,
            "rating": 15,
            "telefono": 20,
            "redes_sociales": 10,
            "ubicacion": 20
        },
        "puntuacion_minima": 60,
        "palabras_clave": ["manufactura", "industria", "fábrica", "producción", "taller"]
    }
}


def get_all_sectors() -> List[str]:
    """Retorna lista de todos los sectores disponibles"""
    return list(SECTOR_TEMPLATES.keys())


def get_sector_info(sector: str) -> Dict:
    """
    Obtiene información detallada de un sector

    Args:
        sector: Código del sector

    Returns:
        Diccionario con información del sector
    """
    return SECTOR_TEMPLATES.get(sector, {})


def calculate_lead_score(lead: Dict, sector: str) -> int:
    """
    Calcula puntuación de un lead basado en criterios del sector

    Args:
        lead: Diccionario con datos del lead
        sector: Código del sector

    Returns:
        Puntuación de 0-100
    """
    if sector not in SECTOR_TEMPLATES:
        return 0

    template = SECTOR_TEMPLATES[sector]
    criterios = template.get("criterios_calificacion", {})

    puntuacion = 0
    total_posible = sum(criterios.values())

    # Evaluar sitio web
    if lead.get("sitio_web"):
        puntuacion += criterios.get("sitio_web", 0)

    # Evaluar reviews
    num_reviews = int(lead.get("numero_reviews", 0)) if lead.get("numero_reviews") else 0
    if num_reviews > 0:
        reviews_weight = min(num_reviews / 50 * criterios.get("reviews", 0), criterios.get("reviews", 0))
        puntuacion += reviews_weight

    # Evaluar rating
    rating = float(lead.get("rating", 0)) if lead.get("rating") else 0
    if rating > 0:
        rating_weight = (rating / 5) * criterios.get("rating", 0)
        puntuacion += rating_weight

    # Evaluar teléfono
    if lead.get("telefono"):
        puntuacion += criterios.get("telefono", 0)

    # Evaluar redes sociales
    redes_sociales = lead.get("redes_sociales", "no_tiene")
    if redes_sociales != "no_tiene":
        puntuacion += criterios.get("redes_sociales", 0)

    # Evaluar ubicación
    if lead.get("direccion"):
        puntuacion += criterios.get("ubicacion", 0)

    # Normalizar a escala 0-100
    return int((puntuacion / total_posible) * 100) if total_posible > 0 else 0


def qualify_leads(records: List[Dict], sector: str) -> pd.DataFrame:
    """
    Califica una lista de leads y retorna DataFrame ordenado

    Args:
        records: Lista de diccionarios con datos de leads
        sector: Código del sector para aplicar criterios

    Returns:
        DataFrame con leads calificados y ordenados
    """
    if not records:
        return pd.DataFrame()

    # Calcular puntuación para cada lead
    for record in records:
        record["puntuacion"] = calculate_lead_score(record, sector)
        record["sector"] = SECTOR_TEMPLATES.get(sector, {}).get("nombre", sector)

    # Convertir a DataFrame y ordenar por puntuación
    df = pd.DataFrame(records)
    df = df.sort_values("puntuacion", ascending=False)

    return df


def get_sector_insights(sector: str) -> Dict:
    """
    Obtiene insights y análisis del sector

    Args:
        sector: Código del sector

    Returns:
        Diccionario con insights del sector
    """
    if sector not in SECTOR_TEMPLATES:
        return {}

    template = SECTOR_TEMPLATES[sector]

    return {
        "sector": sector,
        "nombre": template.get("nombre"),
        "descripcion": template.get("descripcion"),
        "puntuacion_minima": template.get("puntuacion_minima", 60),
        "criterios_principales": template.get("criterios_calificacion", {}),
        "palabras_clave": template.get("palabras_clave", []),
        "recomendaciones": get_sector_recommendations(sector)
    }


def get_sector_recommendations(sector: str) -> List[str]:
    """Obtiene recomendaciones específicas para un sector"""

    recomendaciones_por_sector = {
        "odontologia": [
            "Priorizar leads con reviews y ratings altos",
            "Verificar disponibilidad de servicios especializados",
            "Buscar clínicas con sitio web profesional",
            "Contactar durante horario laboral"
        ],
        "medicina": [
            "Verificar especialidades médicas",
            "Confirmar licencias profesionales",
            "Priorizar centros con infraestructura moderna",
            "Buscar leads con buena reputación en Google"
        ],
        "gastronomia": [
            "Considerar ubicación estratégica",
            "Analizar tendencias en redes sociales",
            "Verificar horarios de funcionamiento",
            "Evaluar delivery o solo presencial"
        ],
        "pyme_general": [
            "Priorizar por presencia online",
            "Verificar antigüedad del negocio",
            "Evaluar rango de servicios ofrecidos",
            "Considerar ubicación y accesibilidad"
        ],
        "manufactura": [
            "Verificar capacidad de producción",
            "Confirmar certificaciones de calidad",
            "Evaluar experiencia en el sector",
            "Priorizar leads con presencia B2B"
        ]
    }

    return recomendaciones_por_sector.get(sector, [
        "Solicitar más información al lead",
        "Verificar datos de contacto",
        "Realizar seguimiento personalizado"
    ])


def filter_qualified_leads(df: pd.DataFrame, min_score: int = 60) -> pd.DataFrame:
    """
    Filtra leads que cumplen puntuación mínima

    Args:
        df: DataFrame con leads
        min_score: Puntuación mínima requerida

    Returns:
        DataFrame filtrado
    """
    if df.empty or "puntuacion" not in df.columns:
        return df

    return df[df["puntuacion"] >= min_score]


# ─── EXPORTAR FUNCIONES Y CONSTANTES ──────────────────────

__all__ = [
    "SECTOR_TEMPLATES",
    "get_all_sectors",
    "get_sector_info",
    "calculate_lead_score",
    "qualify_leads",
    "get_sector_insights",
    "get_sector_recommendations",
    "filter_qualified_leads"
]
