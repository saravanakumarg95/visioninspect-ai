import React from 'react';

interface SourceBadgeProps {
  source: 'DIRECT' | 'AI ESTIMATED' | 'DATABASE MATCH' | 'INSUFFICIENT DATA';
}

export const SourceBadge: React.FC<SourceBadgeProps> = ({ source }) => {
  switch (source) {
    case 'DIRECT':
      return (
        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
          DIRECT
        </span>
      );
    case 'AI ESTIMATED':
      return (
        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-sky-500/20 text-sky-400 border border-sky-500/30">
          AI ESTIMATED
        </span>
      );
    case 'DATABASE MATCH':
      return (
        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-purple-500/20 text-purple-400 border border-purple-500/30">
          DATABASE MATCH
        </span>
      );
    case 'INSUFFICIENT DATA':
    default:
      return (
        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-amber-500/20 text-amber-400 border border-amber-500/30">
          INSUFFICIENT DATA
        </span>
      );
  }
};
