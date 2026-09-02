import React, { useState } from 'react';
import { Search, Filter, SlidersHorizontal, ArrowUpDown } from 'lucide-react';
import { Job } from '../types/job';
import { JobCard } from './JobCard';

interface JobListProps {
  jobs: Job[];
  onOpenGenerateModal: (job: Job) => void;
  onStatusChange: (jobId: string, newStatus: string) => void;
}

export const JobList: React.FC<JobListProps> = ({
  jobs,
  onOpenGenerateModal,
  onStatusChange,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [minMatch, setMinMatch] = useState<number>(0);
  const [selectedTag, setSelectedTag] = useState<string>('alle');
  const [statusFilter, setStatusFilter] = useState<'alle' | 'not_applied' | 'applied'>('alle');

  const popularTags = ['alle', 'Kotlin', 'React', 'TypeScript', 'Python', 'Android', 'Fullstack', 'Drift'];

  const filteredJobs = jobs.filter((job) => {
    // Sjekk min match %
    if (job.match_percentage < minMatch) return false;

    // Sjekk status filter
    if (statusFilter === 'not_applied' && job.application_status === 'applied') return false;
    if (statusFilter === 'applied' && job.application_status !== 'applied' && job.application_status !== 'draft') return false;

    // Sjekk ferdighets-tag
    if (selectedTag !== 'alle') {
      const tagLow = selectedTag.toLowerCase();
      const textToSearch = `${job.title} ${job.description_text || ''} ${job.match_analysis || ''}`.toLowerCase();
      if (!textToSearch.includes(tagLow)) return false;
    }

    // Sjekk fritekst søk
    if (searchQuery.trim() !== '') {
      const qLow = searchQuery.toLowerCase();
      const textToSearch = `${job.title} ${job.company} ${job.location} ${job.description_text || ''}`.toLowerCase();
      if (!textToSearch.includes(qLow)) return false;
    }

    return true;
  });

  return (
    <div className="space-y-6">
      {/* Sjøke- og filtreringslinje */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 md:p-6 space-y-4">
        <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
          {/* Søkefelt */}
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
            <input
              type="text"
              placeholder="Søk etter stillingstittel, bedrift eller nøkkelord..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"
            />
          </div>

          {/* Status Tabs */}
          <div className="flex items-center bg-slate-950 p-1 border border-slate-800 rounded-xl shrink-0">
            <button
              onClick={() => setStatusFilter('alle')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                statusFilter === 'alle' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Alle ({jobs.length})
            </button>
            <button
              onClick={() => setStatusFilter('not_applied')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                statusFilter === 'not_applied' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Ikke Søkt
            </button>
            <button
              onClick={() => setStatusFilter('applied')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                statusFilter === 'applied' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Søkt / Utkast
            </button>
          </div>
        </div>

        {/* Tags & Match Slider */}
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pt-3 border-t border-slate-800/80">
          {/* Populære ferdighets-knapper */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 lg:pb-0">
            <span className="text-xs text-slate-400 font-medium mr-1 shrink-0">Teknologi:</span>
            {popularTags.map((tag) => (
              <button
                key={tag}
                onClick={() => setSelectedTag(tag)}
                className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors shrink-0 border ${
                  selectedTag === tag
                    ? 'bg-blue-500/20 text-blue-300 border-blue-500/40'
                    : 'bg-slate-950 text-slate-400 border-slate-800 hover:border-slate-700 hover:text-slate-300'
                }`}
              >
                {tag}
              </button>
            ))}
          </div>

          {/* Slider for Min Match % */}
          <div className="flex items-center gap-3 shrink-0">
            <SlidersHorizontal size={14} className="text-slate-400" />
            <span className="text-xs text-slate-300 font-medium whitespace-nowrap">
              Min Match: <strong className="text-emerald-400">{minMatch}%</strong>
            </span>
            <input
              type="range"
              min="0"
              max="90"
              step="10"
              value={minMatch}
              onChange={(e) => setMinMatch(Number(e.target.value))}
              className="w-28 accent-blue-500 cursor-pointer"
            />
          </div>
        </div>
      </div>

      {/* Resultat-teller */}
      <div className="flex items-center justify-between text-xs text-slate-400 px-1">
        <p>Viser <strong className="text-slate-200">{filteredJobs.length}</strong> av <strong className="text-slate-200">{jobs.length}</strong> stillinger</p>
        <span className="flex items-center gap-1"><ArrowUpDown size={12} /> Sortert etter Match %</span>
      </div>

      {/* Grid med stillingskort */}
      {filteredJobs.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredJobs.map((job) => (
            <JobCard
              key={job.id}
              job={job}
              onOpenGenerateModal={onOpenGenerateModal}
              onStatusChange={onStatusChange}
            />
          ))}
        </div>
      ) : (
        <div className="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-12 text-center">
          <p className="text-base text-slate-400">Ingen stillinger matchet søkekriteriene dine.</p>
          <p className="text-xs text-slate-500 mt-1">Prøv å senke min match-prosent eller tilbakestille søkefeltet.</p>
        </div>
      )}
    </div>
  );
};
