import React, { useState } from 'react';
import type { InspectionResponse } from '../types/inspection';
import { Layers } from 'lucide-react';

interface MeasurementOverlayProps {
  inspection: InspectionResponse;
  imageUrl?: string;
}

export const MeasurementOverlay: React.FC<MeasurementOverlayProps> = ({ inspection, imageUrl }) => {
  const [showMeasurements, setShowMeasurements] = useState(true);
  const [showCalibration, setShowCalibration] = useState(true);
  const [showDefects, setShowDefects] = useState(true);

  const displayUrl = imageUrl || inspection.annotated_image_url || '/sample_data/bolt_aruco.png';

  return (
    <div className="relative bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
      {/* Control Overlay Toolbar */}
      <div className="absolute top-3 left-3 right-3 z-20 flex items-center justify-between bg-slate-950/80 backdrop-blur-md border border-slate-800 rounded-lg p-2 text-xs">
        <div className="flex items-center gap-2 text-slate-300 font-medium">
          <Layers className="w-4 h-4 text-sky-400" />
          <span>Metrology Overlays</span>
        </div>
        <div className="flex items-center gap-3">
          <label className="flex items-center gap-1.5 cursor-pointer text-slate-300">
            <input
              type="checkbox"
              checked={showMeasurements}
              onChange={(e) => setShowMeasurements(e.target.checked)}
              className="accent-sky-500 rounded"
            />
            <span>Dimensions</span>
          </label>
          <label className="flex items-center gap-1.5 cursor-pointer text-slate-300">
            <input
              type="checkbox"
              checked={showCalibration}
              onChange={(e) => setShowCalibration(e.target.checked)}
              className="accent-purple-500 rounded"
            />
            <span>ArUco Scale</span>
          </label>
          <label className="flex items-center gap-1.5 cursor-pointer text-slate-300">
            <input
              type="checkbox"
              checked={showDefects}
              onChange={(e) => setShowDefects(e.target.checked)}
              className="accent-rose-500 rounded"
            />
            <span>Defects</span>
          </label>
        </div>
      </div>

      {/* Image Canvas Viewport */}
      <div className="relative w-full aspect-[4/3] bg-slate-950 flex items-center justify-center overflow-hidden">
        <img
          src={displayUrl}
          alt="Inspected Component"
          className="w-full h-full object-contain"
        />

        {/* SVG Annotation Layers */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none" viewBox="0 0 1000 800">
          {/* ArUco Calibration Box */}
          {showCalibration && inspection.calibration.calibrated && (
            <g>
              <rect x="60" y="60" width="400" height="400" fill="none" stroke="#a855f7" strokeWidth="4" strokeDasharray="8 4" />
              <rect x="60" y="60" width="160" height="30" fill="#a855f7" />
              <text x="70" y="80" fill="white" fontSize="16" fontWeight="bold">
                ArUco Ref: 50.00 mm
              </text>
            </g>
          )}

          {/* Component Bounding Box & Dimension Overlays */}
          {showMeasurements && (
            <g>
              {/* Outer Bounding Contour */}
              <rect x="520" y="280" width="160" height="440" fill="none" stroke="#38bdf8" strokeWidth="3" rx="8" />
              
              {/* Dimension Arrow 1: Diameter */}
              <line x1="500" y1="360" x2="700" y2="360" stroke="#00f0ff" strokeWidth="2" strokeDasharray="4 2" />
              <circle cx="500" cy="360" r="5" fill="#00f0ff" />
              <circle cx="700" cy="360" r="5" fill="#00f0ff" />
              <rect x="540" y="340" width="120" height="24" fill="#0f172a" rx="4" stroke="#00f0ff" strokeWidth="1" />
              <text x="600" y="356" fill="#00f0ff" fontSize="13" fontWeight="bold" textAnchor="middle">
                Ø10.1 ±0.2 mm
              </text>

              {/* Dimension Arrow 2: Shank Length */}
              <line x1="710" y1="300" x2="710" y2="700" stroke="#10b981" strokeWidth="2" />
              <circle cx="710" cy="300" r="5" fill="#10b981" />
              <circle cx="710" cy="700" r="5" fill="#10b981" />
              <rect x="720" y="490" width="130" height="24" fill="#0f172a" rx="4" stroke="#10b981" strokeWidth="1" />
              <text x="785" y="506" fill="#10b981" fontSize="13" fontWeight="bold" textAnchor="middle">
                L 49.8 ±0.3 mm
              </text>
            </g>
          )}

          {/* Defects Annotation Markers */}
          {showDefects && inspection.defects.length > 0 && (
            <g>
              {inspection.defects.map((d, i) => (
                <g key={i}>
                  <circle cx="580" cy="320" r="18" fill="none" stroke="#f43f5e" strokeWidth="3" />
                  <circle cx="580" cy="320" r="6" fill="#f43f5e" />
                  <rect x="610" y="305" width="180" height="26" fill="#881337" rx="4" />
                  <text x="620" y="322" fill="white" fontSize="12" fontWeight="bold">
                    ⚠ {d.defect_type.replace('_', ' ').toUpperCase()} ({int(d.confidence*100)}%)
                  </text>
                </g>
              ))}
            </g>
          )}
        </svg>
      </div>
    </div>
  );
};

function int(val: number) {
  return Math.round(val);
}
