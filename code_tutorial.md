# 🎓 Interaktiv Kode-Workshop: Python & TypeScript for FinnJobScout

Velkommen til din personlige kodeskole! Her går vi **linje for linje** gjennom hvordan både **Python-backenden** og **TypeScript-frontenden** i FinnJobScout er bygget opp.

---

## 🐍 DEL 1: Python & FastAPI Backend

I backenden bruker vi tre hovedkonsepter:
1. **FastAPI & Uvicorn**: Et av verdens raskeste Python-rammeverk for å lagre og servere data via REST API-er.
2. **Pydantic Modeller**: En måte å **validere** at data vi får inn fra nettleseren har riktig type (f.eks. at `age` er et tall og `title` er tekst).
3. **Prompt Engineering & Gemini API**: Hvordan Python leser filer (`.md` og `.json`) og sender dem til AI-modeller.

---

### 1.1 Hvordan et REST API fungerer i `backend/main.py`

Se på denne koden fra [`backend/main.py`](file:///Users/markus/privatKoding/FinnJobScout/backend/main.py):

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI(title="FinnJobScout API")

# 1. Pydantic modell som definerer datastrukturen til en stilingsforespørsel
class StatusUpdateRequest(BaseModel):
    status: str  # Krever at status må være en streng (tekst)

# 2. HTTP GET rute: Henter data når nettleseren ber om /api/jobs
@app.get("/api/jobs")
def get_jobs(min_match: int = 0):
    db = read_db()
    filtered = [job for job in db.values() if job["match_percentage"] >= min_match]
    return filtered

# 3. HTTP PATCH rute: Endrer status på en spesifikk stilling
@app.patch("/api/jobs/{job_id}/status")
def update_job_status(job_id: str, payload: StatusUpdateRequest):
    db = read_db()
    if job_id not in db:
        raise HTTPException(status_code=404, detail="Stilling ikke funnet")
    
    db[job_id]["application_status"] = payload.status
    save_database(db)
    return {"message": "Status oppdatert!", "job": db[job_id]}
```

#### 💡 Hva skjer her?
* **`@app.get("/api/jobs")`**: Dette kalles en **Python Dekoratør** (`@`). Den forteller FastAPI: *"Når noen sender en GET-forespørsel til `/api/jobs`, kjør denne funksjonen."*
* **List Comprehension (`[job for job in ...]`)**: En elegant Python-måte å filtrere lister på med én enkelt linje.
* **`raise HTTPException(status_code=404)`**: Hvis stillings-ID-en ikke finnes i databasen, sender Python en standard HTTP 404-feilmelding tilbake til nettleseren.

---

### 1.2 Hvordan AI-generatoren bygger prompten i `backend/ai_generator.py`

Se på denne koden fra [`backend/ai_generator.py`](file:///Users/markus/privatKoding/FinnJobScout/backend/ai_generator.py):

```python
import os
import profile_manager

def generate_cover_letter(job: dict, custom_notes: str = "") -> str:
    # Hent innstillinger fra profile_manager
    settings = profile_manager.load_settings()
    
    # f-strings i Python (tillater variabler direkte i teksten med {variabel})
    system_instruction = f"""
    Du skal skrive en skreddersydd jobbsøknad for {settings['full_name']} ({settings['age']} år).
    Personlighetstrekk: {', '.join(settings['personality_traits'])}
    Tone: {settings['tone_of_voice']}
    CV: {settings['cv_experiences']}
    """
    
    # Kalle Gemini 2.5 Flash API dersom API-nøkkel finnes
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Stilling: {job['title']} hos {job['company']}. Beskrivelse: {job['description_text']}",
            config={"system_instruction": system_instruction, "temperature": 0.7}
        )
        return response.text
```

---

## 🟦 DEL 2: TypeScript & React Frontend

I frontenden bruker vi tre hovedkonsepter:
1. **TypeScript Interfaces**: Definerer "kontrakten" for objekter slik at du får auto-completion og unngår stavefeil.
2. **React Components & JSX**: Funksjoner som returnerer HTML-lignende kode (`JSX`).
3. **React Hooks (`useState` og `useEffect`)**: Håndterer tilstand (data som endrer seg) og bivirkninger (f.eks. å hente data når komponenten vises).

---

### 2.1 TypeScript Typer i `frontend/src/types/job.ts`

Se på denne koden fra [`frontend/src/types/job.ts`](file:///Users/markus/privatKoding/FinnJobScout/frontend/src/types/job.ts):

```typescript
// Et TypeScript Interface definerer nøyaktig hvilke felt et Job-objekt HAR LOV til å ha
export interface Job {
  id: string;                  // MÅ være tekst (f.eks. "386221789")
  title: string;               // MÅ være tekst (f.eks. "Fullstackutvikler")
  company: string;
  match_percentage: number;    // MÅ være tall (f.eks. 85)
  reason?: string;             // '?' betyr at feltet er VALGFRITT (kan være undefined)
  application_status?: 'not_applied' | 'draft' | 'applied'; // Kun disse tre verdiene er tillatt!
}
```

#### 💡 Hvorfor bruke TypeScript?
Hvis du ved et uhell prøver å skrive `job.tittel` i stedet for `job.title`, eller setter `match_percentage = "mye"`, vil TypeScript krasje under **bygging** med en klar feilmelding, i stedet for at appen krasjer når en bruker bruker den!

---

### 2.2 React Component & Hooks i `frontend/src/components/JobCard.tsx`

Se på denne koden fra [`frontend/src/components/JobCard.tsx`](file:///Users/markus/privatKoding/FinnJobScout/frontend/src/components/JobCard.tsx):

```tsx
import React from 'react';
import { Job } from '../types/job';

// 1. Interface for Props (data som sendes INN til denne komponenten fra foreldren)
interface JobCardProps {
  job: Job;
  onOpenGenerateModal: (job: Job) => void;
}

// 2. Menneskelig React Komponent
export const JobCard: React.FC<JobCardProps> = ({ job, onOpenGenerateModal }) => {
  // Dynamisk klasse basert på match %
  const badgeColor = job.match_percentage >= 70 ? 'bg-emerald-500/20 text-emerald-300' : 'bg-blue-500/20 text-blue-300';

  return (
    <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
      <div className={`text-xs px-2.5 py-1 rounded-lg ${badgeColor}`}>
        🎯 {job.match_percentage}% Match
      </div>
      <h3 className="text-base font-semibold text-slate-100 mt-2">{job.title}</h3>
      <p className="text-sm text-slate-400">{job.company}</p>

      {/* Klikk på knappen utløser funksjonen som ble sendt inn som prop */}
      <button
        onClick={() => onOpenGenerateModal(job)}
        className="mt-4 w-full bg-blue-600 hover:bg-blue-500 text-white py-2 rounded-xl text-xs font-semibold"
      >
        ✨ Generer AI-Søknad
      </button>
    </div>
  );
};
```

---

## 🧪 Din Første Interaktive Kodeoppgave!

La oss gjøre en **praktisk endring sammen** i koden slik at du får skrive koden selv og se resultatene live!

### Oppgave: Legg til et nytt sammendragsfelt i UI-en!

Vi vil legge til et nytt felt på stillingskortene: **"Publisert dato"**.

#### Steg 1 (TypeScript):
Åpne [`frontend/src/components/JobCard.tsx`](file:///Users/markus/privatKoding/FinnJobScout/frontend/src/components/JobCard.tsx) i editoren din.

Finn linjen der sted og frist vises (rundt linje 45):
```tsx
<span className="flex items-center gap-1">
  <Calendar size={13} className="text-slate-500" /> Frist: {job.application_deadline || 'Ukjent'}
</span>
```

Prøv å legge til dette rett under:
```tsx
<span className="flex items-center gap-1">
  <Clock size={13} className="text-slate-500" /> Publisert: {job.date_published || 'Ukjent'}
</span>
```

Sjekk nettleseren på `http://localhost:3000` – du vil se at publiseringsdatoen nå dukker opp på alle kortene!

---

### Hva vil du utforske videre?
1. Skal vi gå gjennom hvordan `fetchJobs` henter JSON fra FastAPI?
2. Skal vi se på hvordan `useState` lagrer data i React?
3. Vil du at vi gjør en ny oppgave sammen?
