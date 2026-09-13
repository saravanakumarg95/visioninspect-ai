import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera, ShieldCheck, ArrowRight } from 'lucide-react';

export const NewInspectionPage: React.FC = () => {
  const navigate = useNavigate();

  const generatedId = `INS-2026-${Math.floor(100000 + Math.random() * 900000)}`;

  const [componentName, setComponentName] = useState('');
  const [partNumber, setPartNumber] = useState('');
  const [operatorName, setOperatorName] = useState('');
  const [referenceSizeMm, setReferenceSizeMm] = useState('50.0');
  const [calibrationMethod, setCalibrationMethod] = useState('aruco');

  const handleStart = (e: React.FormEvent) => {
    e.preventDefault();
    const params = new URLSearchParams({
      id: generatedId,
      name: componentName || 'Mechanical Component',
      part: partNumber || 'PART-GENERIC',
      operator: operatorName || 'Operator 1',
      refSize: referenceSizeMm,
      calMethod: calibrationMethod
    });
    navigate(`/camera?${params.toString()}`);
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6 animate-fade-in">
      <div className="space-y-1">
        <h1 className="text-2xl font-bold text-slate-100">Start New Inspection</h1>
        <p className="text-xs text-slate-400">Configure component metadata & calibration reference</p>
      </div>

      <form onSubmit={handleStart} className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-6 shadow-xl">
        <div className="bg-sky-500/10 border border-sky-500/20 rounded-xl p-4 flex items-center justify-between">
          <div>
            <div className="text-xs text-sky-400 font-semibold">INSPECTION SESSION ID</div>
            <div className="text-lg font-black text-white font-mono tracking-wider">{generatedId}</div>
          </div>
          <ShieldCheck className="w-8 h-8 text-sky-400 opacity-80" />
        </div>

        {/* Optional Metadata Inputs */}
        <div className="space-y-4">
          <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Component Information (Optional)</h3>
          
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Component Name</label>
            <input
              type="text"
              placeholder="e.g. M10 Hex Bolt, Washer, Mounting Plate"
              value={componentName}
              onChange={(e) => setComponentName(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Part Number</label>
              <input
                type="text"
                placeholder="e.g. DIN-931-M10"
                value={partNumber}
                onChange={(e) => setPartNumber(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Operator Name</label>
              <input
                type="text"
                placeholder="e.g. Quality Engineer"
                value={operatorName}
                onChange={(e) => setOperatorName(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500"
              />
            </div>
          </div>
        </div>

        {/* Calibration Settings */}
        <div className="space-y-4 pt-2 border-t border-slate-800">
          <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Calibration Reference Setup</h3>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Calibration Method</label>
              <select
                value={calibrationMethod}
                onChange={(e) => setCalibrationMethod(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-sky-500"
              >
                <option value="aruco">ArUco Marker (OpenCV DICT_4X4)</option>
                <option value="known_object">Known Reference Coin / Washer</option>
                <option value="ruler">Guided Ruler Points</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Known Size (mm)</label>
              <input
                type="number"
                step="0.1"
                value={referenceSizeMm}
                onChange={(e) => setReferenceSizeMm(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-sky-500"
              />
            </div>
          </div>
        </div>

        <button
          type="submit"
          className="w-full py-3.5 px-6 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-sm shadow-lg shadow-sky-600/30 transition flex items-center justify-center gap-2"
        >
          <Camera className="w-5 h-5" /> Proceed to Camera Inspection <ArrowRight className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
};
