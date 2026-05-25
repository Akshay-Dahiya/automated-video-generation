"use client";

import { motion } from "framer-motion";

const chartData = [
  { day: "Mon", videos: 4 },
  { day: "Tue", videos: 7 },
  { day: "Wed", videos: 5 },
  { day: "Thu", videos: 9 },
  { day: "Fri", videos: 6 },
  { day: "Sat", videos: 8 },
  { day: "Sun", videos: 3 },
];

const maxValue = Math.max(...chartData.map((d) => d.videos));

export function GenerationChart() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="glass-card p-6"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-lg font-semibold text-white">
            Generation Activity
          </h2>
          <p className="text-sm text-dark-200">Videos generated this week</p>
        </div>
        <div className="flex gap-2">
          <button className="px-3 py-1 text-xs rounded-lg bg-primary-600/20 text-primary-400 border border-primary-500/20">
            Week
          </button>
          <button className="px-3 py-1 text-xs rounded-lg text-dark-200 hover:bg-white/5 transition-colors">
            Month
          </button>
        </div>
      </div>

      {/* Simple bar chart */}
      <div className="flex items-end gap-3 h-48">
        {chartData.map((item, index) => (
          <div key={item.day} className="flex-1 flex flex-col items-center gap-2">
            <motion.div
              initial={{ height: 0 }}
              animate={{ height: `${(item.videos / maxValue) * 100}%` }}
              transition={{ delay: index * 0.1, duration: 0.5 }}
              className="w-full rounded-t-lg bg-gradient-to-t from-primary-600 to-primary-400 min-h-[8px] relative group"
            >
              {/* Tooltip */}
              <div className="absolute -top-8 left-1/2 -translate-x-1/2 px-2 py-1 rounded bg-dark-600 text-xs text-white opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                {item.videos} videos
              </div>
            </motion.div>
            <span className="text-xs text-dark-200">{item.day}</span>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
