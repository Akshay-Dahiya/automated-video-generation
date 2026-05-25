"use client";

import { motion } from "framer-motion";
import {
  TrendingUp,
  Eye,
  ThumbsUp,
  Share2,
  BarChart3,
  ArrowUp,
  ArrowDown,
} from "lucide-react";

const platformStats = [
  { name: "YouTube Shorts", views: "89.2K", growth: "+34%", color: "bg-red-500" },
  { name: "Instagram Reels", views: "45.8K", growth: "+12%", color: "bg-pink-500" },
  { name: "TikTok", views: "23.1K", growth: "+8%", color: "bg-dark-400" },
];

const topVideos = [
  { title: "5 AI Tools You Need", views: "23.1K", likes: "2.1K", shares: "450" },
  { title: "Morning Routine Success", views: "15.8K", likes: "1.8K", shares: "320" },
  { title: "Python is Taking Over", views: "12.4K", likes: "980", shares: "210" },
  { title: "Future of Remote Work", views: "8.2K", likes: "670", shares: "140" },
];

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-bold">
          <span className="glow-text">Analytics</span>
        </h1>
        <p className="text-dark-100 mt-1">Track your video performance</p>
      </motion.div>

      {/* Platform Performance */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {platformStats.map((platform, index) => (
          <motion.div
            key={platform.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="glass-card p-5"
          >
            <div className="flex items-center gap-3 mb-3">
              <div className={`w-3 h-3 rounded-full ${platform.color}`} />
              <span className="text-sm text-dark-100">{platform.name}</span>
            </div>
            <p className="text-2xl font-bold text-white">{platform.views}</p>
            <div className="flex items-center gap-1 mt-1">
              <ArrowUp className="w-3 h-3 text-emerald-400" />
              <span className="text-xs text-emerald-400">{platform.growth}</span>
              <span className="text-xs text-dark-200">vs last week</span>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass-card p-4 text-center">
          <Eye className="w-5 h-5 text-cyan-400 mx-auto mb-2" />
          <p className="text-xl font-bold text-white">158.1K</p>
          <p className="text-xs text-dark-200">Total Views</p>
        </motion.div>
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1 }} className="glass-card p-4 text-center">
          <ThumbsUp className="w-5 h-5 text-purple-400 mx-auto mb-2" />
          <p className="text-xl font-bold text-white">5.5K</p>
          <p className="text-xs text-dark-200">Total Likes</p>
        </motion.div>
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }} className="glass-card p-4 text-center">
          <Share2 className="w-5 h-5 text-pink-400 mx-auto mb-2" />
          <p className="text-xl font-bold text-white">1.1K</p>
          <p className="text-xs text-dark-200">Total Shares</p>
        </motion.div>
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }} className="glass-card p-4 text-center">
          <BarChart3 className="w-5 h-5 text-emerald-400 mx-auto mb-2" />
          <p className="text-xl font-bold text-white">6.2%</p>
          <p className="text-xs text-dark-200">Engagement Rate</p>
        </motion.div>
      </div>

      {/* Top Performing Videos */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="glass-card"
      >
        <div className="p-6 border-b border-white/5">
          <h2 className="text-lg font-semibold text-white">Top Performing Videos</h2>
        </div>
        <div className="divide-y divide-white/5">
          {topVideos.map((video, index) => (
            <div key={index} className="flex items-center gap-4 p-4 hover:bg-white/[0.02]">
              <span className="text-lg font-bold text-dark-300 w-6">#{index + 1}</span>
              <div className="flex-1">
                <p className="text-sm font-medium text-white">{video.title}</p>
              </div>
              <div className="flex gap-6 text-right">
                <div>
                  <p className="text-sm font-medium text-white">{video.views}</p>
                  <p className="text-xs text-dark-200">views</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-white">{video.likes}</p>
                  <p className="text-xs text-dark-200">likes</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-white">{video.shares}</p>
                  <p className="text-xs text-dark-200">shares</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
