#!/usr/bin/env python3
"""
Profile & Settings Manager for Universal FinnJobScout
------------------------------------------------------
Håndterer lagring og henting av brukerens profil, CV-erfaringer,
personlighetstrekk, tone of voice og FINN-søkekriterier.
"""

import json
from pathlib import Path
from typing import Dict, Any

BASE_DIR = Path(__file__).parent.parent.resolve()
SETTINGS_FILE = BASE_DIR / "user_profile" / "user_settings.json"
PROFILE_MD_FILE = BASE_DIR / "user_profile" / "master_profile.md"

DEFAULT_SETTINGS: Dict[str, Any] = {
    "full_name": "Markus Hysvær Ingierd",
    "age": 23,
    "current_title": "Utvikler & IT-entusiast",
    "target_category": "IT & Utvikling",
    "tone_of_voice": "Ung & direkte (23 år, uformell, korte setninger, null konsulentspråk)",
    "personality_traits": [
        "Lærevillig & nysgjerrig",
        "Strukturert & ansvarsfull",
        "Folkelig lagånd (Kroa i Bø - 200 frivillige studenter)",
        "Praktisk feilsøker (Toma drift & mekke bil)"
    ],
    "cv_experiences": """
- Mobil- & Webutvikling: Kotlin, Android, Jetpack Compose, React, Next.js, TypeScript, Python, SQL.
- Kulturminner (Android App): Kartbasert app med Kotlin, GPS, Mapbox og Firebase.
- BigFive hos rubyNor (React Dashboard): Utviklet interaktivt dashbord for personlighetsanalyser.
- Driftstekniker hos Toma (Color Line Terminalen): Feilsøking, systemansvar og praktisk vedlikehold.
- Studenthuset Kroa i Bø: Styre- og utvalgsarbeid i tett samarbeid med 200 frivillige studenter.
    """.strip(),
    "custom_search_keywords": ["utvikler", "fullstack", "frontend", "backend", "kotlin", "react", "python", "driftstekniker"],
    "location_filter": "Oslo og omegn"
}

def load_settings() -> Dict[str, Any]:
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)
                # Fyll inn manglende felt fra default dersom nye innstillinger legges til
                for k, v in DEFAULT_SETTINGS.items():
                    if k not in settings:
                        settings[k] = v
                return settings
        except Exception as e:
            print(f"[!] Feil ved lesing av user_settings.json: {e}")
    
    # Lagre default innstillinger om filen ikke fantes
    save_settings(DEFAULT_SETTINGS)
    return DEFAULT_SETTINGS

def save_settings(settings: Dict[str, Any]) -> None:
    SETTINGS_FILE.parent.mkdir(exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

    # Oppdater også master_profile.md for bakoverkompatibilitet
    try:
        md_lines = [
            f"# 👤 Masterprofil – {settings.get('full_name', 'Bruker')}\n",
            f"**Navn:** {settings.get('full_name')}",
            f"**Alder:** {settings.get('age')} år",
            f"**Stillingstittel:** {settings.get('current_title')}",
            f"**Målkategori:** {settings.get('target_category')}",
            f"**Tone:** {settings.get('tone_of_voice')}\n",
            "## 🌟 Personlighetstrekk & Styrker",
            "\n".join([f"* {trait}" for trait in settings.get("personality_traits", [])]),
            "\n## 💼 CV & Erfaringer",
            settings.get("cv_experiences", "")
        ]
        PROFILE_MD_FILE.write_text("\n".join(md_lines), encoding="utf-8")
    except Exception as e:
        print(f"[!] Kunne ikke skrive master_profile.md: {e}")

if __name__ == "__main__":
    s = load_settings()
    print(f"[+] Profil lastet for: {s.get('full_name')}")
