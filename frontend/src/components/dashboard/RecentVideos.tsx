"use client";

import { motion } from "framer-motion";
import { Play, CheckCircle, Clock, AlertCircle, MoreVertical } from "lucide-react";

const mockVideos = [
  {
    id: "1",
    title: "5 AI Tools You Need in 2024",
    status: "completed",
    platform: "YouTube Shorts",
    views: "12.4K",
    duration: "0:58",
    createdAt: "2 hours ago",
  },
  {
    id: "2",
    title: "Why Python is Taking Over",
    status: "rendering",
    platform: "Instagram Reels",
    views: "-",
    duration: "0:45",
    createdAt: "4 hours ago",
  },
  {
    id: "3",
    title: "Morning Routine for Success",
    status: "completed",
    platform: "TikTok",
    views: "8.2K",
    duration: "1:00",
    createdAt: "1 day ago",
  },
  {
    id: "4",
    title: "Web Development in 60 Seconds",
    status: "failed",
    platform: "YouTube Shorts",
    views: "-",
    duration: "0:55",
    createdAt: "1 day ago",
  },
  {
    id: "5",
    title: "The Future of Remote Work",
    status: "completed",
    platform: "Instagram Reels",
    views: "23.1K",
    duration: "0:50",
    createdAt: "2 days ago",
  },
];

const statusConfig = {
  completed: { icon: CheckCircle, color: "text-emerald-400", bg: "bg-emerald-500/20" },
  rendering: { icon: Clock, color: "text-yellow-400", bg: "bg-yellow-500/20" },
  failed: { icon: AlertCircle, color: "text-red-400", bg: "bg-red-500/20" },
};

export function RecentVideos() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
      className="glass-card"
    >
      <div className="flex items-center justify-between p-6 border-b border-white/5">
        <h2 className="text-lg font-semibold text-white">Recent Videos</h2>
        <button className="text-sm text-primary-400 hover:text-primary-300 transition-colors">
          View All
        </button>
      </div>

      <div className="divide-y divide-white/5">
        {mockVideos.map((video, index) => {
          const status = statusConfig[video.status as keyof typeof statusConfig];
          const StatusIcon = status.icon;

          return (
            <motion.div
              key={video.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
              className="flex items-center gap-4 p-4 hover:bg-white/[0.02] transition-colors"
            >
              {/* Thumbnail placeholder */}
              <div className="w-16 h-10 rounded-lg bg-dark-600 flex items-center justify-center flex-shrink-0">
                <Play className="w-4 h-4 text-dark-200" />
              </div>

              {/* Info */}
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white truncate">
                  {video.title}
                </p>
                <p className="text-xs text-dark-200">
                  {video.platform} · {video.duration} · {video.createdAt}
                </p>
              </div>

              {/* Status */}
              <div className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full ${status.bg}`}>
                <StatusIcon className={`w-3.5 h-3.5 ${status.color}`} />
                <span className={`text-xs font-medium ${status.color} capitalize`}>
                  {video.status}
                </span>
              </div>

              {/* Views */}
              <div className="text-right hidden sm:block">
                <p className="text-sm font-medium text-white">{video.views}</p>
                <p className="text-xs text-dark-200">views</p>
              </div>

              {/* Actions */}
              <button className="p-1 rounded-lg hover:bg-white/5">
                <MoreVertical className="w-4 h-4 text-dark-200" />
              </button>
            </motion.div>
          );
        })}
      </div>
    </motion.div>
  );
}
