import { Job, UserProfile, GenerateApplicationRequest, ApplicationResponse, ExportDocxRequest } from '../types/job';

const API_BASE = 'http://localhost:8000/api';

export async function fetchJobs(params?: {
  q?: string;
  min_match?: number;
  status?: string;
  app_status?: string;
}): Promise<Job[]> {
  const url = new URL(`${API_BASE}/jobs`);
  if (params?.q) url.searchParams.append('q', params.q);
  if (params?.min_match) url.searchParams.append('min_match', params.min_match.toString());
  if (params?.status) url.searchParams.append('status', params.status);
  if (params?.app_status) url.searchParams.append('app_status', params.app_status);

  const res = await fetch(url.toString());
  if (!res.ok) {
    throw new Error(`Feil ved henting av stillinger: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchProfile(): Promise<UserProfile> {
  const res = await fetch(`${API_BASE}/profile`);
  if (!res.ok) {
    throw new Error(`Feil ved henting av profil: ${res.statusText}`);
  }
  return res.json();
}

export async function saveProfile(profile: UserProfile): Promise<UserProfile> {
  const res = await fetch(`${API_BASE}/profile`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profile),
  });
  if (!res.ok) {
    throw new Error(`Feil ved lagring av profil: ${res.statusText}`);
  }
  return res.json();
}

export async function triggerFinnScan(): Promise<{ message: string }> {
  const res = await fetch(`${API_BASE}/jobs/scan`, {
    method: 'POST',
  });
  if (!res.ok) {
    throw new Error(`Feil ved oppstart av skanning: ${res.statusText}`);
  }
  return res.json();
}

export async function updateJobStatus(jobId: string, status: string): Promise<void> {
  const res = await fetch(`${API_BASE}/jobs/${jobId}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status })
  });
  if (!res.ok) {
    throw new Error(`Feil ved oppdatering av status: ${res.statusText}`);
  }
}

export async function generateApplication(
  req: GenerateApplicationRequest
): Promise<ApplicationResponse> {
  const res = await fetch(`${API_BASE}/jobs/generate-application`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(req),
  });
  if (!res.ok) {
    throw new Error(`Feil ved generering av søknad: ${res.statusText}`);
  }
  return res.json();
}

export async function exportDocx(req: ExportDocxRequest): Promise<Blob> {
  const res = await fetch(`${API_BASE}/jobs/export-docx`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(req),
  });
  if (!res.ok) {
    throw new Error(`Feil ved generering av Word-dokument: ${res.statusText}`);
  }
  return res.blob();
}
