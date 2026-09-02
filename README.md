# 🔍 FinnJobScout UI (v2.0)

**FinnJobScout** er en universell, automatisert jobb- og søknadsportal for **alle yrker og bransjer**. Systemet skanner FINN.no for relevante stillinger, beregner match-skår mot din CV og profil, og genererer skreddersydde **Antigravity AI-søknader** på få sekunder.

---

## 🚀 Slik starter og stopper du appen lokalt

Du trenger overhodet ikke å ha Antigravity åpen for å bruke FinnJobScout! 

### 💡 1-Klikks Oppstart & Stopp (Finder)

I mappen `/Users/markus/privatKoding/FinnJobScout` finner du to 1-klikks skripter:

* **🚀 Start appen:** Dobbelklikk på **`start.command`**
  * Starter både Python FastAPI backend og React frontend, og åpner `http://localhost:3000` automatisk i nettleseren din!
* **🛑 Stopp appen:** Dobbelklikk på **`stop.command`** (eller trykk `Ctrl + C` / lukk terminalvinduet til start.command)
  * Stopper alle bakgrunnsprosesser umiddelbart slik at datamaskinen din ikke bruker strøm eller ressurser når du ikke bruker appen.

---

## 🌟 Hovedfunksjoner i v2.0

* 📊 **Universelt FINN-Søk (`finn_scout.py`)**: Henter og parser utlysninger for alle yrker (Utvikling, Helse, Salg, Økonomi, Ingeniør, Drift).
* 🧠 **Match & Krok Analyst (`job_analyst.py`)**: Beregner match-skår og henter ut unike "Vipps-kroker" basert på bedriftens egen annonsetekst.
* ⚙️ **Dynamisk Profil & CV-behandler**: Endre CV, personlighetstrekk, styrker og tone direkte i UI-en via knappen **"⚙️ Min Profil & CV"**.
* 🤖 **Antigravity AI-Søknadsmotor (`backend/ai_generator.py`)**: Genererer 100% skreddersydde 4-paragrafs Vipps-søknader med direkte FINN-krok, faglig bevis, driftserfaring og folkelig lagånd.
* 📥 **1-Klikks Word-Eksport (.docx)**: Rediger teksten i nettleseren og last ned ferdig formaterte Word-dokumenter direkte.

---

## 📂 Filstruktur

```
FinnJobScout/
├── start.command                      # 1-klikks oppstartsskript for macOS
├── stop.command                       # 1-klikks stoppskript for macOS
├── backend/                           # Python FastAPI Backend API
│   ├── main.py                        # REST API ruter
│   ├── ai_generator.py                # Antigravity AI Engine
│   └── profile_manager.py             # Dynamisk profil- & CV-styring
├── frontend/                          # TypeScript React Frontend (Vite + Tailwind)
│   ├── src/components/                # UI Komponenter (Header, Cards, Modals)
│   └── src/types/                     # TypeScript Interfaces
├── finn_scout.py                      # FINN.no web-scraper
├── job_analyst.py                     # Matching- & analysalgoritme
├── user_profile/                      # Brukerinnstillinger & masterprofil
│   └── user_settings.json             # Din private profil, CV & innstillinger
├── soknadsbrev/                       # Mappe for lagrede .md og .docx søknader
└── README.md                          # Prosjektdokumentasjon
```
