import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchInspectionHistory } from '../api/client';
import { History, Search, ArrowRight, FileText } from 'lucide-react';

export const HistoryPage: React.FC = () => {
  const [history, setHistory] = useState<any[]>([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInspectionHistory()
      .then((data) => {
        setHistory(data);
        setLoading(false);
      })
      .catch(() => {
        // Fallback default sample history
        setHistory([
          {
            inspection_id: 'INS-2026-000124',
            created_at: '2026-09-13 14:20:00',
            component_type: 'hex_bolt',
            component_name: 'M10 Hex Bolt',
            status: 'PASS',
            scale_px_per_mm: 8.42
          },
          {
            inspection_id: 'INS-2026-000123',
            created_at: '2026-09-12 11:15:00',
            component_type: 'washer',
            component_name: 'M10 Form A Washer',
            status: 'PASS',
            scale_px_per_mm: 8.38
          },
          {
            inspection_id: 'INS-2026-000122',
            created_at: '2026-09-12 09:40:00',
            component_type: 'plate',
            component_name: '4-Hole Plate',
            status: 'REVIEW',
            scale_px_per_mm: 8.40
          }
        ]);
        setLoading(false);
      });
  }, []);

  const filtered = history.filter((item) =>
    item.inspection_id.toLowerCase().includes(query.toLowerCase()) ||
    (item.component_name && item.component_name.toLowerCase().includes(query.toLowerCase())) ||
    (item.component_type && item.component_type.toLowerCase().includes(query.toLowerCase()))
  );

  return (
    <div className="space-y-6 animate-fade-in max-w-5xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <History className="w-6 h-6 text-sky-400" /> Inspection History
          </h1>
          <p className="text-xs text-slate-400">Stored metrology inspections & generated PDF reports</p>
        </div>

        {/* Search Input */}
        <div className="relative min-w-[240px]">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search Inspection ID, part..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-4 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500"
          />
        </div>
      </div>

      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        {loading ? (
          <div className="p-8 text-center text-xs text-slate-400">Loading inspection records...</div>
        ) : filtered.length === 0 ? (
          <div className="p-8 text-center text-xs text-slate-400">No inspection records found.</div>
        ) : (
          <div className="divide-y divide-slate-800/80">
            {filtered.map((record) => (
              <div key={record.inspection_id} className="p-4 flex items-center justify-between gap-4 hover:bg-slate-800/40 transition">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-center font-bold text-sky-400">
                    <FileText className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="font-bold text-sm text-slate-100">{record.component_name || record.component_type.toUpperCase()}</div>
                    <div className="text-xs text-slate-400 font-mono">{record.inspection_id} • {record.created_at}</div>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="hidden sm:block text-right text-xs">
                    <div className="text-slate-300 font-medium">{record.scale_px_per_mm?.toFixed(2)} px/mm</div>
                    <div className="text-slate-500 text-[10px]">ArUco Scale</div>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                    record.status === 'PASS' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                  }`}>
                    {record.status}
                  </span>
                  <Link to={`/result?id=${record.inspection_id}`} className="p-2 text-slate-400 hover:text-sky-400">
                    <ArrowRight className="w-5 h-5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
