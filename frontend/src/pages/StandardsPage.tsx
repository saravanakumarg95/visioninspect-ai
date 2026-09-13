import React, { useState, useEffect } from 'react';
import { searchStandards } from '../api/client';
import { BookOpen, Search } from 'lucide-react';

export const StandardsPage: React.FC = () => {
  const [query, setQuery] = useState('');
  const [standards, setStandards] = useState<any[]>([]);

  useEffect(() => {
    searchStandards(query).then((data) => {
      setStandards(data.items || []);
    });
  }, [query]);

  return (
    <div className="space-y-6 animate-fade-in max-w-5xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-sky-400" /> ISO Metric Engineering Standards
          </h1>
          <p className="text-xs text-slate-400">Extensible mechanical fastener database (ISO 4014, DIN 931, ISO 7089)</p>
        </div>

        <div className="relative min-w-[240px]">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search e.g. M10, Washer, ISO 4014..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-4 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {standards.map((item, idx) => (
          <div key={idx} className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-3 shadow-lg hover:border-slate-700 transition">
            <div className="flex items-center justify-between">
              <div>
                <span className="text-[10px] font-bold text-purple-400 uppercase tracking-wider">{item.standard}</span>
                <h3 className="text-base font-extrabold text-white">{item.designation}</h3>
              </div>
              <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-300 text-xs font-semibold uppercase">
                {item.type.replace('_', ' ')}
              </span>
            </div>

            <div className="grid grid-cols-3 gap-2 text-xs pt-1">
              <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
                <span className="text-slate-400 text-[10px]">Nominal Diam</span>
                <div className="font-bold text-slate-200">{item.nominal_diameter_mm || item.outer_diameter_mm} mm</div>
              </div>
              <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
                <span className="text-slate-400 text-[10px]">Thread Pitch</span>
                <div className="font-bold text-sky-400">{item.pitch_mm ? `${item.pitch_mm} mm` : '-'}</div>
              </div>
              <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
                <span className="text-slate-400 text-[10px]">Head Across Flats</span>
                <div className="font-bold text-emerald-400">{item.head_width_af_mm ? `${item.head_width_af_mm} mm` : '-'}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
