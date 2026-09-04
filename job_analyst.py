#!/usr/bin/env python3
"""
Job Analyst for Markus Hysvær Ingierd (v2.0 Universal Match Engine)
------------------------------------------------------------------
Leser relevante_stillinger_database.json og beregner en universell,
objektiv match-prosent for ALLE stillinger på FINN.no basert på:
1. Karrierenivå (Junior/Graduate/Nyutdannet boost)
2. Fagfelt & Utviklerrolle (Software, Web, Mobil, Drift)
3. Spesifikk Tek-stakk (Kotlin, React, Next.js, Python, TypeScript, SQL osv.)
"""

import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
DB_FILE = BASE_DIR / "relevante_stillinger_database.json"
PROFILE_FILE = BASE_DIR / "markus_master_profil.md"
OUTPUT_MD = BASE_DIR / "relevante_stillinger.md"

# Kilde-prosjekt database sti for 1-veis fletting
SOURCE_JOBSKNADER_DB = Path("/Users/markus/privatKoding/jobsknader/relevante_stillinger_database.json")

def load_database():
    db = {}
    if DB_FILE.exists():
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                db = json.load(f)
        except Exception:
            pass

    if SOURCE_JOBSKNADER_DB.exists():
        try:
            with open(SOURCE_JOBSKNADER_DB, "r", encoding="utf-8") as f:
                source_db = json.load(f)
                for job_id, job_data in source_db.items():
                    if job_id not in db:
                        db[job_id] = job_data
        except Exception as e:
            print(f"[!] Kunne ikke flette kilde-database: {e}")

    return db

def save_database(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def extract_company_hook_insight(company_name, job_title, description_text):
    text = (company_name + " " + job_title + " " + description_text).lower()
    
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
    """
    UNIVERSELL 3-PILLER MATCH ALGORITME v2
    ---------------------------------------
    1. Karrierenivå-match (Maks 35p)
    2. Fagfelt & Utviklerrolle (Maks 35p)
    3. Spesifikk Tek-Stakk (Maks 30p)
    """
    text = (job_title + " " + description_text).lower()
    title_low = job_title.lower()

    # 1. KARRIERENIVÅ-MATCH (Maks 35 poeng)
    is_junior_grad = any(k in text for k in [
        "junior", "graduate", "nyutdannet", "trainee", "internship", 
        "intern", "startstilling", "førstekonsulent", "sommerjobb", "entry level"
    ])
    is_senior_lead = any(k in text for k in [
        "senior", "lead", "principal", "direktør", "avdelingsleder", "cto", "head of"
    ])

    if is_junior_grad:
        level_score = 35
    elif not is_senior_lead:
        level_score = 25
    else:
        level_score = 5

    # 2. FAGFELT & UTVIKLERROLLE (Maks 35 poeng)
    is_core_dev_title = any(k in title_low for k in [
        "utvikler", "developer", "software", "systemutvikler", "fullstack", 
        "frontend", "backend", "driftstekniker", "programmerer", "ingeniør", "it"
    ])
    
    domain_keywords = [
        "utvikler", "systemutvikler", "programvareutvikler", "fullstack", 
        "frontend", "backend", "programmering", "it-utvikler", "bachelor", 
        "sky", "cloud", "mobil", "mobile", "applikasjon", "driftstekniker", 
        "drift", "feilsøking", "systemarkitektur", "web", "it", "kode", "koding"
    ]
    domain_matches = [kw for kw in domain_keywords if kw in text]
    
    if is_core_dev_title:
        domain_score = 35
    else:
        domain_score = min(35, len(domain_matches) * 10)

    # 3. SPESIFIKK TEK-STAKK & KOMPETANSE (Maks 30 poeng)
    tech_keywords = [
        "kotlin", "react", "next.js", "typescript", "javascript", "python", 
        "android", "java", "sql", "firebase", "supabase", "mapbox", 
        "jetpack compose", "git", "rest", "api", "ui", "ux", "agenter", 
        "ai", "ki", "smidig", "tverrfaglig", "automasjon", "feilsøking"
    ]
    matched_skills = [kw.capitalize() for kw in tech_keywords if kw in text]
    
    if is_junior_grad and is_core_dev_title:
        tech_score = max(15, min(30, len(matched_skills) * 6))
    else:
        tech_score = min(30, len(matched_skills) * 6)

    # TOTAL SCORE (Maks 100%)
    total_match = min(100, level_score + domain_score + tech_score)

    unique_matches = list(dict.fromkeys(matched_skills))[:5]
    if unique_matches:
        analysis = f"Matchende nøkkelord: {', '.join(unique_matches)}"
    else:
        analysis = "IT/Utvikler-stilling"

    return total_match, analysis

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
        
        for filename, content in applied_files.items():
            fn_low = filename.lower()
            if (job_id in content) or (job_url and job_url in content):
                is_applied = True
                applied_file_name = filename
                break
            company_words = [w for w in company.split() if len(w) >= 3]
            if any(w in fn_low for w in company_words) and company in content:
                is_applied = True
                applied_file_name = filename
                break
        
        if is_applied or job.get("application_status") == "applied":
            job["application_status"] = "applied"
            job["applied_file"] = f"soknadsbrev/{applied_file_name}" if applied_file_name else job.get("applied_file", "")
        else:
            if job.get("application_status") != "draft":
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

    unapplied_jobs.sort(key=lambda x: x.get("match_percentage", 0), reverse=True)
    applied_jobs.sort(key=lambda x: x.get("match_percentage", 0), reverse=True)

    now_str = datetime.now().strftime("%d.%m.%Y kl. %H:%M")
    user_name = get_user_info()

    md = []
    md.append(f"# 🎯 Relevante Stillinger for {user_name}")
    md.append(f"\n*Sist oppdatert: {now_str}*\n")
    md.append("Dette dokumentet oppdateres automatisk av `job_analyst.py`.\n")
    
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

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

def run_analyst():
    print("🧠 Starter Job Analyst for Markus (v2.0 Universal Engine)...")
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
    print(f"✨ Analyst ferdig: Re-analyserte {updated_count} stillinger med universell formel.")

if __name__ == "__main__":
    run_analyst()
