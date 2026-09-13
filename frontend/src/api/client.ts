import axios from 'axios';
import type { InspectionResponse, QualityAnalysisResult } from '../types/inspection';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
});

export const uploadImageInspection = async (
  file: File,
  sideFile: File | null = null,
  referenceSizeMm: number = 50.0,
  calibrationMethod: string = 'aruco',
  componentName?: string,
  partNumber?: string,
  operatorName?: string
): Promise<InspectionResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  if (sideFile) {
    formData.append('side_file', sideFile);
  }
  formData.append('reference_size_mm', referenceSizeMm.toString());
  formData.append('calibration_method', calibrationMethod);
  if (componentName) formData.append('component_name', componentName);
  if (partNumber) formData.append('part_number', partNumber);
  if (operatorName) formData.append('operator_name', operatorName);

  const res = await api.post<InspectionResponse>('/api/analyze/image', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
};

export const checkCameraQuality = async (file: File): Promise<QualityAnalysisResult> => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await api.post<QualityAnalysisResult>('/api/camera/quality-check', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
};

export const fetchInspectionHistory = async (): Promise<any[]> => {
  const res = await api.get<any[]>('/api/inspections');
  return res.data;
};

export const fetchInspectionById = async (id: string): Promise<any> => {
  const res = await api.get<any>(`/api/inspections/${id}`);
  return res.data;
};

export const searchStandards = async (query: string = ''): Promise<any> => {
  const res = await api.get<any>(`/api/standards/search?query=${encodeURIComponent(query)}`);
  return res.data;
};
