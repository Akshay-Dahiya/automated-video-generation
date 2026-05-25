/**
 * API Client for the VideoGen Backend
 * Handles all HTTP requests to the FastAPI backend.
 */

import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: `${API_BASE}/api/v1`,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor for auth
api.interceptors.request.use((config) => {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      if (typeof window !== "undefined") {
        localStorage.removeItem("token");
      }
    }
    return Promise.reject(error);
  }
);

// API methods
export const scriptAPI = {
  generate: (data: {
    topic: string;
    tone?: string;
    duration_seconds?: number;
  }) => api.post("/scripts/generate", data),
  getById: (id: string) => api.get(`/scripts/${id}`),
  list: (params?: { limit?: number; offset?: number }) =>
    api.get("/scripts/", { params }),
};

export const videoAPI = {
  generate: (data: {
    topic: string;
    tone?: string;
    duration_seconds?: number;
    voice_id?: string;
    auto_upload?: boolean;
  }) => api.post("/videos/generate", data),
  getById: (id: string) => api.get(`/videos/${id}`),
  list: (params?: { status?: string; limit?: number }) =>
    api.get("/videos/", { params }),
  delete: (id: string) => api.delete(`/videos/${id}`),
  retry: (id: string) => api.post(`/videos/${id}/retry`),
};

export const voiceAPI = {
  generate: (data: { text: string; voice_id?: string; provider?: string }) =>
    api.post("/voices/generate", data),
  listStyles: () => api.get("/voices/styles"),
};

export const mediaAPI = {
  search: (data: { query: string; media_type?: string; orientation?: string }) =>
    api.post("/media/search", data),
  autoCollect: (scriptId: string, clipsNeeded?: number) =>
    api.post("/media/auto-collect", { script_id: scriptId, clips_needed: clipsNeeded }),
};

export const uploadAPI = {
  publish: (data: {
    video_id: string;
    platforms: string[];
    title: string;
    description: string;
  }) => api.post("/uploads/publish", data),
  getStatus: (videoId: string) => api.get(`/uploads/${videoId}/status`),
};

export const analyticsAPI = {
  getDashboard: () => api.get("/analytics/dashboard"),
  getVideoPerformance: (videoId: string) =>
    api.get(`/analytics/videos/${videoId}/performance`),
  getTrends: (days?: number) => api.get("/analytics/trends", { params: { days } }),
  getLogs: (params?: { limit?: number; offset?: number; status?: string }) =>
    api.get("/analytics/generation-logs", { params }),
};
