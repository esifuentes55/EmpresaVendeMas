import os
from typing import Optional

from openai import OpenAI

_DEFAULT_CATEGORY = "General"


def categorize_provider(description: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _fallback_category(description)

    client = OpenAI(api_key=api_key)
    prompt = (
        "Clasifica este proveedor en una categoría de negocio corta (1-3 palabras). "
        "Solo responde la categoría sin puntuación extra.\n\n"
        f"Descripción: {description}"
    )

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            input=prompt,
            temperature=0,
            max_output_tokens=20,
        )
        text = (response.output_text or "").strip()
        return text or _fallback_category(description)
    except Exception:
        return _fallback_category(description)


def _fallback_category(description: str) -> str:
    desc = description.lower()
    keywords: list[tuple[str, str]] = [
        ("marketing", "Marketing"),
        ("seo", "Marketing"),
        ("software", "Tecnología"),
        ("desarrollo", "Tecnología"),
        ("contable", "Finanzas"),
        ("legal", "Legal"),
        ("logística", "Logística"),
        ("transporte", "Logística"),
    ]
    for key, category in keywords:
        if key in desc:
            return category
    return _DEFAULT_CATEGORY
