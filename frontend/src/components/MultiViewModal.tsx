import React from 'react';
import { Camera, X, CheckCircle2 } from 'lucide-react';

interface MultiViewModalProps {
  isOpen: boolean;
  reason?: string;
  onClose: () => void;
  onCaptureSideView: () => void;
}

export const MultiViewModal: React.FC<MultiViewModalProps> = ({
  isOpen,
  reason,
  onClose,
  onCaptureSideView
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-sky-400">
            <Camera className="w-6 h-6" />
            <h3 className="text-lg font-bold text-slate-100">Multi-View Request</h3>
          </div>
          <button onClick={onClose} className="p-1 text-slate-400 hover:text-slate-200">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="bg-amber-500/10 border border-amber-500/20 rounded-xl p-4 space-y-2">
          <div className="text-xs font-semibold text-amber-400 uppercase tracking-wider">
            Additional View Required
          </div>
          <p className="text-sm text-amber-200">
            {reason || "Thickness/height cannot be measured from a single top-down image. A side view is required."}
          </p>
        </div>

        <div className="space-y-2 text-xs text-slate-400">
          <div className="flex items-center gap-2 text-slate-300">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>View 1 (Top-down planar geometry): Captured</span>
          </div>
          <div className="flex items-center gap-2 text-amber-300 font-medium">
            <div className="w-4 h-4 rounded-full border-2 border-amber-400 border-t-transparent animate-spin shrink-0" />
            <span>View 2 (Side profile height): Awaiting Capture</span>
          </div>
        </div>

        <div className="flex gap-3 pt-2">
          <button
            onClick={onClose}
            className="flex-1 py-2.5 px-4 rounded-xl border border-slate-700 text-slate-300 hover:bg-slate-800 font-semibold text-sm transition"
          >
            Skip Side View
          </button>
          <button
            onClick={onCaptureSideView}
            className="flex-1 py-2.5 px-4 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-semibold text-sm shadow-lg shadow-sky-600/30 transition flex items-center justify-center gap-2"
          >
            <Camera className="w-4 h-4" /> Capture Side View
          </button>
        </div>
      </div>
    </div>
  );
};
