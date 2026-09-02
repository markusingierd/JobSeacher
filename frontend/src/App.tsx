import React, { useState, useEffect } from 'react';
import { Job } from './types/job';
import { fetchJobs, triggerFinnScan, updateJobStatus } from './api/client';
import { DashboardHeader } from './components/DashboardHeader';
import { JobList } from './components/JobList';
import { ApplicationModal } from './components/ApplicationModal';
import { ProfileModal } from './components/ProfileModal';

export function App() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [isScanning, setIsScanning] = useState<boolean>(false);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [isProfileOpen, setIsProfileOpen] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const loadJobs = async () => {
    try {
      const data = await fetchJobs();
      setJobs(data);
      setError(null);
    } catch (err: any) {
      console.error('Feil ved henting av stillinger:', err);
      setError('Kunne ikke koble til FastAPI-backenden. Sjekk at serveren kjører på port 8000.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadJobs();
  }, []);

  const handleTriggerScan = async () => {
    setIsScanning(true);
    try {
      await triggerFinnScan();
      setTimeout(() => {
        loadJobs();
        setIsScanning(false);
      }, 3500);
    } catch (err: any) {
      alert(`Feil ved oppstart av skanning: ${err.message}`);
      setIsScanning(false);
    }
  };

  const handleStatusChange = async (jobId: string, newStatus: string) => {
    try {
      await updateJobStatus(jobId, newStatus);
      setJobs((prev) =>
        prev.map((j) => (j.id === jobId ? { ...j, application_status: newStatus } : j))
      );
    } catch (err) {
      console.error('Feil ved statusoppdatering:', err);
    }
  };

  const handleApplicationGenerated = (jobId: string) => {
    setJobs((prev) =>
      prev.map((j) => (j.id === jobId ? { ...j, application_status: 'draft' } : j))
    );
  };

  return (
    <div className="min-h-screen bg-[#0b0f19] text-slate-100 flex flex-col selection:bg-blue-500 selection:text-white">
      {/* Top Navigation & Header */}
      <DashboardHeader
        jobs={jobs}
        isScanning={isScanning}
        onTriggerScan={handleTriggerScan}
        onOpenProfile={() => setIsProfileOpen(true)}
      />

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 lg:px-8 py-8 flex-1 w-full">
        {loading ? (
          <div className="flex flex-col items-center justify-center py-24 space-y-4">
            <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            <p className="text-sm font-medium text-slate-400">Laster inn stillinger fra FINN-databasen...</p>
          </div>
        ) : error ? (
          <div className="bg-red-500/10 border border-red-500/20 text-red-300 p-6 rounded-2xl text-center max-w-xl mx-auto my-12">
            <p className="font-semibold text-base mb-2">⚠️ Tilkoblingsfeil</p>
            <p className="text-xs text-red-200/80 mb-4">{error}</p>
            <button
              onClick={loadJobs}
              className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-xl text-xs font-semibold transition-colors"
            >
              Prøv på nytt
            </button>
          </div>
        ) : (
          <JobList
            jobs={jobs}
            onOpenGenerateModal={(job) => setSelectedJob(job)}
            onStatusChange={handleStatusChange}
          />
        )}
      </main>

      {/* Modal for AI Søknad */}
      <ApplicationModal
        job={selectedJob}
        onClose={() => setSelectedJob(null)}
        onApplicationGenerated={handleApplicationGenerated}
      />

      {/* Modal for Brukerprofil & CV */}
      <ProfileModal
        isOpen={isProfileOpen}
        onClose={() => setIsProfileOpen(false)}
      />

      {/* Footer */}
      <footer className="border-t border-slate-800/80 py-6 text-center text-xs text-slate-400">
        FinnJobScout v2.0 • Universell AI Jobb- & Søknadsportal • Python FastAPI & TypeScript React
      </footer>
    </div>
  );
}

export default App;
