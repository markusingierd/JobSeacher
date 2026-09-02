import React from 'react';
import { ExternalLink, Sparkles, MapPin, Calendar, CheckCircle2, Clock, FileText } from 'lucide-react';
import { Job } from '../types/job';

interface JobCardProps {
  job: Job;
  onOpenGenerateModal: (job: Job) => void;
  onStatusChange: (jobId: string, newStatus: string) => void;
}

export const JobCard: React.FC<JobCardProps> = ({
  job,
  onOpenGenerateModal,
  onStatusChange,
}) => {
  const getMatchBadgeColor = (pct: number) => {
    if (pct >= 70) return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30';
    if (pct >= 50) return 'bg-blue-500/20 text-blue-300 border-blue-500/30';
    if (pct >= 30) return 'bg-amber-500/20 text-amber-300 border-amber-500/30';
    return 'bg-slate-700/50 text-slate-400 border-slate-600/30';
  };

  const isApplied = job.application_status === 'applied';
  const isDraft = job.application_status === 'draft';

  return (
    <div className="bg-slate-900/80 border border-slate-800 hover:border-slate-700/80 rounded-2xl p-5 transition-all duration-200 hover:shadow-xl hover:shadow-blue-500/5 flex flex-col justify-between group">
      <div>
        {/* Top Header: Match Badge & Status */}
        <div className="flex items-center justify-between gap-2 mb-3">
          <span
            className={`text-xs font-bold px-2.5 py-1 rounded-lg border flex items-center gap-1.5 ${getMatchBadgeColor(
              job.match_percentage
            )}`}
          >
            <span className="text-[10px]">🎯</span> {job.match_percentage}% Match
          </span>

          <div className="flex items-center gap-2">
            {isApplied && (
              <span className="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded-md flex items-center gap-1">
                <CheckCircle2 size={12} /> Søkt
              </span>
            )}
            {isDraft && (
              <span className="text-xs bg-purple-500/10 text-purple-300 border border-purple-500/20 px-2 py-0.5 rounded-md flex items-center gap-1">
                <FileText size={12} /> Utkast
              </span>
            )}
          </div>
        </div>

        {/* Tittel & Bedrift */}
        <h3 className="text-base font-semibold text-slate-100 group-hover:text-blue-400 transition-colors line-clamp-2">
          {job.title}
        </h3>
        <p className="text-sm font-medium text-slate-400 mt-0.5">{job.company}</p>

        {/* Info tags: Sted & Frist */}
        <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400 mt-3 pt-3 border-t border-slate-800/80">
          <span className="flex items-center gap-1">
            <MapPin size={13} className="text-slate-500" /> {job.location || 'Oslo/Omegn'}
          </span>
          <span className="flex items-center gap-1">
            <Calendar size={13} className="text-slate-500" /> Frist: {job.application_deadline || 'Ukjent'}
          </span>
        </div>

        {/* Match Analyse / Nøkkelord */}
        {job.match_analysis && (
          <p className="text-xs text-slate-400 mt-3 bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/60">
            <strong className="text-slate-300 font-semibold">Analyse:</strong> {job.match_analysis}
          </p>
        )}

        {/* Vipps-Krok forslag */}
        {job.company_hook_insight && (
          <div className="text-xs text-blue-300/90 mt-2 bg-blue-950/30 p-2.5 rounded-lg border border-blue-900/30">
            <strong className="text-blue-400 font-semibold">💡 Vipps-Krok:</strong> {job.company_hook_insight}
          </div>
        )}
      </div>

      {/* Handlingsknapper i bunn */}
      <div className="flex items-center gap-2 mt-5 pt-3 border-t border-slate-800/80">
        <a
          href={job.url}
          target="_blank"
          rel="noreferrer"
          className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2 bg-slate-800/80 hover:bg-slate-700 text-slate-300 hover:text-white rounded-xl text-xs font-medium transition-colors border border-slate-700/60"
        >
          <ExternalLink size={13} />
          <span>Åpne på FINN</span>
        </a>

        <button
          onClick={() => onOpenGenerateModal(job)}
          className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2 bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-500 hover:to-emerald-500 text-white rounded-xl text-xs font-semibold transition-all shadow-md shadow-blue-500/10 hover:scale-[1.02] active:scale-[0.98]"
        >
          <Sparkles size={13} className="text-yellow-300 animate-pulse" />
          <span>{isDraft || isApplied ? 'Se / Endre Søknad' : 'Generer AI-Søknad'}</span>
        </button>
      </div>
    </div>
  );
};
