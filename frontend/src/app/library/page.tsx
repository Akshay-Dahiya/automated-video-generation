"use client";

import { motion } from "framer-motion";
import { FileText, Mic, Image, Music, Search, Plus } from "lucide-react";

const assets = [
  { id: "1", name: "AI Tools Script", type: "script", date: "2024-01-15" },
  { id: "2", name: "Rachel Voiceover", type: "voice", date: "2024-01-15" },
  { id: "3", name: "Tech Background", type: "media", date: "2024-01-14" },
  { id: "4", name: "Upbeat Electronic", type: "music", date: "2024-01-14" },
  { id: "5", name: "Python Tutorial Script", type: "script", date: "2024-01-13" },
  { id: "6", name: "City Timelapse", type: "media", date: "2024-01-13" },
  { id: "7", name: "Motivational Voice", type: "voice", date: "2024-01-12" },
  { id: "8", name: "Lo-fi Background", type: "music", date: "2024-01-12" },
];

const typeConfig = {
  script: { icon: FileText, color: "text-cyan-400", bg: "bg-cyan-500/20" },
  voice: { icon: Mic, color: "text-purple-400", bg: "bg-purple-500/20" },
  media: { icon: Image, color: "text-pink-400", bg: "bg-pink-500/20" },
  music: { icon: Music, color: "text-emerald-400", bg: "bg-emerald-500/20" },
};

export default function LibraryPage() {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold">
            <span className="glow-text">Asset Library</span>
          </h1>
          <p className="text-dark-100 mt-1">Manage scripts, voices, media & music</p>
        </div>
        <button className="glass-button flex items-center gap-2 text-sm">
          <Plus className="w-4 h-4" />
          Upload Asset
        </button>
      </motion.div>

      {/* Filter Tabs */}
      <div className="flex gap-2">
        {["All", "Scripts", "Voices", "Media", "Music"].map((tab) => (
          <button
            key={tab}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              tab === "All"
                ? "bg-primary-600/20 text-primary-400 border border-primary-500/30"
                : "text-dark-100 hover:bg-white/5"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Assets Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {assets.map((asset, index) => {
          const config = typeConfig[asset.type as keyof typeof typeConfig];
          const Icon = config.icon;
          return (
            <motion.div
              key={asset.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="glass-card-hover p-4"
            >
              <div className={`w-10 h-10 rounded-lg ${config.bg} flex items-center justify-center mb-3`}>
                <Icon className={`w-5 h-5 ${config.color}`} />
              </div>
              <p className="text-sm font-medium text-white truncate">{asset.name}</p>
              <p className="text-xs text-dark-200 mt-1 capitalize">{asset.type} · {asset.date}</p>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
