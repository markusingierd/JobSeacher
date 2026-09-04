# 🔍 JobbsøkerNettside (FinnJobScout v2.0)

**JobbsøkerNettside** er en universell, lokal-først jobb- og AI-søknadsportal for **alle yrker og bransjer**. Applikasjonen skanner FINN.no for relevante stillinger, beregner en presis match-skår mot din CV og brukerprofil via en 3-tier analysealgoritme, og genererer skreddersydde, vinnende AI-søknader uten oppstyltet konsulentspråk.

---

## ⚡️ Rask Oppstart (Quick Start)

###  macOS (1-Klikks Oppstart)

1. **Klon prosjektet:**
   ```bash
   git clone https://github.com/markusingierd/JobSeacher.git
   cd JobSeacher
   ```
2. **Start appen:**
   * Dobbelklikk på **`start.command`** i Finder (eller kjør `./start.command` i Terminal).
   * Skriptet setter opp virtuelt Python-miljø (`.venv`), installerer Node-pakker, starter backend og frontend, og åpner `http://127.0.0.1:3000` i nettleseren din!
3. **Stopp appen:**
   * Dobbelklikk på **`stop.command`** eller trykk `Ctrl + C` i terminalvinduet.

---

### 💻 Manuell Oppstart (Windows / Linux / Mac)

#### 1. Backend (Python FastAPI)
```bash
# Opprett og aktiver virtuelt miljø
python3 -m venv .venv
source .venv/bin/activate  # På Windows: .venv\Scripts\activate

# Installere avhengigheter
pip install -r backend/requirements.txt

# Start backend-serveren
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

#### 2. Frontend (React + Vite + Tailwind)
```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 3000
```

Åpne deretter `http://127.0.0.1:3000` i nettleseren din.

---

## 💰 100 % Gratis-Garanti (0 kr)

* **Google AI Studio Free Tier (Gemini 2.5 Flash)**:
  Appen benytter Gemini 2.5 Flash som har **1 500 gratis forespørsler per dag** uten behov for kredittkort eller betalingsinformasjon.
* **Innebygd Lokal Python-motor (Offline Fallback)**:
  Dersom du ikke har en API-nøkkel eller er offline, kobles automatisk den lokale Python-motoren inn. Den genererer skreddersydde søknader 100 % lokalt på din maskin – uansett netttilgang.
* **Ingen skjulte cloud-utgifter**: Alt kjører på din egen maskin (`localhost`).

---

## 🔒 100 % GDPR & Lokal Personvern (Privacy First)

* **Ingen sky-lagring av personopplysninger**: Din masterprofil, CV, innstillinger og lagrede søknader oppbevares 100 % utelukkende lokalt i mappen `user_profile/` og `soknadsbrev/`.
* **Kildekode på GitHub er anonymisert**: Ingen personfølsom data publiseres eller committes til Git. `.gitignore` beskytter dine private dokumenter.

---

## 🌟 Nøkkelfunksjoner i v2.0

* 📊 **Universal 3-Tier Match Engine**: Analyserer FINN.no-annonser mot din CV og gir en realistisk match-prosent (inkludert Graduate/Junior/Entry-level stillinger).
* 📝 **Renskrevne AI-søknader**: Genererer 4-paragrafs Vipps-søknader med direkte bedriftskrok, faglig bevis (80% IT/fagfokus), feilsøkingssinn og lagånd.
* 📄 **Klar for Word-Eksport**: Ingen markdown-støy (`*`, `**`, `#`) i teksten. Lim inn rett i Word eller last ned ferdig formaterte `.docx`-filer.
* ⚙️ **Dynamisk Profilbehandling**: Endre CV-erfaringer, personlighetstrekk og tone-of-voice direkte i nettportalen.

---

## 📂 Filstruktur

```
JobSeacher/
├── start.command                      # 1-klikks oppstartsskript for macOS
├── stop.command                       # 1-klikks stoppskript for macOS
├── backend/                           # Python FastAPI Backend API
│   ├── main.py                        # REST API ruter
│   ├── ai_generator.py                # Antigravity AI Engine & Markdown Stripper
│   ├── profile_manager.py             # Dynamisk profil- & CV-styring
│   └── requirements.txt               # Backend Python-avhengigheter
├── frontend/                          # TypeScript React Frontend (Vite + Tailwind)
│   ├── src/components/                # UI Komponenter (Header, Cards, Modals)
│   └── src/types/                     # TypeScript Interfaces
├── finn_scout.py                      # FINN.no web-scraper
├── job_analyst.py                     # Matching- & analysalgoritme v2.0
├── user_profile/                      # Brukerinnstillinger & masterprofil (GDPR-beskyttet)
│   └── user_settings.json             # Din private profil, CV & innstillinger
├── soknadsbrev/                       # Mappe for lagrede .md og .docx søknader
└── README.md                          # Prosjektdokumentasjon
```

---

## 📄 Lisens & Bidrag

Dette prosjektet er open-source og fritt tilgjengelig for alle som ønsker en effektiv, privat og gratis måte å søke jobber på.
