/**
 * Global State Management using Zustand
 * Manages application state for the video generation platform.
 */

import { create } from "zustand";

interface VideoJob {
  id: string;
  topic: string;
  status: string;
  progress: number;
  videoUrl?: string;
  createdAt: string;
}

interface AppState {
  // Video generation
  currentJob: VideoJob | null;
  jobs: VideoJob[];
  isGenerating: boolean;
  
  // UI state
  sidebarOpen: boolean;
  
  // Actions
  setCurrentJob: (job: VideoJob | null) => void;
  addJob: (job: VideoJob) => void;
  updateJob: (id: string, updates: Partial<VideoJob>) => void;
  setIsGenerating: (val: boolean) => void;
  toggleSidebar: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  // State
  currentJob: null,
  jobs: [],
  isGenerating: false,
  sidebarOpen: true,

  // Actions
  setCurrentJob: (job) => set({ currentJob: job }),
  addJob: (job) => set((state) => ({ jobs: [job, ...state.jobs] })),
  updateJob: (id, updates) =>
    set((state) => ({
      jobs: state.jobs.map((j) => (j.id === id ? { ...j, ...updates } : j)),
      currentJob:
        state.currentJob?.id === id
          ? { ...state.currentJob, ...updates }
          : state.currentJob,
    })),
  setIsGenerating: (val) => set({ isGenerating: val }),
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
}));
