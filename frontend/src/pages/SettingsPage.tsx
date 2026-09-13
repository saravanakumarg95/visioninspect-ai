import React, { useState } from 'react';
import { Settings, Save, ShieldCheck } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const [arucoSize, setArucoSize] = useState('50.0');
  const [unit, setUnit] = useState('mm');
  const [confidenceThreshold, setConfidenceThreshold] = useState('0.75');
  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
          <Settings className="w-6 h-6 text-sky-400" /> Metrology Configuration & Settings
        </h1>
        <p className="text-xs text-slate-400">Configure default calibration reference, units, and AI thresholds</p>
      </div>

      <form onSubmit={handleSave} className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-6 shadow-xl">
        <div className="space-y-4">
          <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Calibration Defaults</h3>
          
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Default ArUco Marker Size (mm)</label>
            <input
              type="number"
              step="0.1"
              value={arucoSize}
              onChange={(e) => setArucoSize(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-sky-500"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Measurement Unit</label>
            <select
              value={unit}
              onChange={(e) => setUnit(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-sky-500"
            >
              <option value="mm">Millimeters (mm)</option>
              <option value="in">Inches (in)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">AI Detection Confidence Threshold</label>
            <input
              type="number"
              step="0.05"
              min="0.5"
              max="0.95"
              value={confidenceThreshold}
              onChange={(e) => setConfidenceThreshold(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-sky-500"
            />
          </div>
        </div>

        {saved && (
          <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-xs text-emerald-400 font-semibold flex items-center gap-2">
            <ShieldCheck className="w-4 h-4" /> Settings updated successfully!
          </div>
        )}

        <button
          type="submit"
          className="w-full py-3.5 px-6 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-sm shadow-lg shadow-sky-600/30 transition flex items-center justify-center gap-2"
        >
          <Save className="w-4 h-4" /> Save Configuration
        </button>
      </form>
    </div>
  );
};
