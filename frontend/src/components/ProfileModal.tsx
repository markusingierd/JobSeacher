import React, { useState, useEffect } from 'react';
import { X, Save, User, Briefcase, Sparkles, FileText, Check, Plus, Trash2 } from 'lucide-react';
import { UserProfile } from '../types/job';
import { fetchProfile, saveProfile } from '../api/client';

interface ProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
  onProfileUpdated?: () => void;
}

export const ProfileModal: React.FC<ProfileModalProps> = ({
  isOpen,
  onClose,
  onProfileUpdated,
}) => {
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [profile, setProfile] = useState<UserProfile>({
    full_name: '',
    age: 23,
    current_title: '',
    target_category: 'IT & Utvikling',
    tone_of_voice: 'Ung & direkte (23 år), uformell, korte setninger, null konsulentspråk',
    personality_traits: [],
    cv_experiences: '',
    custom_search_keywords: [],
    location_filter: 'Oslo og omegn',
  });
  const [newTrait, setNewTrait] = useState('');

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      fetchProfile()
        .then((data) => setProfile(data))
        .catch((err) => console.error('Feil ved lesing av profil:', err))
        .finally(() => setLoading(false));
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSave = async () => {
    setSaving(true);
    try {
      await saveProfile(profile);
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 2500);
      if (onProfileUpdated) onProfileUpdated();
    } catch (err: any) {
      alert(`Feil ved lagring: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  const handleAddTrait = () => {
    if (newTrait.trim() !== '') {
      setProfile({
        ...profile,
        personality_traits: [...profile.personality_traits, newTrait.trim()],
      });
      setNewTrait('');
    }
  };

  const handleRemoveTrait = (index: number) => {
    setProfile({
      ...profile,
      personality_traits: profile.personality_traits.filter((_, i) => i !== index),
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-3xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/90">
          <div className="flex items-center gap-2.5">
            <div className="p-2 bg-blue-500/10 text-blue-400 rounded-xl">
              <User size={20} />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-100">⚙️ Profil, CV & AI-Innstillinger</h2>
              <p className="text-xs text-slate-400">
                Styr hva AI-modellen vet om deg, din CV, personlighetstrekk og din foretrukne tone.
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-white bg-slate-800/60 hover:bg-slate-800 rounded-xl transition-colors"
          >
            <X size={18} />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 overflow-y-auto space-y-5 flex-1">
          {loading ? (
            <div className="py-12 text-center text-xs text-slate-400">Laster inn profil data...</div>
          ) : (
            <>
              {/* Grunnleggende Personalia */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Fullt Navn</label>
                  <input
                    type="text"
                    value={profile.full_name}
                    onChange={(e) => setProfile({ ...profile, full_name: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Alder (År)</label>
                  <input
                    type="number"
                    value={profile.age}
                    onChange={(e) => setProfile({ ...profile, age: Number(e.target.value) })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Hovedtittel / Yrke</label>
                  <input
                    type="text"
                    value={profile.current_title}
                    onChange={(e) => setProfile({ ...profile, current_title: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-blue-500"
                  />
                </div>
              </div>

              {/* Målkategori & Tone */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Målkategori / Bransje</label>
                  <select
                    value={profile.target_category}
                    onChange={(e) => setProfile({ ...profile, target_category: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-blue-500"
                  >
                    <option value="IT & Utvikling">💻 IT & Utvikling</option>
                    <option value="Helse, Pleie & Omsorg">🏥 Helse, Pleie & Omsorg</option>
                    <option value="Økonomi & Finans">💼 Økonomi & Finans</option>
                    <option value="Salg, Markedsføring & PR">📣 Salg & Markedsføring</option>
                    <option value="Ingeniør & Tekniske Fag">⚙️ Ingeniør & Tekniske Fag</option>
                    <option value="Generelt / Alle Yrker">🌍 Generelt / Alle Yrker</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Ønsket Tone of Voice</label>
                  <input
                    type="text"
                    value={profile.tone_of_voice}
                    onChange={(e) => setProfile({ ...profile, tone_of_voice: e.target.value })}
                    placeholder="F.eks. Ung & direkte, uformell, korte setninger..."
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-blue-500"
                  />
                </div>
              </div>

              {/* Personlighetstrekk & Styrker */}
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Personlighetstrekk & Styrker (som AI-en fletter inn):
                </label>
                <div className="flex flex-wrap gap-2 mb-2">
                  {profile.personality_traits.map((trait, index) => (
                    <span
                      key={index}
                      className="bg-blue-950/60 border border-blue-800/60 text-blue-300 px-2.5 py-1 rounded-lg text-xs flex items-center gap-1.5"
                    >
                      {trait}
                      <button
                        onClick={() => handleRemoveTrait(index)}
                        className="hover:text-red-400 transition-colors"
                      >
                        <X size={12} />
                      </button>
                    </span>
                  ))}
                </div>
                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="Legg til nytt trekk (f.eks. 'Samlende lagspiller', 'Strukturert')..."
                    value={newTrait}
                    onChange={(e) => setNewTrait(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleAddTrait()}
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3 py-1.5 text-xs text-slate-100 focus:outline-none focus:border-blue-500"
                  />
                  <button
                    onClick={handleAddTrait}
                    className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold flex items-center gap-1 border border-slate-700"
                  >
                    <Plus size={14} /> Legg til
                  </button>
                </div>
              </div>

              {/* CV & Erfaringer Textarea */}
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5 flex items-center justify-between">
                  <span className="flex items-center gap-1">
                    <FileText size={14} className="text-blue-400" />
                    CV, Utdanning & Hovederfaringer (Markdown / Tekst):
                  </span>
                  <span className="text-[11px] text-slate-400">AI-modellen leser dette når den skreddersyr</span>
                </label>
                <textarea
                  value={profile.cv_experiences}
                  onChange={(e) => setProfile({ ...profile, cv_experiences: e.target.value })}
                  rows={8}
                  placeholder="Lim inn din CV eller skriv inn dine viktigste prosjekter og erfaringer her..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3.5 font-mono text-xs text-slate-200 focus:outline-none focus:border-blue-500 leading-relaxed"
                />
              </div>
            </>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-slate-800 bg-slate-900/90 flex items-center justify-between">
          <span className="text-xs text-slate-400">
            {savedSuccess ? '✅ Profil lagret!' : 'Endringer blir lagret i user_settings.json'}
          </span>
          <div className="flex items-center gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-medium border border-slate-700"
            >
              Lukk
            </button>
            <button
              onClick={handleSave}
              disabled={saving}
              className="flex items-center gap-1.5 px-5 py-2 bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-500 hover:to-emerald-500 text-white rounded-xl text-xs font-semibold shadow-md shadow-blue-500/20"
            >
              {saving ? <Sparkles size={14} className="animate-spin" /> : savedSuccess ? <Check size={14} /> : <Save size={14} />}
              <span>{saving ? 'Lagrer...' : savedSuccess ? 'Lagret!' : 'Lagre Profil & CV'}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
