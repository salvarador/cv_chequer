"""
cv_triager.py: CV triaging and entity extraction using spaCy
"""
import re
from typing import Dict, Any

import spacy

"""
Spanish CV triager using spaCy es_core_news_lg
"""
try:
    nlp = spacy.load("es_core_news_lg")
except Exception:
    nlp = None

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

# Spanish keywords
SKILL_KEYWORDS = ["Python", "JavaScript", "AWS", "Docker", "React", "SQL", "Node.js", "Kubernetes", "Java", "C++", "Azure", "Spring", "Angular"]
DEGREE_KEYWORDS = ["Licenciado", "Ingeniero", "Maestría", "Doctorado", "Bachiller", "MBA", "Grado"]


def triage_cv(text: str) -> Dict[str, Any]:
    """
    Extrae entidades clave de CV en español: nombre, email, habilidades, años de experiencia, empresas, cargo, ubicación, grado.
    """
    result = {
        "nombre": None,
        "email": None,
        "habilidades": [],
        "anos_experiencia": None,
        "empresas": [],
        "cargo": None,
        "ubicacion": None,
        "grado": None,
    }
    if not nlp:
        return result
    doc = nlp(text)

    # Nombre (primer entidad PERSON)
    for ent in doc.ents:
        if ent.label_ == "PER":
            result["nombre"] = ent.text
            break

    # Email
    match = re.search(EMAIL_REGEX, text)
    if match:
        result["email"] = match.group(0)

    # Habilidades (coincidencia de palabras clave)
    result["habilidades"] = [skill for skill in SKILL_KEYWORDS if skill.lower() in text.lower()]

    # Años de experiencia (regex en español)
    exp_match = re.search(r"(\d{1,2})\s+(años|ano|años de experiencia|ano de experiencia)", text, re.I)
    if exp_match:
        result["anos_experiencia"] = int(exp_match.group(1))

    # Empresas (entidades ORG)
    result["empresas"] = list({ent.text for ent in doc.ents if ent.label_ == "ORG"})

    # Cargo (títulos comunes en español)
    cargos = ["Ingeniero", "Desarrollador", "Gerente", "Líder", "Arquitecto", "Consultor", "Director", "Jefe"]
    for cargo in cargos:
        if re.search(rf"\b{cargo}\b", text, re.I):
            result["cargo"] = cargo
            break

    # Ubicación (entidad LOC o GPE)
    for ent in doc.ents:
        if ent.label_ in ["LOC", "GPE"]:
            result["ubicacion"] = ent.text
            break

    # Grado (coincidencia de palabras clave)
    for grado in DEGREE_KEYWORDS:
        if grado.lower() in text.lower():
            result["grado"] = grado
            break

    return result
