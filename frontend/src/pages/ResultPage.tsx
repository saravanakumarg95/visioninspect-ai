import React, { useState } from 'react';
import { useLocation, useSearchParams, Link } from 'react-router-dom';
import type { InspectionResponse } from '../types/inspection';
import { MeasurementOverlay } from '../components/MeasurementOverlay';
import { SourceBadge } from '../components/SourceBadge';
import { DefectBadge } from '../components/DefectBadge';
import { MultiViewModal } from '../components/MultiViewModal';
import { 
  Download, CheckCircle2, AlertTriangle, XCircle, 
  ShieldCheck, ArrowLeft, Camera 
} from 'lucide-react';

export const ResultPage: React.FC = () => {
  const location = useLocation();
  const [searchParams] = useSearchParams();
  const [isMultiViewOpen, setIsMultiViewOpen] = useState(false);

  // Use passed inspection state or fallback baseline sample result
  const inspection: InspectionResponse = location.state?.inspection || {
    inspection_id: searchParams.get('id') || 'INS-2026-000124',
    created_at: new Date().toISOString().replace('T', ' ').substring(0, 19),
    mode: 'photo',
    component: {
      detected_class: 'hex_bolt',
      confidence: 0.92,
      detection_method: 'Classical CV fallback'
    },
    quality: {
      sharpness_laplacian: 184.2,
      is_sharp: true,
      brightness_mean: 142.5,
      is_well_lit: true,
      glare_percent: 1.2,
      is_low_glare: true,
      object_coverage_percent: 24.5,
      is_adequate_size: true,
      perspective_angle_deg: 2.1,
      is_perpendicular: true,
      readiness_score: 94.0,
      recommendations: []
    },
    calibration: {
      calibrated: true,
      method: 'aruco',
      reference_size_mm: 50.0,
      detected_size_px: 421.0,
      scale_px_per_mm: 8.42,
      error_percent: 0.42,
      perspective_corrected: true,
      uncertainty_percent: 0.42,
      status: 'valid'
    },
    measurements: [
      {
        name: 'Length',
        value: 49.8,
        unit: 'mm',
        uncertainty: 0.3,
        confidence: 0.92,
        source: 'DIRECT',
        reliability: 'HIGH',
        pass_fail: 'PASS'
      },
      {
        name: 'Outer Diameter',
        value: 10.1,
        unit: 'mm',
        uncertainty: 0.2,
        confidence: 0.91,
        source: 'DIRECT',
        reliability: 'HIGH',
        pass_fail: 'PASS'
      },
      {
        name: 'Thread Pitch (Estimated)',
        value: 1.5,
        unit: 'mm',
        uncertainty: 0.1,
        confidence: 0.75,
        source: 'AI ESTIMATED',
        reliability: 'MEDIUM',
        pass_fail: 'PASS'
      },
      {
        name: 'Thickness / Height',
        value: null,
        unit: 'mm',
        uncertainty: 0.0,
        confidence: 0.0,
        source: 'INSUFFICIENT DATA',
        reliability: 'INSUFFICIENT',
        pass_fail: 'UNVERIFIED',
        details: { reason: 'Requires side view capture' }
      }
    ],
    defects: [],
    fastener: {
      matched: true,
      standard: 'ISO 4014 / DIN 931',
      designation: 'M10 x 1.5',
      type: 'hex_bolt',
      nominal_diameter_mm: 10.0,
      pitch_mm: 1.5,
      confidence: 0.92,
      match_source: 'DATABASE MATCH'
    },
    uncertainty: {
      calibration_uncertainty_percent: 0.42,
      perspective_uncertainty_percent: 0.20,
      edge_detection_uncertainty_percent: 0.30,
      video_temporal_variance_percent: 0.0,
      combined_uncertainty_mm: 0.18,
      explanation: 'Combined RSS uncertainty of ±0.18 mm (0.55%) derived from Calibration, Perspective, and Edge Quantization.'
    },
    status: 'PASS',
    multiview_required: true,
    multiview_reason: 'Thickness cannot be measured from top-down view. Capture side view.',
    views_captured: 1,
    annotated_image_url: '/sample_data/bolt_aruco.png',
    pdf_report_url: `http://localhost:8000/api/reports/${searchParams.get('id') || 'INS-2026-000124'}.pdf`,
    notes: []
  };

  const getStatusBanner = (status: string) => {
    if (status === 'PASS') {
      return {
        bg: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400',
        badgeBg: 'bg-emerald-600 text-white',
        icon: CheckCircle2,
        title: 'PASS — COMPONENT SATISFIES SPECIFICATIONS'
      };
    }
    if (status === 'FAIL') {
      return {
        bg: 'bg-rose-500/10 border-rose-500/30 text-rose-400',
        badgeBg: 'bg-rose-600 text-white',
        icon: XCircle,
        title: 'FAIL — CRITICAL DEFECT OR OUT-OF-SPEC DIMENSION'
      };
    }
    return {
      bg: 'bg-amber-500/10 border-amber-500/30 text-amber-400',
      badgeBg: 'bg-amber-600 text-white',
      icon: AlertTriangle,
      title: 'REVIEW — LOW CONFIDENCE OR UNCALIBRATED MARGIN'
    };
  };

  const statusConfig = getStatusBanner(inspection.status);
  const StatusIcon = statusConfig.icon;

  const pdfUrl = inspection.pdf_report_url || `http://localhost:8000/api/reports/${inspection.inspection_id}.pdf`;

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Navigation Top Bar */}
      <div className="flex items-center justify-between">
        <Link to="/new" className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-semibold text-slate-300 hover:text-white transition">
          <ArrowLeft className="w-4 h-4" /> Start Another Inspection
        </Link>
        <div className="flex items-center gap-3">
          <a
            href={pdfUrl}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs shadow-lg shadow-sky-600/30 transition"
          >
            <Download className="w-4 h-4" /> Download PDF Report
          </a>
        </div>
      </div>

      {/* Large 3-State Verdict Banner */}
      <div className={`border rounded-2xl p-5 flex items-center justify-between shadow-xl ${statusConfig.bg}`}>
        <div className="flex items-center gap-4">
          <div className={`w-12 h-12 rounded-xl flex items-center justify-center font-black ${statusConfig.badgeBg}`}>
            <StatusIcon className="w-7 h-7" />
          </div>
          <div>
            <div className="text-xs font-bold uppercase tracking-wider opacity-80">Inspection Status</div>
            <h2 className="text-xl font-extrabold tracking-tight">{statusConfig.title}</h2>
            <div className="text-xs opacity-75 mt-0.5">ID: {inspection.inspection_id} • {inspection.created_at}</div>
          </div>
        </div>

        {inspection.multiview_required && (
          <button
            onClick={() => setIsMultiViewOpen(true)}
            className="hidden sm:inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 border border-amber-500/40 text-amber-300 text-xs font-bold transition"
          >
            <Camera className="w-4 h-4" /> Side View Required
          </button>
        )}
      </div>

      {/* Main Two-Column Layout for Metrology Inspection */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Image Canvas Overlay */}
        <div className="lg:col-span-6 space-y-4">
          <MeasurementOverlay inspection={inspection} />

          {/* ArUco Calibration Summary Card */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 space-y-2">
            <div className="flex items-center justify-between text-xs font-bold text-slate-300 uppercase">
              <span className="flex items-center gap-1.5 text-purple-400">
                <ShieldCheck className="w-4 h-4" /> Calibration Reference
              </span>
              <span className="text-emerald-400">CALIBRATED</span>
            </div>
            <div className="grid grid-cols-3 gap-2 text-xs pt-1">
              <div className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                <span className="text-slate-400 text-[10px]">Reference Size</span>
                <div className="font-bold text-slate-200">{inspection.calibration.reference_size_mm} mm</div>
              </div>
              <div className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                <span className="text-slate-400 text-[10px]">Scale Ratio</span>
                <div className="font-bold text-sky-400">{inspection.calibration.scale_px_per_mm.toFixed(2)} px/mm</div>
              </div>
              <div className="bg-slate-950 p-2 rounded-lg border border-slate-800">
                <span className="text-slate-400 text-[10px]">Calibration Error</span>
                <div className="font-bold text-emerald-400">{inspection.calibration.error_percent.toFixed(2)}%</div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Complete Analysis & Measurements */}
        <div className="lg:col-span-6 space-y-6">
          {/* Component Identification Card */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 space-y-2 shadow-lg">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">AI Component Identification</h3>
            <div className="flex items-center justify-between bg-slate-950 p-3 rounded-lg border border-slate-800">
              <div>
                <div className="text-base font-extrabold text-white capitalize">{inspection.component.detected_class.replace('_', ' ')}</div>
                <div className="text-xs text-slate-400">{inspection.component.detection_method}</div>
              </div>
              <div className="text-right">
                <div className="text-lg font-black text-sky-400">{Math.round(inspection.component.confidence * 100)}%</div>
                <div className="text-[10px] text-slate-400">Confidence</div>
              </div>
            </div>
          </div>

          {/* Dimensional Measurements Table */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-3 shadow-lg">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">Dimensional Measurements</h3>
              <span className="text-xs text-slate-400">Uncertainty Bound: ±{inspection.uncertainty.combined_uncertainty_mm} mm</span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-950 text-slate-400 font-semibold">
                  <tr>
                    <th className="p-2.5 rounded-l-lg">Feature</th>
                    <th className="p-2.5">Value</th>
                    <th className="p-2.5">Uncertainty</th>
                    <th className="p-2.5">Source</th>
                    <th className="p-2.5 rounded-r-lg">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/80">
                  {inspection.measurements.map((m, idx) => (
                    <tr key={idx} className="hover:bg-slate-800/40">
                      <td className="p-2.5 font-bold text-slate-200">{m.name}</td>
                      <td className="p-2.5 font-mono text-slate-100 font-bold">
                        {m.value !== null ? `${m.value.toFixed(2)} ${m.unit}` : <span className="text-amber-400 font-normal">INSUFFICIENT DATA</span>}
                      </td>
                      <td className="p-2.5 text-slate-400 font-mono">
                        {m.value !== null ? `±${m.uncertainty.toFixed(2)} ${m.unit}` : '-'}
                      </td>
                      <td className="p-2.5">
                        <SourceBadge source={m.source} />
                      </td>
                      <td className="p-2.5">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          m.pass_fail === 'PASS' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'
                        }`}>
                          {m.pass_fail}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Fastener Database Candidate Match */}
          {inspection.fastener && (
            <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 space-y-2 shadow-lg">
              <h3 className="text-xs font-bold text-purple-400 uppercase tracking-wider">ISO Metric Fastener Candidate Match</h3>
              <div className="bg-purple-950/30 border border-purple-800/50 rounded-lg p-3 flex items-center justify-between">
                <div>
                  <div className="text-sm font-extrabold text-purple-200">{inspection.fastener.designation} ({inspection.fastener.standard})</div>
                  <div className="text-xs text-purple-300/80">Nominal Diam: {inspection.fastener.nominal_diameter_mm} mm • Pitch: {inspection.fastener.pitch_mm} mm</div>
                </div>
                <div className="px-2.5 py-1 rounded bg-purple-500/20 text-purple-300 text-xs font-bold">
                  {Math.round(inspection.fastener.confidence * 100)}% Match
                </div>
              </div>
            </div>
          )}

          {/* Defect Inspection Results */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 space-y-3 shadow-lg">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Visual Defect Analysis</h3>
            {inspection.defects.length === 0 ? (
              <div className="text-xs text-emerald-400 flex items-center gap-2 bg-emerald-500/10 p-3 rounded-lg border border-emerald-500/20">
                <CheckCircle2 className="w-4 h-4" /> No visual surface or edge defects detected.
              </div>
            ) : (
              <div className="space-y-2">
                {inspection.defects.map((d, i) => (
                  <div key={i} className="bg-rose-950/20 border border-rose-800/40 p-3 rounded-lg flex items-center justify-between text-xs">
                    <div>
                      <div className="font-bold text-rose-300 capitalize">{d.defect_type.replace('_', ' ')}</div>
                      <div className="text-slate-400 text-[11px]">{d.description}</div>
                    </div>
                    <DefectBadge severity={d.severity} />
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Multi-View Side View Capture Dialog */}
      <MultiViewModal
        isOpen={isMultiViewOpen}
        reason={inspection.multiview_reason}
        onClose={() => setIsMultiViewOpen(false)}
        onCaptureSideView={() => alert("Ready to capture side profile View 2!")}
      />
    </div>
  );
};
