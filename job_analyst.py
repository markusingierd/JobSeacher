#!/usr/bin/env python3
"""
Job Analyst for Markus Hysvær Ingierd
-------------------------------------
Leser relevante_stillinger_database.json og markus_master_profil.md.
Beregner match-prosent lokalt basert på nøkkelordvekting og genererer
en oppdatert, strukturert relevante_stillinger.md.
"""

import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
DB_FILE = BASE_DIR / "relevante_stillinger_database.json"
PROFILE_FILE = BASE_DIR / "markus_master_profil.md"
OUTPUT_MD = BASE_DIR / "relevante_stillinger.md"

# Nøkkelord-vektlegging for match-beregning (basert på cvMarkus.md)
KEYWORDS_WEIGHTS = {
    # Primære tekniske ferdigheter & rammeverk (Høy vekt)
    "kotlin": 15,
    "android": 15,
    "react": 12,
    "next.js": 12,
    "typescript": 12,
    "javascript": 10,
    "js": 8,
    "python": 10,
    "ai": 10,
    "ki": 10,
    "agenter": 10,
    "firebase": 12,
    "supabase": 10,
    "sql": 10,
    "java": 10,
    "mobile": 10,
    "mobil": 10,
    "jetpack compose": 12,
    "mapbox": 10,
    
    # Utviklingskonsepter & arkitektur
    "fullstack": 10,
    "frontend": 10,
    "backend": 10,
    "systemutvikler": 10,
    "programvareutvikler": 10,
    "api": 8,
    "git": 6,
    "rest": 6,
    "ui": 6,
    "ux": 6,
    "datavisualisering": 8,
    "komponentbasert": 6,
    
    # Driftsteknisk & praktisk feilsøking (Ny fra oppdatert CV)
    "driftstekniker": 10,
    "drift": 8,
    "feilsøking": 8,
    "vedlikehold": 6,
    "automasjon": 8,
    "systemansvar": 8,
    
    # Sosiale ferdigheter, prosjektstyring & verv
    "team": 6,
    "samarbeid": 6,
    "frivillig": 8,
    "ledelse": 6,
    "koordinator": 6,
    "smidig": 5,
    "tverrfaglig": 5
}

def load_database():
    if DB_FILE.exists():
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_database(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def extract_company_hook_insight(company_name, job_title, description_text):
    text = (company_name + " " + job_title + " " + description_text).lower()
    
    # Ekstraher konkrete team- og kultur-nøkkelsetninger direkte fra FINN-teksten
    team_focus = []
    if "salgsløsning" in text or "kundereise" in text:
        team_focus.append("de digitale salgsløsningene og hele kundereisen")
    if "tverrfaglig" in text:
        team_focus.append("tverrfaglig samarbeid med UX, analytikere og produkteiere")
    if "spille hverandre gode" in text:
        team_focus.append("kultur der vi spiller hverandre gode")
    if "høyt under taket" in text:
        team_focus.append("miljø med superhøyt under taket")

    base_hook = ""
    if any(k in text for k in ["gjensidige", "forsikring", "trygd", "fremtind", "storebrand"]):
        base_hook = "Bileier/Forsikringskunde: Koble egen erfaring med bil/reise/innbo til teamets ansvar for næringslivskunder og hele kundereisen."
    elif any(k in text for k in ["autopay", "parkering", "transport", "vy", "entur", "hyre", "ruter"]):
        base_hook = "Bileier/Reisende: Koble bil- og parkeringshverdag til sømløse løsninger uten bommer/støy."
    elif any(k in text for k in ["skatteetaten", "oslo kommune", "direktoratet", "udi", "statnett", "nav", "politiet"]):
        base_hook = "Innbygger/Samfunn: Koble egen hverdag med skatt/tjenester til nytten løsningen gir 5 mill innbyggere."
    elif any(k in text for k in ["etterretningstjenesten", "sikkerhet", "krypto", "cyber", "forsvaret"]):
        base_hook = "Trygghet/Infrastruktur: Respekt for samfunnsoppdraget om informasjonsskjerming og nasjonal trygghet."
    elif any(k in text for k in ["sparebank", "dnb", "bank", "finans", "vipps"]):
        base_hook = "Hverdagsøkonomi: Koble daglig bruk av apper/betaling til stabile og enkle finansløsninger."
    else:
        base_hook = "Brukerfokus: Koble din egen brukererfaring til nytten teamet skaper for sine kunder."

    if team_focus:
        return f"{base_hook} (Fra FINN-annonsen: {', '.join(team_focus)})"
    return base_hook

def calculate_match(job_title, description_text):
    text = (job_title + " " + description_text).lower()
    score = 0
    max_possible = 100
    matched_skills = []

    for kw, weight in KEYWORDS_WEIGHTS.items():
        if kw in text:
            score += weight
            matched_skills.append(kw.capitalize())

    # Normaliser score til en prosent (maks 100%)
    match_pct = min(100, int((score / max_possible) * 100))
    
    # Skap en kort analyse
    unique_matches = list(dict.fromkeys(matched_skills))[:5]
    if unique_matches:
        analysis = f"Matchende nøkkelord: {', '.join(unique_matches)}"
    else:
        analysis = "Generell IT/Utvikler-stilling"

    return match_pct, analysis

def check_applied_status(db):
    soknadsbrev_dir = BASE_DIR / "soknadsbrev"
    applied_files = {}
    if soknadsbrev_dir.exists():
        for file in soknadsbrev_dir.glob("*.md"):
            try:
                content = file.read_text(encoding="utf-8").lower()
                applied_files[file.name] = content
            except Exception:
                pass

    for job_id, job in db.items():
        company = job.get("company", "").lower()
        job_url = job.get("url", "").lower()
        title = job.get("title", "").lower()
        
        is_applied = False
        applied_file_name = ""
        
        # Sjekk om stillings-ID, URL eller unikt bedriftsnavn finnes i et søknadsbrev
        for filename, content in applied_files.items():
            fn_low = filename.lower()
            if (job_id in content) or (job_url and job_url in content):
                is_applied = True
                applied_file_name = filename
                break
            # Sjekk om bedriftsnavn eller nøkkelord i filnavnet matcher
            company_words = [w for w in company.split() if len(w) >= 4]
            if any(w in fn_low for w in company_words) and company in content:
                is_applied = True
                applied_file_name = filename
                break
        
        if is_applied or job.get("application_status") == "applied":
            job["application_status"] = "applied"
            job["applied_file"] = f"soknadsbrev/{applied_file_name}" if applied_file_name else job.get("applied_file", "")
        else:
            job["application_status"] = "not_applied"

def get_user_info():
    profile_paths = [
        BASE_DIR / "markus_master_profil.md",
        BASE_DIR / "user_profile" / "master_profile.md",
        BASE_DIR / "user_profile" / "master_profile.template.md"
    ]
    for path in profile_paths:
        if path.exists():
            try:
                content = path.read_text(encoding="utf-8")
                for line in content.splitlines():
                    if "navn:" in line.lower() and "[ditt navn" not in line.lower():
                        parts = line.split(":", 1)
                        if len(parts) > 1 and parts[1].strip():
                            return parts[1].strip().replace("**", "").replace("*", "")
                    elif "markus hysvær ingierd" in line.lower():
                        return "Markus Hysvær Ingierd"
            except Exception:
                pass
    return "Jobbsøker"

def generate_markdown(db):
    unapplied_jobs = []
    applied_jobs = []
    excluded_jobs = []

    for job_id, job in db.items():
        if job.get("status") == "excluded":
            excluded_jobs.append(job)
        elif job.get("application_status") == "applied":
            applied_jobs.append(job)
        else:
            unapplied_jobs.append(job)

    # Sorter stillinger etter match-prosent (synkende)
    unapplied_jobs.sort(key=lambda x: x.get("match_percentage", 0), reverse=True)
    applied_jobs.sort(key=lambda x: x.get("match_percentage", 0), reverse=True)

    now_str = datetime.now().strftime("%d.%m.%Y kl. %H:%M")
    user_name = get_user_info()

    md = []
    md.append(f"# 🎯 Relevante Stillinger for {user_name}")
    md.append(f"\n*Sist oppdatert: {now_str}*\n")
    md.append("Dette dokumentet oppdateres automatisk av `job_analyst.py`. Stillinger du allerede har skrevet søknad til blir automatisk merket som ✅ Søkt for å unngå dubletter.\n")
    
    md.append("---")
    md.append("\n## 🌟 Aktuelle Stillinger – IKKE SØKT ENNÅ (Sortert etter Match %)\n")
    md.append("| Match % | Stillingstittel | Bedrift | Sted | Frist | Lenke |")
    md.append("| :---: | :--- | :--- | :--- | :---: | :---: |")

    for job in unapplied_jobs:
        pct = job.get("match_percentage", 0)
        if pct == 0:
            continue
        title = job.get("title", "Ukjent")
        company = job.get("company", "Ukjent")
        location = job.get("location", "Ukjent")
        deadline = job.get("application_deadline", "Ukjent")
        url = job.get("url", "#")
        
        md.append(f"| **{pct}%** | {title} | {company} | {location} | {deadline} | [Åpne på FINN]({url}) |")

    if applied_jobs:
        md.append("\n---")
        md.append("\n## ✅ SØKTE STILLINGER (Søknadsbrev opprettet)\n")
        md.append("| Match % | Stillingstittel | Bedrift | Frist | Søknadsbrev | Lenke |")
        md.append("| :---: | :--- | :--- | :---: | :---: | :---: |")
        for job in applied_jobs:
            pct = job.get("match_percentage", 0)
            title = job.get("title", "Ukjent")
            company = job.get("company", "Ukjent")
            deadline = job.get("application_deadline", "Ukjent")
            url = job.get("url", "#")
            app_file = job.get("applied_file", "")
            file_link = f"[{Path(app_file).name}]({app_file})" if app_file else "Opprettet"
            md.append(f"| **{pct}%** | {title} | {company} | {deadline} | {file_link} | [FINN]({url}) |")

    md.append("\n---")
    md.append("\n## 🔍 Detaljert Match-Analyse for Nye Stillinger\n")

    for job in unapplied_jobs:
        pct = job.get("match_percentage", 0)
        if pct == 0:
            continue
        title = job.get("title", "Ukjent")
        company = job.get("company", "Ukjent")
        url = job.get("url", "#")
        analysis = job.get("match_analysis", "Ingen analyse tilgjengelig.")
        reason = job.get("reason", "")
        exp = job.get("experience_req", "Ukjent")
        hook = job.get("company_hook_insight", "")

        md.append(f"### [{title}]({url}) - {company} ({pct}% Match)")
        md.append(f"* **Sted:** {job.get('location', 'Ukjent')} | **Frist:** {job.get('application_deadline', 'Ukjent')} | **Erfaringskrav:** {exp}")
        md.append(f"* **Analyse:** {analysis}")
        if hook:
            md.append(f"* **Vipps-Krok Forslag:** {hook}")
        if reason:
            md.append(f"* **Merk:** {reason}")
        md.append("")

    if excluded_jobs:
        md.append("---")
        md.append("\n## 🚫 Filtrerte/Ekskluderte Stillinger\n")
        md.append(f"Totalt {len(excluded_jobs)} stilling(er) ble ekskludert (f.eks. på grunn av Senior/Leder-krav).\n")
        for job in excluded_jobs[:10]:  # Viser topp 10 ekskluderte
            md.append(f"- **{job.get('title')}** ({job.get('company')}): {job.get('reason')}")

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print(f"[+] Genererte oppdatert {OUTPUT_MD.name} med {len(unapplied_jobs)} nye stillinger og {len(applied_jobs)} søkte stillinger.")

def run_analyst():
    print("🧠 Starter Job Analyst for Markus...")
    db = load_database()
    
    check_applied_status(db)
    
    updated_count = 0
    for job_id, job in db.items():
        if job.get("status") == "excluded":
            continue
        
        match_pct, analysis = calculate_match(job.get("title", ""), job.get("description_text", ""))
        hook_insight = extract_company_hook_insight(job.get("company", ""), job.get("title", ""), job.get("description_text", ""))
        
        job["match_percentage"] = match_pct
        job["match_analysis"] = analysis
        job["company_hook_insight"] = hook_insight
        job["status"] = "analyzed"
        updated_count += 1

    save_database(db)
    generate_markdown(db)
    print(f"✨ Analyst ferdig: Analyserte {updated_count} stillinger.")

if __name__ == "__main__":
    run_analyst()
