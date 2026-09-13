import React from 'react';
import type { QualityAnalysisResult } from '../types/inspection';
import { CheckCircle2, AlertTriangle, ShieldCheck } from 'lucide-react';

interface QualityMeterProps {
  quality: QualityAnalysisResult;
}

export const QualityMeter: React.FC<QualityMeterProps> = ({ quality }) => {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10';
    if (score >= 60) return 'text-amber-400 border-amber-500/30 bg-amber-500/10';
    return 'text-rose-400 border-rose-500/30 bg-rose-500/10';
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-sky-400" />
          <h3 className="text-sm font-semibold text-slate-200 uppercase tracking-wider">Capture Quality</h3>
        </div>
        <div className={`px-3 py-1 rounded-full border text-sm font-bold ${getScoreColor(quality.readiness_score)}`}>
          {quality.readiness_score}% Readiness
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 text-xs">
        {/* Sharpness */}
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80 flex flex-col justify-between">
          <span className="text-slate-400">Sharpness</span>
          <div className="flex items-center gap-1.5 mt-1 font-medium">
            {quality.is_sharp ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            ) : (
              <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
            )}
            <span className={quality.is_sharp ? 'text-emerald-300' : 'text-amber-300'}>
              {quality.sharpness_laplacian} Var
            </span>
          </div>
        </div>

        {/* Lighting */}
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80 flex flex-col justify-between">
          <span className="text-slate-400">Lighting</span>
          <div className="flex items-center gap-1.5 mt-1 font-medium">
            {quality.is_well_lit ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            ) : (
              <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
            )}
            <span className={quality.is_well_lit ? 'text-emerald-300' : 'text-amber-300'}>
              {quality.brightness_mean} Mean
            </span>
          </div>
        </div>

        {/* Glare */}
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80 flex flex-col justify-between">
          <span className="text-slate-400">Low Glare</span>
          <div className="flex items-center gap-1.5 mt-1 font-medium">
            {quality.is_low_glare ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            ) : (
              <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0" />
            )}
            <span className={quality.is_low_glare ? 'text-emerald-300' : 'text-rose-300'}>
              {quality.glare_percent}% Saturated
            </span>
          </div>
        </div>

        {/* Coverage */}
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80 flex flex-col justify-between">
          <span className="text-slate-400">Coverage</span>
          <div className="flex items-center gap-1.5 mt-1 font-medium">
            {quality.is_adequate_size ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            ) : (
              <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
            )}
            <span className={quality.is_adequate_size ? 'text-emerald-300' : 'text-amber-300'}>
              {quality.object_coverage_percent}% Area
            </span>
          </div>
        </div>

        {/* Perspective */}
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80 flex flex-col justify-between col-span-2 sm:col-span-1">
          <span className="text-slate-400">Perspective</span>
          <div className="flex items-center gap-1.5 mt-1 font-medium">
            {quality.is_perpendicular ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            ) : (
              <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
            )}
            <span className={quality.is_perpendicular ? 'text-emerald-300' : 'text-amber-300'}>
              {quality.perspective_angle_deg}° Tilt
            </span>
          </div>
        </div>
      </div>

      {quality.recommendations.length > 0 && (
        <div className="bg-amber-500/10 border border-amber-500/20 rounded-lg p-2.5 text-xs text-amber-300 space-y-1">
          <div className="font-semibold flex items-center gap-1 text-amber-400">
            <AlertTriangle className="w-3.5 h-3.5" /> Recommendations to improve measurement accuracy:
          </div>
          <ul className="list-disc list-inside space-y-0.5 text-amber-200/90 pl-1">
            {quality.recommendations.map((rec, idx) => (
              <li key={idx}>{rec}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
