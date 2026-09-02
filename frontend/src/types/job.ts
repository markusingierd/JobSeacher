// TypeScript typer for FinnJobScout

export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  url: string;
  status: 'new' | 'analyzed' | 'excluded' | string;
  reason?: string;
  date_found?: string;
  date_published?: string;
  application_deadline?: string;
  match_percentage: number;
  match_analysis?: string;
  company_hook_insight?: string;
  application_status?: 'not_applied' | 'draft' | 'applied' | 'rejected' | 'interview' | string;
  applied_file?: string;
  description_text?: string;
}

export interface UserProfile {
  full_name: string;
  age: number;
  current_title: string;
  target_category: string;
  tone_of_voice: string;
  personality_traits: string[];
  cv_experiences: string;
  custom_search_keywords: string[];
  location_filter: string;
}

export interface GenerateApplicationRequest {
  job_id: string;
  custom_notes?: string;
}

export interface ApplicationResponse {
  job_id: string;
  job_title: string;
  company: string;
  cover_letter_markdown: string;
}

export interface ExportDocxRequest {
  job_id: string;
  company: string;
  job_title: string;
  content_markdown: string;
}
