import React from 'react';
import { Search, RefreshCw, Briefcase, Award, CheckCircle2, Settings, User } from 'lucide-react';
import { Job } from '../types/job';

interface DashboardHeaderProps {
  jobs: Job[];
  isScanning: boolean;
  onTriggerScan: () => void;
  onOpenProfile: () => void;
}

export const DashboardHeader: React.FC<DashboardHeaderProps> = ({
  jobs,
  isScanning,
  onTriggerScan,
  onOpenProfile,
}) => {
  const totalJobs = jobs.length;
  const highMatchJobs = jobs.filter((j) => j.match_percentage >= 60).length;
  const appliedJobs = jobs.filter((j) => j.application_status === 'applied' || j.application_status === 'draft').length;

  return (
    <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur-md sticky top-0 z-20 px-4 lg:px-8 py-4">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        {/* Logo & Tittel */}
        <div>
          <div className="flex items-center gap-2">
            <span className="text-2xl">🔍</span>
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
              FinnJobScout UI
            </h1>
            <span className="text-xs bg-blue-500/20 text-blue-300 border border-blue-500/30 px-2 py-0.5 rounded-full font-medium">
              v2.0 • Universal & AI
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Universell jobbportal for alle yrker. Scann FINN.no og generer skreddersydde Antigravity-søknader.
          </p>
        </div>

        {/* Stats-kort & Handlingsknapper */}
        <div className="flex items-center gap-3 w-full md:w-auto overflow-x-auto pb-1 md:pb-0">
          <div className="bg-slate-800/80 border border-slate-700/60 px-3 py-2 rounded-xl flex items-center gap-3 shrink-0">
            <div className="p-2 bg-blue-500/10 text-blue-400 rounded-lg">
              <Briefcase size={18} />
            </div>
            <div>
              <p className="text-[10px] text-slate-400 font-medium uppercase tracking-wider">Stillinger</p>
              <p className="text-sm font-bold text-slate-100">{totalJobs}</p>
            </div>
          </div>

          <div className="bg-slate-800/80 border border-slate-700/60 px-3 py-2 rounded-xl flex items-center gap-3 shrink-0">
            <div className="p-2 bg-emerald-500/10 text-emerald-400 rounded-lg">
              <Award size={18} />
            </div>
            <div>
              <p className="text-[10px] text-slate-400 font-medium uppercase tracking-wider">Høy Match</p>
              <p className="text-sm font-bold text-emerald-400">{highMatchJobs}</p>
            </div>
          </div>

          <div className="bg-slate-800/80 border border-slate-700/60 px-3 py-2 rounded-xl flex items-center gap-3 shrink-0">
            <div className="p-2 bg-purple-500/10 text-purple-400 rounded-lg">
              <CheckCircle2 size={18} />
            </div>
            <div>
              <p className="text-[10px] text-slate-400 font-medium uppercase tracking-wider">Søkt / Utkast</p>
              <p className="text-sm font-bold text-purple-300">{appliedJobs}</p>
            </div>
          </div>

          {/* Min Profil Knapp */}
          <button
            onClick={onOpenProfile}
            className="flex items-center gap-1.5 px-3.5 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold border border-slate-700 transition-colors shrink-0"
          >
            <User size={15} className="text-blue-400" />
            <span>Min Profil & CV</span>
          </button>

          {/* Scann-knapp */}
          <button
            onClick={onTriggerScan}
            disabled={isScanning}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-xl font-semibold text-sm transition-all duration-200 shadow-lg shrink-0 ${
              isScanning
                ? 'bg-slate-800 text-slate-400 cursor-not-allowed border border-slate-700'
                : 'bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-500 hover:to-emerald-500 text-white shadow-blue-500/20 hover:scale-[1.02] active:scale-[0.98]'
            }`}
          >
            <RefreshCw size={16} className={isScanning ? 'animate-spin text-blue-400' : ''} />
            <span>{isScanning ? 'Skanner FINN...' : 'Scann FINN Nå'}</span>
          </button>
        </div>
      </div>
    </header>
  );
};
