#!/usr/bin/env python3
"""
Universal Antigravity AI Engine for FinnJobScout
-------------------------------------------------
Genererer verdensklasse skreddersydde jobbsøknader for ALLE yrker og stillinger.
Bruker dynamisk profil (CV, personlighetstrekk, tone) fra profile_manager
og fletter det med bedriftens uthentede FINN-innsikt.
"""

import os
import json
from pathlib import Path
import profile_manager

BASE_DIR = Path(__file__).parent.parent.resolve()
SKILL_FILE = BASE_DIR / ".agents" / "skills" / "application_expert" / "SKILL.md"

def load_skill_rules() -> str:
    if SKILL_FILE.exists():
        return SKILL_FILE.read_text(encoding="utf-8")
    return "Skriv 4-paragrafs Vipps-søknad med ung tone, korte setninger, samskriving og null konsulentspråk."

def generate_cover_letter(job: dict, custom_notes: str = "") -> str:
    job_title = job.get("title", "Stilling")
    company = job.get("company", "Bedriften")
    location = job.get("location", "Oslo")
    hook_insight = job.get("company_hook_insight", "")
    description = job.get("description_text", "")[:4000]

    # Hent dynamiske brukerinnstillinger
    settings = profile_manager.load_settings()
    full_name = settings.get("full_name", "Markus Hysvær Ingierd")
    age = settings.get("age", 23)
    current_title = settings.get("current_title", "Utvikler & IT-entusiast")
    tone_of_voice = settings.get("tone_of_voice", "Ung & direkte (23 år), uformell, korte setninger, null konsulentspråk")
    personality_traits = ", ".join(settings.get("personality_traits", []))
    cv_experiences = settings.get("cv_experiences", "")
    skill_rules = load_skill_rules()

    # Sjekk om Gemini API-nøkkel finnes i miljøvariablene
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)

            system_instruction = f"""
            Du er en verdensklasse AI-søknadsekspert. Du skal skrive et 100% skreddersydd, vinnende søknadsbrev for {full_name} ({age} år).

            === KANDIDATENS DRIFT OG PERSONLIGHET ===
            Navn: {full_name} ({age} år)
            Stillingstittel: {current_title}
            Personlighetstrekk & Styrker: {personality_traits}
            Ønsket Tone & Stil: {tone_of_voice}
            CV & Hovederfaringer:
            {cv_experiences}

            === REGELBOK & MENTALITET (APPLICATION EXPERT) ===
            {skill_rules}

            === STRENG 4-PARAGRAFS VIPPS-STRUKTUR ===
            1. PARAGRAF (Menneskelig Åpning): Menneskelig, direkte og uformell åpning (Maks 2-3 setninger). Kobles direkte til bedriftens kultur/samfunnsoppdrag eller denne FINN-kroken: "{hook_insight}". Null floskler som "Jeg viser til deres annonse" eller "Dette er et utrolig spennende sted å starte min karriere".
            2. PARAGRAF (Faglig/Teknisk Bevis): Velg de mest relevante erfaringene fra kandidatens CV som matcher kravene i annonsen. Viss at kandidaten kan levere verdi fra dag én med konkrete resultater.
            3. PARAGRAF (Praktisk Arbeid, Verktøy & Gjennomføringsevne): Trekk fram praktisk feilsøking, arbeidsmoral, og verktøy/metoder (f.eks. Toma driftstekniker, mekanisk feilsøking eller moderne verktøy).
            4. PARAGRAF (Folkelig Lagånd & Avslutning): Fremhev folkelig lagånd, teambygging (f.eks. Kroa i Bø med 200 frivillige studenter dsom kandidaten er Markus), og avslutt på en uformell, hyggelig og selvsikker måte uten Konsulentspråk.
            """

            user_prompt = f"""
            Skriv et perfekt skreddersydd søknadsbrev til følgende utlysning:
            
            Stillingstittel: {job_title}
            Bedrift: {company}
            Sted: {location}
            FINN-Krok / Innsikt: {hook_insight}
            Stillingstekst fra FINN:
            {description}
            
            Tilleggsønsker fra bruker: {custom_notes or 'Ingen'}

            Returner kun selve søknadsbrevet i ren Markdown format (start direkte med f.eks. 'Hei {company}-teamet!' eller 'Hei!').
            """

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config={"system_instruction": system_instruction, "temperature": 0.7}
            )
            if response.text and len(response.text.strip()) > 100:
                return response.text.strip()
        except Exception as e:
            print(f"[!] Gemini API error: {e}")

    # INTELLIGENT PYTHON ENGINE (High-converting fallback engine)
    clean_hook = hook_insight.split(":")[-1].strip() if ":" in hook_insight else hook_insight
    if not clean_hook:
        clean_hook = f"deres arbeid med {job_title.lower()} fremstår som et utrolig spennende prosjekt"

    text = (job_title + " " + description).lower()
    
    # Tilpass faglige bevis ut fra annonse og kandidatens CV
    if any(k in text for k in ["android", "kotlin", "mobil", "mobile", "gps"]):
        proof_text = (
            "Med min bakgrunn innen Kotlin og Android-utvikling brenner jeg for å bygge robuste, brukerrettede apper. "
            "I prosjektet *Kulturminner* utviklet jeg en kartbasert Android-applikasjon med Kotlin, Jetpack Compose og GPS-posisjonering, "
            "noe som ga meg dyp erfaring med helhetlig systemarkitektur, API-integrasjon og god brukeropplevelse."
        )
    elif any(k in text for k in ["react", "next.js", "typescript", "frontend", "ui", "ux"]):
        proof_text = (
            "Med min bakgrunn innen React, Next.js og TypeScript brenner jeg for å bygge intuitive, brukerrettede webgrensesnitt. "
            "I prosjektet *BigFive hos rubyNor* utviklet jeg et interaktivt dashbord for personlighetsanalyser for ledere, "
            "der fokuset var ren komponentstruktur, responsivt UI og ryddig datavisualisering."
        )
    else:
        proof_text = (
            "Med min bakgrunn innen både fullstackutvikling (React, Next.js, TypeScript, Python) og mobilløsninger "
            "trives jeg godt i hele utviklingsløpet. Jeg har bygget applikasjoner som kombinerer solid ytelse med "
            "et intuitivt og brukersentrert grensesnitt."
        )

    letter = f"""Hei {company}-teamet!

Da jeg så at dere leter etter en engasjert {job_title.lower()}, måtte jeg legge inn en søknad. {clean_hook.capitalize()} gjør dette til en veldig spennende mulighet.

{proof_text}

Ved siden av ren programmering har jeg erfaring som driftstekniker hos Toma på Color Line Terminalen. Det har gitt meg dyp praktisk forståelse for feilsøking, systemansvar og struktur når ting må løses i hverdagen. Jeg bruker også AI-verktøy som Cursor, Claude og Python-agenter aktivt for å jobbe smart og effektivt.

Gjennom min tid på studenthuset Kroa i Bø samarbeidet jeg tett med 200 frivillige studenter. Det har lært meg verdien av god kommunikasjon, folkelig lagånd og det å spille hverandre gode. Jeg ser frem til en hyggelig prat om hvordan jeg kan bidra hos dere.

Med vennlig hilsen,
{full_name}
{age} år | {current_title}
"""
    return letter
