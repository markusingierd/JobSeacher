import React, { useState, useEffect } from 'react';
import { X, Sparkles, Download, Copy, Check, FileText, AlertCircle } from 'lucide-react';
import { Job, ApplicationResponse } from '../types/job';
import { generateApplication, exportDocx } from '../api/client';

interface ApplicationModalProps {
  job: Job | null;
  onClose: () => void;
  onApplicationGenerated: (jobId: string) => void;
}

export const ApplicationModal: React.FC<ApplicationModalProps> = ({
  job,
  onClose,
  onApplicationGenerated,
}) => {
  const [loading, setLoading] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [copied, setCopied] = useState(false);
  const [customNotes, setCustomNotes] = useState('');
  const [contentMarkdown, setContentMarkdown] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    if (job) {
      setContentMarkdown('');
      setError('');
      setCustomNotes('');
    }
  }, [job]);

  if (!job) return null;

  const handleGenerate = async () => {
    setLoading(true);
    setError('');
    try {
      const res: ApplicationResponse = await generateApplication({
        job_id: job.id,
        custom_notes: customNotes,
      });
      setContentMarkdown(res.cover_letter_markdown);
      onApplicationGenerated(job.id);
    } catch (err: any) {
      setError(err.message || 'Kunne ikke generere søknad');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(contentMarkdown);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleExportDocx = async () => {
    setExporting(true);
    try {
      const blob = await exportDocx({
        job_id: job.id,
        company: job.company,
        job_title: job.title,
        content_markdown: contentMarkdown,
      });

      // Trigg automatisk fildownload i nettleseren
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const cleanCompany = job.company.replace(/[^a-zA-Z0-9]/g, '_');
      a.download = `Soknad_${cleanCompany}_Markus.docx`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      alert(`Feil ved nedlasting av Word-fil: ${err.message}`);
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/90">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">✨</span>
              <h2 className="text-lg font-bold text-slate-100">AI Søknadsgenerator</h2>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              {job.title} hos <strong className="text-slate-200">{job.company}</strong>
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-white bg-slate-800/60 hover:bg-slate-800 rounded-xl transition-colors"
          >
            <X size={18} />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-5 flex-1">
          {error && (
            <div className="bg-red-500/10 border border-red-500/20 text-red-300 p-3 rounded-xl text-xs flex items-center gap-2">
              <AlertCircle size={16} />
              <span>{error}</span>
            </div>
          )}

          {/* Vipps Krok Innsikt */}
          {job.company_hook_insight && (
            <div className="bg-blue-950/40 border border-blue-900/40 rounded-xl p-3.5 text-xs text-blue-200">
              <strong className="text-blue-400 block font-semibold mb-1">💡 FINN-Analyse Krok:</strong>
              {job.company_hook_insight}
            </div>
          )}

          {/* Valgfritt tilleggsnotat */}
          {!contentMarkdown && (
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                Spesielle ønsker eller relevante detaljer til AI-en (valgfritt):
              </label>
              <input
                type="text"
                placeholder="F.eks. 'Fremhev min Kotlin-erfaring ekstra' eller 'Nevn min bilinteresse'..."
                value={customNotes}
                onChange={(e) => setCustomNotes(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500"
              />
            </div>
          )}

          {/* Generer-knapp (om ikke generert ennå) */}
          {!contentMarkdown && (
            <div className="pt-2">
              <button
                onClick={handleGenerate}
                disabled={loading}
                className="w-full flex items-center justify-center gap-2 py-3 px-4 bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-500 hover:to-emerald-500 text-white font-semibold text-sm rounded-xl transition-all shadow-lg shadow-blue-500/15"
              >
                <Sparkles size={16} className={loading ? 'animate-spin' : 'text-yellow-300'} />
                <span>{loading ? 'Genererer skreddersydd Vipps-søknad...' : 'Generer AI-Søknad Nå'}</span>
              </button>
            </div>
          )}

          {/* Redigerbar Markdown Textarea etter generering */}
          {contentMarkdown && (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                  <FileText size={14} className="text-blue-400" />
                  Rediger søknadsutkast (Vipps 4-paragrafs formel):
                </span>
                <span className="text-[11px] text-emerald-400 font-medium">✓ Klar til bruk eller tilpasning</span>
              </div>

              <textarea
                value={contentMarkdown}
                onChange={(e) => setContentMarkdown(e.target.value)}
                rows={14}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-4 font-mono text-xs text-slate-200 focus:outline-none focus:border-blue-500 leading-relaxed"
              />
            </div>
          )}
        </div>

        {/* Modal Footer (Eksportknapper) */}
        {contentMarkdown && (
          <div className="px-6 py-4 border-t border-slate-800 bg-slate-900/90 flex flex-col sm:flex-row items-center justify-between gap-3">
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="text-xs text-slate-400 hover:text-slate-200 underline font-medium"
            >
              {loading ? 'Genererer ny...' : '🔄 Generer på nytt med AI'}
            </button>

            <div className="flex items-center gap-2 w-full sm:w-auto">
              <button
                onClick={handleCopy}
                className="flex-1 sm:flex-initial flex items-center justify-center gap-1.5 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold transition-colors border border-slate-700"
              >
                {copied ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} />}
                <span>{copied ? 'Kopiert!' : 'Kopier Tekst'}</span>
              </button>

              <button
                onClick={handleExportDocx}
                disabled={exporting}
                className="flex-1 sm:flex-initial flex items-center justify-center gap-1.5 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-semibold transition-all shadow-md shadow-emerald-600/20"
              >
                <Download size={14} />
                <span>{exporting ? 'Lager Word-fil...' : 'Last ned Word (.docx)'}</span>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
