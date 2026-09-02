#!/usr/bin/env python3
"""
FINN Job Scout for Markus Hysvær Ingierd
----------------------------------------
Søker og ekstraherer IT/utvikler-stillinger fra FINN.no for Oslo og omegn.
Ekstraherer strukturert data (JSON-LD / Schema.org) for minimal tokenbruk
og oppdaterer relevante_stillinger_database.json.
"""

import json
import re
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
DB_FILE = BASE_DIR / "relevante_stillinger_database.json"

# Nøkkelord som automatisk ekskluderer stillinger
EXCLUDE_KEYWORDS = [
    "senior", "lead", "principal", "direktør", "seksjonsleder", 
    "avdelingsleder", "cto", "arkitekt - senior", "head of"
]

# FINN.no søke-URLer (IT, Utvikling, Frontend/Backend, Kotlin, React, Python, AI, IT-drift i Oslo og omegn)
FINN_SEARCH_URLS = [
    "https://www.finn.no/job/fulltime/search.html?q=utvikler&location=1.20001.20061",
    "https://www.finn.no/job/fulltime/search.html?q=systemutvikler&location=1.20001.20061",
    "https://www.finn.no/job/fulltime/search.html?q=fullstack&location=1.20001.20061",
    "https://www.finn.no/job/fulltime/search.html?q=frontend&location=1.20001.20061",
    "https://www.finn.no/job/fulltime/search.html?q=backend&location=1.20001.20061",
    "https://www.finn.no/job/fulltime/search.html?q=kotlin&location=1.20001.20061",
    "https://www.finn.no/job/fulltime/search.html?q=react&location=1.20001.20061",
    "https://www.finn.no/job/fulltime/search.html?q=typescript&location=1.20001.20061",
    "https://www.finn.no/job/fulltime/search.html?q=python&location=1.20001.20061",
    "https://www.finn.no/job/fulltime/search.html?q=ai&location=1.20001.20061",
    "https://www.finn.no/job/fulltime/search.html?q=driftstekniker&location=1.20001.20061",
    "https://www.finn.no/job/fulltime/search.html?occupations=0.23"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def load_database():
    if DB_FILE.exists():
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] Feil ved lesing av database: {e}")
    return {}

def save_database(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    print(f"[+] Databasen ble oppdatert. Totalt {len(db)} stillinger i databasen.")

def fetch_url(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode("utf-8")
    except Exception as e:
        print(f"[!] Feil ved henting av {url}: {e}")
        return None

def extract_job_ids_from_search(html):
    if not html:
        return []
    # Ekstraher FINN ad IDs fra søkeresultat
    matches = re.findall(r'/ad/(\d+)', html)
    return list(set(matches))

def fetch_and_parse_ad(ad_id):
    url = f"https://www.finn.no/job/ad/{ad_id}"
    html = fetch_url(url)
    if not html:
        return None

    # Ekstraher JSON-LD (Schema.org JobPosting)
    json_ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    
    title = ""
    company = ""
    location = ""
    description = ""
    date_published = "Ukjent"
    application_deadline = "Ukjent"

    for match in json_ld_matches:
        try:
            data = json.loads(match)
            if isinstance(data, dict) and data.get("@type") == "JobPosting":
                title = data.get("title", "")
                company = data.get("hiringOrganization", {}).get("name", "") if isinstance(data.get("hiringOrganization"), dict) else ""
                loc_data = data.get("jobLocation", {})
                if isinstance(loc_data, dict):
                    addr = loc_data.get("address", {})
                    if isinstance(addr, dict):
                        location = addr.get("addressLocality", "") or addr.get("addressRegion", "")
                elif isinstance(loc_data, list) and len(loc_data) > 0:
                    addr = loc_data[0].get("address", {})
                    if isinstance(addr, dict):
                        location = addr.get("addressLocality", "")
                
                description = data.get("description", "")
                date_published = data.get("datePosted", "Ukjent")[:10] if data.get("datePosted") else "Ukjent"
                application_deadline = data.get("validThrough", "Ukjent")[:10] if data.get("validThrough") else "Ukjent"
                break
        except Exception:
            continue

    # Fallback om JSON-LD ikke fantes
    if not title:
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
        if title_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()

    # Rens beskrivelsestekst for HTML-tags
    clean_desc = re.sub(r'<[^>]+>', ' ', description)
    clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()

    # Sjekk for ekskluderingsord
    status = "new"
    reason = ""
    for kw in EXCLUDE_KEYWORDS:
        if kw in title.lower():
            status = "excluded"
            reason = f"Tittel inneholder ekskluderingsordet '{kw.capitalize()}'"
            break

    today_str = datetime.now().strftime("%Y-%m-%d")

    return {
        "id": str(ad_id),
        "title": title or f"Stilling {ad_id}",
        "company": company or "Ukjent bedrift",
        "location": location or "Oslo/Omegn",
        "url": url,
        "status": status,
        "reason": reason,
        "experience_req": "Ukjent",
        "date_found": today_str,
        "date_published": date_published,
        "application_deadline": application_deadline,
        "match_percentage": 0,
        "match_analysis": "",
        "description_text": clean_desc
    }

def run_scout():
    print("🔍 Starter FINN Job Scout for Markus...")
    db = load_database()
    initial_count = len(db)

    found_ids = set()
    for search_url in FINN_SEARCH_URLS:
        html = fetch_url(search_url)
        ids = extract_job_ids_from_search(html)
        found_ids.update(ids)

    print(f"📊 Fant {len(found_ids)} unik(e) stillings-IDer på FINN.")
    
    new_adds = 0
    for ad_id in found_ids:
        if str(ad_id) in db:
            continue
        
        print(f"  -> Henter stilling {ad_id}...")
        ad_data = fetch_and_parse_ad(ad_id)
        if ad_data:
            db[str(ad_id)] = ad_data
            new_adds += 1

    save_database(db)
    print(f"✨ Scout ferdig: {new_adds} ny(e) stilling(er) lagt til i databasen.")

if __name__ == "__main__":
    run_scout()
