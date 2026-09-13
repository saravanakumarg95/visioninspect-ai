import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useCamera } from '../hooks/useCamera';
import { checkCameraQuality, uploadImageInspection } from '../api/client';
import type { QualityAnalysisResult, InspectionResponse } from '../types/inspection';
import { QualityMeter } from '../components/QualityMeter';
import { 
  Camera as CameraIcon, RefreshCw, Upload, 
  AlertTriangle, ShieldCheck, Loader2, ArrowLeft 
} from 'lucide-react';

export const CameraPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const inspectionId = searchParams.get('id') || 'INS-2026-000124';
  const componentName = searchParams.get('name') || 'M10 Hex Bolt';
  const referenceSizeMm = parseFloat(searchParams.get('refSize') || '50.0');
  const calibrationMethod = searchParams.get('calMethod') || 'aruco';

  const {
    videoRef,
    isCameraActive,
    error: cameraError,
    startCamera,
    stopCamera,
    toggleCameraFacing,
    captureFrame
  } = useCamera({ facingMode: 'environment' });

  const [mode, setMode] = useState<'photo' | 'video' | 'live'>('photo');
  const [capturedBlob, setCapturedBlob] = useState<Blob | null>(null);
  const [capturedPreviewUrl, setCapturedPreviewUrl] = useState<string | null>(null);
  const [qualityResult, setQualityResult] = useState<QualityAnalysisResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);

  // Auto start camera on mount
  useEffect(() => {
    startCamera();
    return () => stopCamera();
  }, []);

  const handleCapture = async () => {
    const blob = captureFrame();
    if (!blob) {
      // Fallback: If camera snapshot fails or unavailable, fetch sample image for demonstration
      try {
        const res = await fetch('/sample_data/bolt_aruco.png');
        const sampleBlob = await res.blob();
        processBlob(sampleBlob);
      } catch (err) {
        setAnalysisError("Failed to capture frame from camera.");
      }
      return;
    }
    processBlob(blob);
  };

  const processBlob = async (blob: Blob) => {
    setCapturedBlob(blob);
    const previewUrl = URL.createObjectURL(blob);
    setCapturedPreviewUrl(previewUrl);

    // Run Quality Check
    const file = new File([blob], "capture.jpg", { type: "image/jpeg" });
    try {
      const q = await checkCameraQuality(file);
      setQualityResult(q);
    } catch (err) {
      console.warn("Quality check failed:", err);
    }
  };

  const handleUploadFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      processBlob(file);
    }
  };

  const handleRunSampleData = async (sampleName: string) => {
    try {
      const res = await fetch(`/sample_data/${sampleName}`);
      const blob = await res.blob();
      processBlob(blob);
    } catch (err) {
      setAnalysisError("Failed to load sample image.");
    }
  };

  const handleExecuteAnalysis = async () => {
    if (!capturedBlob) return;
    setIsAnalyzing(true);
    setAnalysisError(null);

    try {
      const file = new File([capturedBlob], "inspection_frame.jpg", { type: "image/jpeg" });
      const response: InspectionResponse = await uploadImageInspection(
        file,
        null,
        referenceSizeMm,
        calibrationMethod,
        componentName
      );

      // Navigate to Inspection Result Page with analysis data
      navigate(`/result?id=${response.inspection_id}`, { state: { inspection: response } });
    } catch (err: any) {
      console.error("Analysis error:", err);
      setAnalysisError(err.response?.data?.detail || "Failed to execute computer vision analysis backend pipeline.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-fade-in">
      {/* Header Bar */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <button onClick={() => navigate('/new')} className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200">
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2">
              <CameraIcon className="w-5 h-5 text-sky-400" /> Camera Viewport
            </h1>
            <p className="text-xs text-slate-400">Session: <span className="font-mono text-sky-400">{inspectionId}</span> • Ref: {referenceSizeMm} mm</p>
          </div>
        </div>

        {/* Mode Selector Tabs */}
        <div className="flex bg-slate-900 border border-slate-800 rounded-xl p-1 text-xs font-semibold">
          <button
            onClick={() => setMode('photo')}
            className={`px-3 py-1.5 rounded-lg transition ${mode === 'photo' ? 'bg-sky-600 text-white' : 'text-slate-400 hover:text-slate-200'}`}
          >
            PHOTO
          </button>
          <button
            onClick={() => setMode('video')}
            className={`px-3 py-1.5 rounded-lg transition ${mode === 'video' ? 'bg-sky-600 text-white' : 'text-slate-400 hover:text-slate-200'}`}
          >
            VIDEO
          </button>
          <button
            onClick={() => setMode('live')}
            className={`px-3 py-1.5 rounded-lg transition ${mode === 'live' ? 'bg-sky-600 text-white' : 'text-slate-400 hover:text-slate-200'}`}
          >
            LIVE
          </button>
        </div>
      </div>

      {/* Main Viewport Container */}
      <div className="relative bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
        {/* Camera Error / Warning Banner */}
        {cameraError && !capturedPreviewUrl && (
          <div className="p-4 bg-amber-500/10 border-b border-amber-500/20 text-xs text-amber-300 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
              <span>Camera unavailable or permission restricted. Select file upload or sample demonstration below.</span>
            </div>
            <button onClick={startCamera} className="px-2.5 py-1 bg-amber-500/20 hover:bg-amber-500/30 rounded font-semibold text-amber-200">
              Retry
            </button>
          </div>
        )}

        {/* Viewport View (Live Camera Stream or Captured Image) */}
        <div className="relative w-full aspect-[4/3] bg-black flex items-center justify-center">
          {capturedPreviewUrl ? (
            <img src={capturedPreviewUrl} alt="Captured preview" className="w-full h-full object-contain" />
          ) : (
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="w-full h-full object-cover"
            />
          )}

          {/* ArUco Calibration Guide Frame Overlay */}
          {!capturedPreviewUrl && (
            <div className="absolute inset-0 pointer-events-none border-2 border-dashed border-sky-400/40 m-8 rounded-2xl flex items-center justify-center">
              <div className="text-center bg-slate-950/70 backdrop-blur-md px-4 py-2 rounded-xl text-xs text-slate-200 border border-slate-800">
                Place 50 mm ArUco marker beside component in frame
              </div>
            </div>
          )}

          {/* Live Indicator */}
          {isCameraActive && !capturedPreviewUrl && (
            <div className="absolute top-4 left-4 flex items-center gap-2 px-3 py-1 rounded-full bg-slate-950/80 backdrop-blur-md border border-slate-800 text-xs font-semibold text-emerald-400">
              <div className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              LIVE STREAM ACTIVE
            </div>
          )}
        </div>

        {/* Camera Control Panel */}
        <div className="p-4 bg-slate-950 border-t border-slate-800 flex items-center justify-between gap-4">
          {capturedPreviewUrl ? (
            <div className="flex items-center gap-3 w-full">
              <button
                onClick={() => { setCapturedBlob(null); setCapturedPreviewUrl(null); setQualityResult(null); startCamera(); }}
                className="flex-1 py-3 px-4 rounded-xl border border-slate-700 text-slate-300 hover:bg-slate-800 font-semibold text-sm transition"
              >
                Retake Frame
              </button>
              <button
                onClick={handleExecuteAnalysis}
                disabled={isAnalyzing}
                className="flex-1 py-3 px-4 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-sm shadow-lg shadow-sky-600/30 transition flex items-center justify-center gap-2"
              >
                {isAnalyzing ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" /> Analyzing Computer Vision...
                  </>
                ) : (
                  <>
                    <ShieldCheck className="w-5 h-5" /> Analyze Component
                  </>
                )}
              </button>
            </div>
          ) : (
            <>
              <button
                onClick={toggleCameraFacing}
                className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-slate-100"
                title="Switch Camera"
              >
                <RefreshCw className="w-5 h-5" />
              </button>

              <button
                onClick={handleCapture}
                className="w-16 h-16 rounded-full bg-sky-600 border-4 border-slate-950 shadow-xl shadow-sky-600/40 hover:bg-sky-500 transition transform active:scale-95 flex items-center justify-center text-white"
              >
                <div className="w-6 h-6 rounded-full bg-white" />
              </button>

              <label className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-slate-100 cursor-pointer" title="Upload Image File">
                <Upload className="w-5 h-5" />
                <input type="file" accept="image/*" onChange={handleUploadFileChange} className="hidden" />
              </label>
            </>
          )}
        </div>
      </div>

      {/* Sample Data Fast Selectors for Demonstration */}
      {!capturedPreviewUrl && (
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 space-y-2">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Fast Demonstration Test Cases (Pre-calibrated ArUco 50mm)
          </span>
          <div className="flex flex-wrap gap-3 pt-1">
            <button
              onClick={() => handleRunSampleData('bolt_aruco.png')}
              className="px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700 flex items-center gap-2"
            >
              🔩 Sample M10 Hex Bolt
            </button>
            <button
              onClick={() => handleRunSampleData('washer_aruco.png')}
              className="px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700 flex items-center gap-2"
            >
              ⭕ Sample M10 Washer
            </button>
            <button
              onClick={() => handleRunSampleData('plate_aruco.png')}
              className="px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700 flex items-center gap-2"
            >
              🔲 Sample 4-Hole Plate
            </button>
          </div>
        </div>
      )}

      {/* Quality Analysis Results */}
      {qualityResult && (
        <div className="animate-fade-in">
          <QualityMeter quality={qualityResult} />
        </div>
      )}

      {/* Analysis Error Message */}
      {analysisError && (
        <div className="p-4 bg-rose-500/10 border border-rose-500/30 rounded-xl text-xs text-rose-300 font-medium">
          ⚠️ {analysisError}
        </div>
      )}
    </div>
  );
};
