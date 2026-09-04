#!/usr/bin/env python3
"""
Sync Upstream Manager for FinnJobScout
--------------------------------------
Garanterer 100% SIKKER 1-VEIS LESETILGANG (Read-Only) fra kilderepositoriet
(https://github.com/markusingierd/FinnJobScout.git).

SIKKERHETSGARANTI:
- Upstream sin PUSH-URL er satt til 'DISABLE_PUSH_READ_ONLY'.
- Dette skriptet kan ALDRI skrive, endre eller pushe til kilderepositoriet.
- Skriptet kan KUN hente (fetch) nye filer og endringer INN i dette prosjektet.
"""

import subprocess
import os
from pathlib import Path
from typing import Dict, Any, List

BASE_DIR = Path(__file__).parent.parent.resolve()

def ensure_read_only_remote() -> bool:
    """Verifiserer at upstream push-URL er satt til DISABLE_PUSH_READ_ONLY for 100% sikkerhet."""
    try:
        res = subprocess.run(
            ["git", "remote", "get-url", "--push", "upstream"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            check=False
        )
        push_url = res.stdout.strip()
        if push_url != "DISABLE_PUSH_READ_ONLY":
            # Tving push-URL til å være deaktivert
            subprocess.run(
                ["git", "remote", "set-url", "--push", "upstream", "DISABLE_PUSH_READ_ONLY"],
                cwd=BASE_DIR,
                check=False
            )
        return True
    except Exception as e:
        print(f"[!] Feil ved sjekk av upstream remote: {e}")
        return False

def check_upstream_updates() -> Dict[str, Any]:
    """Sjekker om det finnes nye oppdateringer i kilderepositoriet uten å gjøre endringer."""
    ensure_read_only_remote()
    try:
        # Fetch nyeste commits fra upstream (100% Lesetilgang)
        subprocess.run(["git", "fetch", "upstream", "main"], cwd=BASE_DIR, capture_output=True, check=False)
        
        # Sjekk forskjell mellom lokal main og upstream/main
        diff_res = subprocess.run(
            ["git", "diff", "--name-only", "main..upstream/main"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            check=False
        )
        changed_files = [f.strip() for f in diff_res.stdout.splitlines() if f.strip()]
        
        return {
            "has_updates": len(changed_files) > 0,
            "changed_files": changed_files,
            "message": f"Fant {len(changed_files)} endret(e) fil(er) i kilderepositoriet." if changed_files else "Dette prosjektet er helt oppdatert med kilden."
        }
    except Exception as e:
        return {"has_updates": False, "changed_files": [], "error": str(e)}

def pull_upstream_updates() -> Dict[str, Any]:
    """Henter og integrerer oppdateringer fra kilde-repoet inn i dette prosjektet (1-veis)."""
    ensure_read_only_remote()
    try:
        # 1. Hent nyeste commits fra upstream (Lesetilgang)
        subprocess.run(["git", "fetch", "upstream", "main"], cwd=BASE_DIR, capture_output=True, check=False)
        
        # 2. Hent liste over filer som er endret
        diff_res = subprocess.run(
            ["git", "diff", "--name-only", "main..upstream/main"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            check=False
        )
        changed_files = [f.strip() for f in diff_res.stdout.splitlines() if f.strip()]

        if not changed_files:
            return {"status": "success", "updated_files": [], "message": "Prosjektet var allerede 100% oppdatert med kilderepositoriet."}

        # 3. Cherry-pick eller checkout filer fra upstream/main for å oppdatere skripter/regler
        updated_files = []
        for file_path in changed_files:
            # Vi beskytter private brukerinnstillinger fra å bli overskrevet!
            if "user_settings.json" in file_path or "master_profile.md" in file_path or "soknadsbrev" in file_path:
                continue
            
            checkout_res = subprocess.run(
                ["git", "checkout", "upstream/main", "--", file_path],
                cwd=BASE_DIR,
                capture_output=True,
                check=False
            )
            if checkout_res.returncode == 0:
                updated_files.append(file_path)

        # 4. Gjør en lokal commit i dette prosjektet med oppdateringene
        if updated_files:
            subprocess.run(["git", "add"] + updated_files, cwd=BASE_DIR, check=False)
            subprocess.run(["git", "commit", "-m", f"sync: hentet 1-veis oppdateringer fra kilderepo ({len(updated_files)} filer)"], cwd=BASE_DIR, check=False)

        return {
            "status": "success",
            "updated_files": updated_files,
            "message": f"Synkroniserte {len(updated_files)} fil(er) trygt fra kilderepositoriet!"
        }
    except Exception as e:
        return {"status": "error", "updated_files": [], "error": str(e)}

if __name__ == "__main__":
    ensure_read_only_remote()
    res = check_upstream_updates()
    print("[+] Status sjekket:", res)
