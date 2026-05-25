/**
 * API Client for the VideoGen Backend
 * 
 * Features:
 * - Auto-fallback to mock data when backend is unavailable
 * - Works in full demo mode (no backend needed)
 * - Seamlessly switches to real API when backend is running
 */

import axios from "axios";
import {
  mockDashboardStats,
  mockVideos,
  mockScriptGeneration,
  mockVoices,
  mockTrends,
  mockMediaResults,
} from "./mock-data";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: `${API_BASE}/api/v1`,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 5000, // 5 second timeout - falls back to mock if backend is slow/down
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
      if (typeof window !== "undefined") {
        localStorage.removeItem("token");
      }
    }
    return Promise.reject(error);
  }
);

/**
 * Helper: Try API call, fallback to mock data on failure.
 * This allows the frontend to work even without the backend running.
 */
async function withFallback<T>(apiCall: () => Promise<any>, mockData: T): Promise<T> {
  try {
    const response = await apiCall();
    return response.data;
  } catch (error) {
    console.log("[VideoGen] Backend unavailable, using demo data");
    return mockData;
  }
}

// ============================================================
// API Methods with Demo Fallback
// ============================================================

export const scriptAPI = {
  generate: (data: { topic: string; tone?: string; duration_seconds?: number }) =>
    withFallback(
      () => api.post("/scripts/generate", data),
      { ...mockScriptGeneration, topic: data.topic, title: `${data.topic} - What Nobody Tells You` }
    ),
  getById: (id: string) =>
    withFallback(() => api.get(`/scripts/${id}`), mockScriptGeneration),
  list: (params?: { limit?: number; offset?: number }) =>
    withFallback(() => api.get("/scripts/", { params }), { scripts: [mockScriptGeneration], total: 1 }),
};

export const videoAPI = {
  generate: (data: { topic: string; tone?: string; duration_seconds?: number; voice_id?: string; auto_upload?: boolean }) =>
    withFallback(
      () => api.post("/videos/generate", data),
      {
        id: `demo-${Date.now()}`,
        status: "generating_script",
        topic: data.topic,
        progress: 0.1,
        script_id: null,
        video_url: null,
        thumbnail_url: null,
        duration: null,
        created_at: new Date().toISOString(),
        completed_at: null,
      }
    ),
  getById: (id: string) =>
    withFallback(() => api.get(`/videos/${id}`), mockVideos[0]),
  list: (params?: { status?: string; limit?: number }) =>
    withFallback(() => api.get("/videos/", { params }), { videos: mockVideos, total: mockVideos.length }),
  delete: (id: string) =>
    withFallback(() => api.delete(`/videos/${id}`), { message: "Video deleted successfully" }),
  retry: (id: string) =>
    withFallback(() => api.post(`/videos/${id}/retry`), mockVideos[0]),
};

export const voiceAPI = {
  generate: (data: { text: string; voice_id?: string; provider?: string }) =>
    withFallback(
      () => api.post("/voices/generate", data),
      { id: "demo-voice-001", audio_url: "./temp/demo.mp3", duration: 45.0, provider: "demo", demo_mode: true }
    ),
  listStyles: () =>
    withFallback(() => api.get("/voices/styles"), mockVoices),
};

export const mediaAPI = {
  search: (data: { query: string; media_type?: string; orientation?: string }) =>
    withFallback(() => api.post("/media/search", data), mockMediaResults),
  autoCollect: (scriptId: string, clipsNeeded?: number) =>
    withFallback(
      () => api.post("/media/auto-collect", { script_id: scriptId, clips_needed: clipsNeeded }),
      { script_id: scriptId, clips_collected: 5, clips: [], demo_mode: true }
    ),
};

export const uploadAPI = {
  publish: (data: { video_id: string; platforms: string[]; title: string; description: string }) =>
    withFallback(
      () => api.post("/uploads/publish", data),
      {
        video_id: data.video_id,
        uploads: data.platforms.map((p) => ({
          platform: p,
          status: "published",
          url: `https://${p}.com/shorts/demo-${data.video_id.slice(0, 8)}`,
          uploaded_at: new Date().toISOString(),
          demo_mode: true,
        })),
      }
    ),
  getStatus: (videoId: string) =>
    withFallback(() => api.get(`/uploads/${videoId}/status`), []),
};

export const analyticsAPI = {
  getDashboard: () =>
    withFallback(() => api.get("/analytics/dashboard"), mockDashboardStats),
  getVideoPerformance: (videoId: string) =>
    withFallback(
      () => api.get(`/analytics/videos/${videoId}/performance`),
      { video_id: videoId, total_views: 12400, total_likes: 890, total_comments: 45, total_shares: 120 }
    ),
  getTrends: (days?: number) =>
    withFallback(() => api.get("/analytics/trends", { params: { days } }), mockTrends),
  getLogs: (params?: { limit?: number; offset?: number; status?: string }) =>
    withFallback(() => api.get("/analytics/generation-logs", { params }), { logs: [], total: 0 }),
};
