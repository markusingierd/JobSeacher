#!/usr/bin/env python3
"""
Universal Antigravity AI Engine v2.0 for FinnJobScout
------------------------------------------------------
Genererer verdensklasse, autentiske og skreddersydde jobbsøknader for ALLE yrker.
Eliminerer KI-klisjéer, bruker streng 4-paragrafs struktur og tilpasser seg
dynamisk til kandidatens CV, personlighetstrekk, tone og utlysningens fagfelt.
"""

import os
import re
import json
import random
from pathlib import Path
import profile_manager

BASE_DIR = Path(__file__).parent.parent.resolve()
SKILL_FILE = BASE_DIR / ".agents" / "skills" / "application_expert" / "SKILL.md"

def load_skill_rules() -> str:
    if SKILL_FILE.exists():
        return SKILL_FILE.read_text(encoding="utf-8")
    return "Skriv 4-paragrafs Vipps-søknad med ung tone, korte setninger, samskriving og null konsulentspråk."

def strip_markdown(text: str) -> str:
    """Fjerner alle markdown-tegn (*, **, #, __, osv.) slik at teksten kan limest rent inn i Word uten merkevare-støy."""
    if not text:
        return ""
    
    # Fjern overskrift-tegn (#, ##, ### osv) på starten av linjer
    text = re.sub(r'^\s*#+\s*', '', text, flags=re.MULTILINE)
    
    # Fjern fet og kursiv skrift (**tekst**, *tekst*, __tekst__, _tekst_)
    text = text.replace('**', '').replace('__', '')
    text = text.replace('*', '').replace('_', '')
    
    # Fjern punktmerking på starten av linjer (- punkt eller * punkt)
    text = re.sub(r'^\s*[\*\-]\s+', '', text, flags=re.MULTILINE)
    
    # Fjern klammer for lenker [tekst](url) -> tekst
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # Fjern innledende/avsluttende ekstra linjeskift per linje
    lines = [line.rstrip() for line in text.splitlines()]
    result = '\n'.join(lines)
    
    # Maks 2 påfølgende linjeskift (avsnittsskille)
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.strip()

def generate_cover_letter(job: dict, custom_notes: str = "") -> str:
    job_title = job.get("title", "Stilling")
    company = job.get("company", "Bedriften")
    location = job.get("location", "Oslo")
    hook_insight = job.get("company_hook_insight", "")
    description = job.get("description_text", "")[:4000]

    # Hent dynamiske brukerinnstillinger fra profile_manager
    settings = profile_manager.load_settings()
    full_name = settings.get("full_name", "Markus Hysvær Ingierd")
    age = settings.get("age", 23)
    current_title = settings.get("current_title", "Utvikler & IT-entusiast")
    target_category = settings.get("target_category", "IT & Utvikling")
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
            Du er Norges dyktigste og mest treffsikre karriere- og søknadsforfatter.
            Du skal skrive et 100 % skreddersydd, autentisk og vinnende søknadsbrev for {full_name} ({age} år).

            === KANDIDATENS DRIFT OG PERSONLIGHET ===
            Navn: {full_name} ({age} år)
            Yrke / Stillingstittel: {current_title}
            Målkategori: {target_category}
            Personlighetstrekk & Styrker: {personality_traits}
            Ønsket Tone & Stil: {tone_of_voice}
            CV & Hovederfaringer:
            {cv_experiences}

            === STRENG REGELBOK & MENTALITET (APPLICATION EXPERT) ===
            {skill_rules}

            === KRITISK FORMATERINGSREGLER FOR WORD-EKSPORT ===
            - IKKE bruk noen form for Markdown-tegn! INGEN stjerner (* eller **), INGEN skråstreker, INGEN emneknagger (#), INGEN kulepunkter.
            - Teksten skal returneres i REN TEKST (Plain text) med klare avsnittskift, slik at den kan limest rett inn i Microsoft Word uten opprydding.

            === FORBUD MOT KI-KLISJÉER (STRICT NEGATIVE CONSTRAINTS) ===
            - ALDRI bruk uttrykk som: "Jeg viser til deres annonse...", "Dette fremstår som en utrolig spennende mulighet...", "Passer min bakgrunn midt i blinken...", "Tilføre merverdi", "Synergier".
            - ALDRI bruk parenteser () midt i setninger for å pakke inn verktøy eller eksempler.
            - ALDRI bruk engelske tankestreker (- / –) inne i norsk leddsetning. Bruk leddsetninger med komma.
            - ALLTID bruk korrekt norsk samskriving (f.eks. fullstackutvikler, frontendkompetanse, skiftarbeid, systemarkitektur).

            === STRENG 4-PARAGRAFS VIPPS-STRUKTUR ===
            1. PARAGRAF (Menneskelig Åpning): Menneskelig, direkte og uformell åpning (Maks 2-3 setninger). Kobles direkte til bedriftens kultur eller utfordringen: "{hook_insight}". Helt ny og frisk vinkling uten samlebånd-intro.
            2. PARAGRAF (Faglig Bevis & Verdiskaping - 80% IT-fokus): Velg de 2-3 mest relevante resultatene fra kandidatens CV som matcher stillingen (f.eks. Kotlin, Android, Jetpack Compose, React, Next.js, TypeScript, Python, skyarkitektur). Vis at kandidaten kan levere verdi fra dag én.
            3. PARAGRAF (Praktisk Arbeid, Verktøy & Gjennomføringsevne): Trekk fram praktisk feilsøking (Toma driftetekniker / mekke bil som kort støtte) og bruk av moderne AI-verktøy som Cursor, Claude og Python-agenter for å jobbe effektivt.
            4. PARAGRAF (Folkelig Lagånd & Avslutning): Fremhev folkelig lagånd, teambygging (f.eks. Kroa i Bø med 200 frivillige studenter), og avslutt på en uformell, hyggelig og selvsikker måte uten konsulentspråk.
            """

            user_prompt = f"""
            Skriv et perfekt skreddersydd søknadsbrev til følgende utlysning på FINN.no:
            
            Stillingstittel: {job_title}
            Bedrift: {company}
            Sted: {location}
            FINN-Krok / Innsikt: {hook_insight}
            Stillingstekst fra FINN:
            {description}
            
            Tilleggsønsker fra bruker: {custom_notes or 'Ingen'}

            Returner KUN selve teksten til søknadsbrevet i REN TEKST uten Markdown-formatering (start direkte med 'Hei {company}-teamet!' eller 'Hei!').
            """

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config={"system_instruction": system_instruction, "temperature": 0.7}
            )
            if response.text and len(response.text.strip()) > 100:
                return strip_markdown(response.text.strip())
        except Exception as e:
            print(f"[!] Gemini API error: {e}")

    # UNIVERSELL INTELLIGENT PYTHON ENGINE (Lokal offline motor uten Markdown-støy)
    clean_hook = hook_insight.split(":")[-1].strip() if ":" in hook_insight else hook_insight
    if not clean_hook:
        clean_hook = f"deres fokus på {job_title.lower()}"

    text = (job_title + " " + description).lower()
    
    # Åpningskroker (Variert for å unngå klisjéer)
    openings = [
        f"Da jeg så at dere leter etter en engasjert {job_title.lower()}, måtte jeg legge inn en søknad. {clean_hook.capitalize()} gjør at denne stillingen skiller seg positivt ut.",
        f"Stillingen som {job_title.lower()} hos {company} fanger interessen min umiddelbart. {clean_hook.capitalize()} samsvarer godt med måten jeg liker å jobbe på.",
        f"Dere i {company} søker etter en {job_title.lower()}, og det matcher min bakgrunn og interesseområde veldig bra. {clean_hook.capitalize()} virker som en super utfordring."
    ]
    p1 = random.choice(openings)

    # Tilpass faglige bevis ut fra utlysning og kandidatens CV (Uten Markdown-stjerner)
    if any(k in text for k in ["android", "kotlin", "mobil", "mobile", "gps"]):
        proof_text = (
            "Med min bakgrunn innen Kotlin og Android-utvikling brenner jeg for å bygge robuste, brukerrettede apper. "
            "I prosjektet Kulturminner utviklet jeg en kartbasert Android-applikasjon med Kotlin, Jetpack Compose, Mapbox SDK og posisjonering, "
            "noe som ga meg dyp erfaring med helhetlig systemarkitektur, API-integrasjon og god brukeropplevelse."
        )
    elif any(k in text for k in ["react", "next.js", "typescript", "frontend", "ui", "ux"]):
        proof_text = (
            "Med min bakgrunn innen React, Next.js og TypeScript brenner jeg for å bygge intuitive, brukerrettede webgrensesnitt. "
            "I mitt prosjekt hos rubyNor utviklet jeg et interaktivt dashbord for personlighetsanalyser for ledere, "
            "der fokuset var ren komponentstruktur, responsivt UI og ryddig datavisualisering."
        )
    elif any(k in text for k in ["python", "backend", "api", "database", "sql"]):
        proof_text = (
            "Jeg har jobbet mye med backend-utvikling, databaser og REST-API-er i Python og TypeScript. "
            "Gjennom praktiske prosjekter har jeg bygget automatiserte pipelines og datamodeller som sikrer høy ytelse, "
            "ryddig datastruktur og stabil drift."
        )
    else:
        proof_text = (
            "Gjennom min bachelor i IT og informasjonssystemer og praktiske utviklingsprosjekter har jeg bygget solid kompetanse "
            "innen moderne programvareutvikling, både på frontend og backend. Jeg trives godt i hele gjennomføringsløpet, og fokuserer alltid "
            "på ren kode, god struktur og brukersentrerte løsninger."
        )

    p3 = (
        "Ved siden av programmering har jeg erfaring som driftstekniker hos Toma på Color Line Terminalen. "
        "Det har gitt meg dyp praktisk forståelse for feilsøking, systemansvar og struktur når ting må løses i hverdagen. "
        "Jeg bruker også AI-verktøy som Cursor, Claude og Python-agenter aktivt for å jobbe smart og effektivt."
    )

    p4 = (
        "Gjennom min tid på studenthuset Kroa i Bø samarbeidet jeg tett med 200 frivillige studenter. "
        "Det har lært meg verdien av god kommunikasjon, folkelig lagånd og det å spille hverandre gode. "
        "Jeg ser frem til en hyggelig prat om hvordan jeg kan bidra hos dere."
    )

    raw_letter = f"""Hei {company}-teamet!

{p1}

{proof_text}

{p3}

{p4}

Med vennlig hilsen,
{full_name}
{age} år | {current_title}"""

    return strip_markdown(raw_letter)
