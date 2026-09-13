import React from 'react';

interface DefectBadgeProps {
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
}

export const DefectBadge: React.FC<DefectBadgeProps> = ({ severity }) => {
  switch (severity) {
    case 'LOW':
      return <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-slate-300">LOW</span>;
    case 'MEDIUM':
      return <span className="px-2 py-0.5 rounded text-xs font-medium bg-amber-500/20 text-amber-400 border border-amber-500/30">MEDIUM</span>;
    case 'HIGH':
    case 'CRITICAL':
    default:
      return <span className="px-2 py-0.5 rounded text-xs font-medium bg-rose-500/20 text-rose-400 border border-rose-500/30">HIGH SEVERITY</span>;
  }
};
