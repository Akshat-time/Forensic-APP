
import React, { useState, useCallback } from 'react';
import { AudioFeatures, Classification, ExplanationResult } from './types';
import FeatureControl from './components/FeatureControl';
import ForensicChart from './components/ForensicChart';
import { generateForensicJustification } from './services/geminiService';

const App: React.FC = () => {
  const [features, setFeatures] = useState<AudioFeatures>({
    pauseEntropy: 1.25,
    pitchJitter: 0.84,
    shimmer: 1.12,
    silenceNoiseVariance: 0.0045,
    prosodyDrift: 2.1,
    language: 'English',
  });

  const [classification, setClassification] = useState<Classification>(Classification.AUTHENTIC);
  const [result, setResult] = useState<ExplanationResult>({ text: '', loading: false });

  const updateFeature = useCallback((key: keyof AudioFeatures, val: any) => {
    setFeatures(prev => ({ ...prev, [key]: val }));
  }, []);

  const handleGenerate = async () => {
    setResult({ text: '', loading: true });
    try {
      const justification = await generateForensicJustification(features, classification);
      setResult({ text: justification, loading: false });
    } catch (err: any) {
      setResult({ text: '', loading: false, error: err.message });
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 md:py-12">
      <header className="mb-10 text-center">
        <h1 className="text-3xl md:text-4xl font-bold text-slate-50 mb-2 flex items-center justify-center gap-3">
          <svg className="w-10 h-10 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
          </svg>
          Forensics Explanation Assistant
        </h1>
        <p className="text-slate-400 max-w-2xl mx-auto">
          Convert numerical forensic features into technical justifications for audio analysis reports.
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-4 space-y-4">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-1 h-6 bg-emerald-500 rounded-full"></div>
            <h2 className="text-lg font-semibold uppercase tracking-widest text-slate-300">Analysis Inputs</h2>
          </div>

          <div className="flex flex-col gap-2 p-3 bg-slate-900 rounded-lg border border-slate-800">
            <label className="text-xs font-semibold uppercase tracking-wider text-slate-400">Language Context</label>
            <select
              value={features.language}
              onChange={(e) => updateFeature('language', e.target.value)}
              className="bg-slate-800 border-none text-slate-100 text-sm rounded-md p-2 focus:ring-1 focus:ring-emerald-500 outline-none"
            >
              <option>English</option>
              <option>Hindi</option>
              <option>Telugu</option>
              <option>Tamil</option>
              <option>Malayalam</option>
            </select>
          </div>

          <FeatureControl
            label="Pause Entropy"
            value={features.pauseEntropy}
            min={0} max={5} step={0.01}
            onChange={(v) => updateFeature('pauseEntropy', v)}
          />
          <FeatureControl
            label="Pitch Jitter"
            value={features.pitchJitter}
            min={0} max={5} step={0.01} unit="%"
            onChange={(v) => updateFeature('pitchJitter', v)}
          />
          <FeatureControl
            label="Amplitude Shimmer"
            value={features.shimmer}
            min={0} max={5} step={0.01} unit="%"
            onChange={(v) => updateFeature('shimmer', v)}
          />
          <FeatureControl
            label="Silence Noise Variance"
            value={features.silenceNoiseVariance}
            min={0} max={1} step={0.0001}
            onChange={(v) => updateFeature('silenceNoiseVariance', v)}
          />
          <FeatureControl
            label="Prosody Drift Score"
            value={features.prosodyDrift}
            min={0} max={10} step={0.1}
            onChange={(v) => updateFeature('prosodyDrift', v)}
          />
        </div>

        <div className="lg:col-span-8 space-y-8">
          <section className="bg-slate-900 rounded-2xl p-6 border border-slate-800 shadow-xl">
            <div className="flex items-center gap-2 mb-6">
              <div className="w-1 h-6 bg-emerald-500 rounded-full"></div>
              <h2 className="text-lg font-semibold uppercase tracking-widest text-slate-300">Forensic Verdict</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {Object.values(Classification).map((type) => (
                <button
                  key={type}
                  onClick={() => setClassification(type)}
                  className={`px-4 py-3 rounded-xl border transition-all duration-200 text-sm font-medium ${classification === type
                    ? 'bg-emerald-500/10 border-emerald-500 text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.1)]'
                    : 'bg-slate-800/50 border-slate-700 text-slate-400 hover:bg-slate-800 hover:border-slate-600'
                    }`}
                >
                  {type}
                </button>
              ))}
            </div>
          </section>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
            <ForensicChart features={features} />

            <div className="space-y-6">
              <button
                onClick={handleGenerate}
                disabled={result.loading}
                className="w-full py-4 bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-800 disabled:text-slate-500 text-white font-bold rounded-xl transition-all shadow-lg shadow-emerald-900/20 active:scale-[0.98] flex items-center justify-center gap-2"
              >
                {result.loading ? (
                  <>
                    <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Analyzing Summary...
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    Generate Technical Justification
                  </>
                )}
              </button>

              <div className="bg-slate-900 rounded-xl p-6 border border-slate-800 min-h-[160px] flex flex-col justify-center relative overflow-hidden">
                <div className="absolute top-0 right-0 p-3">
                  <span className="text-[10px] text-slate-600 font-mono tracking-tighter">AF_EXP_v2.0</span>
                </div>

                {result.error && (
                  <div className="text-red-400 text-sm bg-red-400/10 p-3 rounded border border-red-500/20">
                    {result.error}
                  </div>
                )}

                {result.text ? (
                  <div className="animate-in fade-in slide-in-from-bottom-2 duration-500">
                    <p className="text-emerald-50 leading-relaxed font-medium italic border-l-2 border-emerald-500 pl-4">
                      "{result.text}"
                    </p>
                  </div>
                ) : !result.loading && (
                  <p className="text-slate-600 text-sm text-center italic">
                    Set parameters and click generate...
                  </p>
                )}

                {result.loading && (
                  <div className="flex flex-col items-center gap-3">
                    <div className="h-2 w-32 bg-slate-800 rounded-full overflow-hidden">
                      <div className="h-full bg-emerald-500 animate-[loading_1.5s_infinite_linear]"></div>
                    </div>
                    <span className="text-xs text-slate-500 font-mono">EXTRACTING_LOGIC_PATH</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      <footer className="mt-16 pt-8 border-t border-slate-900 text-center text-slate-500 text-xs">
        <p>© Audio Forensic Analytical Division - Automated Explanation Service</p>
        <p className="mt-1 opacity-50 uppercase tracking-widest font-mono">Secure Node: AD-102-SYS</p>
      </footer>

      <style>{`
        @keyframes loading {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
      `}</style>
    </div>
  );
};

export default App;
