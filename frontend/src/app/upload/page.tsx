"use client";

import { motion } from "framer-motion";
import { Upload, Youtube, Instagram, Music2, Link2, CheckCircle } from "lucide-react";

const platforms = [
  {
    id: "youtube",
    name: "YouTube Shorts",
    icon: Youtube,
    connected: true,
    color: "from-red-500/20 to-red-600/5",
    textColor: "text-red-400",
  },
  {
    id: "instagram",
    name: "Instagram Reels",
    icon: Instagram,
    connected: true,
    color: "from-pink-500/20 to-purple-600/5",
    textColor: "text-pink-400",
  },
  {
    id: "tiktok",
    name: "TikTok",
    icon: Music2,
    connected: false,
    color: "from-dark-500/20 to-dark-600/5",
    textColor: "text-dark-100",
  },
];

export default function UploadPage() {
  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-bold">
          <span className="glow-text">Publish</span>
        </h1>
        <p className="text-dark-100 mt-1">Upload videos to social platforms</p>
      </motion.div>

      {/* Connected Platforms */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <h2 className="text-lg font-semibold text-white mb-4">Connected Platforms</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {platforms.map((platform) => (
            <div
              key={platform.id}
              className={`p-4 rounded-xl bg-gradient-to-br ${platform.color} border border-white/5 flex items-center gap-3`}
            >
              <platform.icon className={`w-6 h-6 ${platform.textColor}`} />
              <div className="flex-1">
                <p className="text-sm font-medium text-white">{platform.name}</p>
                <p className="text-xs text-dark-200">
                  {platform.connected ? "Connected" : "Not connected"}
                </p>
              </div>
              {platform.connected ? (
                <CheckCircle className="w-5 h-5 text-emerald-400" />
              ) : (
                <button className="px-3 py-1 text-xs rounded-lg bg-white/10 text-white hover:bg-white/20 transition-colors">
                  Connect
                </button>
              )}
            </div>
          ))}
        </div>
      </motion.div>

      {/* Upload Form */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="glass-card p-6"
      >
        <h2 className="text-lg font-semibold text-white mb-4">Publish Video</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm text-dark-100 mb-2">Select Video</label>
            <select className="glass-input">
              <option value="">Choose a rendered video...</option>
              <option>5 AI Tools You Need in 2024</option>
              <option>Why Python is Taking Over</option>
              <option>Morning Routine for Success</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-dark-100 mb-2">Title</label>
            <input placeholder="Video title for platforms..." className="glass-input" />
          </div>
          <div>
            <label className="block text-sm text-dark-100 mb-2">Description</label>
            <textarea placeholder="Video description..." className="glass-input h-24 resize-none" />
          </div>
          <div>
            <label className="block text-sm text-dark-100 mb-2">Platforms</label>
            <div className="flex gap-3">
              {platforms.filter(p => p.connected).map(p => (
                <label key={p.id} className="flex items-center gap-2 px-3 py-2 rounded-lg bg-white/5 border border-white/5 cursor-pointer hover:bg-white/10">
                  <input type="checkbox" className="accent-primary-500" />
                  <span className="text-sm text-white">{p.name}</span>
                </label>
              ))}
            </div>
          </div>
          <motion.button
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            className="w-full glass-button flex items-center justify-center gap-2"
          >
            <Upload className="w-4 h-4" />
            Publish Now
          </motion.button>
        </div>
      </motion.div>
    </div>
  );
}
