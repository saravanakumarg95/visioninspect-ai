import React from 'react';
import { Link } from 'react-router-dom';
import { PlusCircle, Scan, ShieldCheck, ArrowRight } from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const recentInspections = [
    {
      id: 'INS-2026-000124',
      name: 'M10 Hex Bolt',
      partNumber: 'DIN-931-M10',
      status: 'PASS',
      date: 'Today, 14:20',
      confidence: 92,
      scale: '8.42 px/mm'
    },
    {
      id: 'INS-2026-000123',
      name: 'M10 Form A Washer',
      partNumber: 'ISO-7089-M10',
      status: 'PASS',
      date: 'Yesterday',
      confidence: 94,
      scale: '8.38 px/mm'
    },
    {
      id: 'INS-2026-000122',
      name: '4-Hole Mounting Plate',
      partNumber: 'PLT-8050-04',
      status: 'REVIEW',
      date: 'Yesterday',
      confidence: 88,
      scale: '8.40 px/mm'
    }
  ];

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Hero Banner */}
      <div className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-slate-900 to-sky-950/60 border border-slate-800 rounded-3xl p-6 sm:p-10 shadow-2xl">
        <div className="absolute top-0 right-0 -mt-10 -mr-10 w-80 h-80 bg-sky-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="max-w-2xl space-y-4 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-500/20 text-sky-400 text-xs font-semibold">
            <ShieldCheck className="w-4 h-4" /> AI-Powered Metrology & Mechanical Vision Inspection
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
            Precision Component Inspection using your Smartphone Camera
          </h1>
          <p className="text-sm sm:text-base text-slate-300">
            ArUco reference calibration, real sub-pixel dimensional measurement, visual defect detection, ISO metric standards matching, and PDF metrology report generation.
          </p>
          <div className="pt-2 flex flex-wrap gap-4">
            <Link
              to="/new"
              className="inline-flex items-center gap-2.5 px-6 py-3.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-sm shadow-xl shadow-sky-600/30 transition transform active:scale-95"
            >
              <PlusCircle className="w-5 h-5" /> Start New Inspection
            </Link>
            <Link
              to="/standards"
              className="inline-flex items-center gap-2 px-5 py-3.5 rounded-xl bg-slate-800/80 hover:bg-slate-800 text-slate-200 font-semibold text-sm border border-slate-700 transition"
            >
              Browse ISO Standards
            </Link>
          </div>
        </div>
      </div>

      {/* Overview Metrology Stats Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 space-y-1">
          <span className="text-xs text-slate-400 font-medium">Total Inspections</span>
          <div className="text-2xl font-black text-slate-100">124</div>
          <span className="text-[10px] text-emerald-400">↑ 12 this week</span>
        </div>
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 space-y-1">
          <span className="text-xs text-slate-400 font-medium">Pass Rate</span>
          <div className="text-2xl font-black text-emerald-400">94.2%</div>
          <span className="text-[10px] text-slate-400">117 Passed</span>
        </div>
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 space-y-1">
          <span className="text-xs text-slate-400 font-medium">Mean Calibration Error</span>
          <div className="text-2xl font-black text-sky-400">0.42%</div>
          <span className="text-[10px] text-sky-300">ArUco 50mm Ref</span>
        </div>
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 space-y-1">
          <span className="text-xs text-slate-400 font-medium">Reports Generated</span>
          <div className="text-2xl font-black text-purple-400">98</div>
          <span className="text-[10px] text-purple-300">PDF PDF/A Metrology</span>
        </div>
      </div>

      {/* Recent Inspections Table */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <h2 className="text-lg font-bold text-slate-100">Recent Component Inspections</h2>
            <p className="text-xs text-slate-400">Real-time computer vision analysis results</p>
          </div>
          <Link to="/history" className="text-xs font-semibold text-sky-400 hover:text-sky-300 flex items-center gap-1">
            View All <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="divide-y divide-slate-800/80">
          {recentInspections.map((item) => (
            <div key={item.id} className="py-3.5 flex items-center justify-between gap-4 hover:bg-slate-800/30 px-2 rounded-xl transition">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-slate-800 flex items-center justify-center text-slate-300 border border-slate-700">
                  <Scan className="w-5 h-5 text-sky-400" />
                </div>
                <div>
                  <div className="font-bold text-sm text-slate-100">{item.name}</div>
                  <div className="text-xs text-slate-400 flex items-center gap-2">
                    <span>{item.id}</span> • <span>{item.partNumber}</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="hidden sm:block text-right text-xs">
                  <div className="text-slate-300 font-medium">{item.scale}</div>
                  <div className="text-slate-400 text-[10px]">{item.date}</div>
                </div>
                <div className={`px-3 py-1 rounded-full text-xs font-bold ${
                  item.status === 'PASS'
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                    : 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                }`}>
                  {item.status}
                </div>
                <Link to={`/result?id=${item.id}`} className="p-2 text-slate-400 hover:text-sky-400">
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
