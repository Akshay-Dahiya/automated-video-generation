"use client";

import { motion } from "framer-motion";
import { Video, Filter, Search, Play, Download, Trash2 } from "lucide-react";

const videos = [
  { id: "1", title: "5 AI Tools You Need in 2024", status: "completed", duration: "0:58", views: "12.4K", date: "2024-01-15" },
  { id: "2", title: "Why Python is Taking Over", status: "completed", duration: "0:45", views: "8.2K", date: "2024-01-14" },
  { id: "3", title: "Morning Routine for Success", status: "completed", duration: "1:00", views: "23.1K", date: "2024-01-13" },
  { id: "4", title: "Web Dev in 60 Seconds", status: "completed", duration: "0:55", views: "5.6K", date: "2024-01-12" },
  { id: "5", title: "The Future of Remote Work", status: "completed", duration: "0:50", views: "15.8K", date: "2024-01-11" },
  { id: "6", title: "Crypto Explained Simply", status: "rendering", duration: "0:48", views: "-", date: "2024-01-10" },
];

export default function VideosPage() {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold">
            <span className="glow-text">Video Library</span>
          </h1>
          <p className="text-dark-100 mt-1">Manage all your generated videos</p>
        </div>
        <div className="flex gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-dark-200" />
            <input
              placeholder="Search videos..."
              className="pl-9 pr-4 py-2 rounded-xl bg-white/5 border border-white/5 text-sm text-white placeholder:text-dark-200 focus:border-primary-500/30 focus:outline-none"
            />
          </div>
          <button className="px-4 py-2 rounded-xl bg-white/5 border border-white/5 flex items-center gap-2 text-sm text-dark-100 hover:bg-white/10 transition-colors">
            <Filter className="w-4 h-4" />
            Filter
          </button>
        </div>
      </motion.div>

      {/* Video Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {videos.map((video, index) => (
          <motion.div
            key={video.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            className="glass-card-hover group"
          >
            {/* Thumbnail */}
            <div className="aspect-[9/16] max-h-48 bg-dark-700 rounded-t-2xl flex items-center justify-center relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-t from-dark-900/80 to-transparent" />
              <Video className="w-8 h-8 text-dark-300" />
              <div className="absolute bottom-2 right-2 px-2 py-0.5 rounded bg-black/60 text-xs text-white">
                {video.duration}
              </div>
              {/* Hover overlay */}
              <div className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <Play className="w-10 h-10 text-white" />
              </div>
            </div>

            {/* Info */}
            <div className="p-4">
              <h3 className="text-sm font-medium text-white truncate">{video.title}</h3>
              <p className="text-xs text-dark-200 mt-1">
                {video.date} · {video.views} views
              </p>
              <div className="flex items-center gap-2 mt-3">
                <button className="flex-1 px-3 py-1.5 rounded-lg bg-primary-600/20 text-primary-400 text-xs font-medium hover:bg-primary-600/30 transition-colors">
                  <Download className="w-3 h-3 inline mr-1" />
                  Download
                </button>
                <button className="p-1.5 rounded-lg bg-red-500/10 text-red-400 hover:bg-red-500/20 transition-colors">
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
