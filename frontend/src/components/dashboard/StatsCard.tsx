"use client";

import { motion } from "framer-motion";
import { LucideIcon } from "lucide-react";

interface StatsCardProps {
  title: string;
  value: string;
  change: string;
  icon: LucideIcon;
  color: "cyan" | "purple" | "pink" | "emerald";
}

const colorMap = {
  cyan: "from-cyan-500/20 to-cyan-600/5 border-cyan-500/20 text-cyan-400",
  purple: "from-purple-500/20 to-purple-600/5 border-purple-500/20 text-purple-400",
  pink: "from-pink-500/20 to-pink-600/5 border-pink-500/20 text-pink-400",
  emerald: "from-emerald-500/20 to-emerald-600/5 border-emerald-500/20 text-emerald-400",
};

const iconBgMap = {
  cyan: "bg-cyan-500/20",
  purple: "bg-purple-500/20",
  pink: "bg-pink-500/20",
  emerald: "bg-emerald-500/20",
};

export function StatsCard({ title, value, change, icon: Icon, color }: StatsCardProps) {
  const isPositive = change.startsWith("+");

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02 }}
      className={`stat-card bg-gradient-to-br ${colorMap[color]} border`}
    >
      <div className="flex items-center justify-between">
        <div className={`p-2 rounded-lg ${iconBgMap[color]}`}>
          <Icon className="w-5 h-5" />
        </div>
        <span
          className={`text-xs font-medium px-2 py-0.5 rounded-full ${
            isPositive
              ? "bg-emerald-500/20 text-emerald-400"
              : "bg-red-500/20 text-red-400"
          }`}
        >
          {change}
        </span>
      </div>
      <div className="mt-3">
        <p className="text-2xl font-bold text-white">{value}</p>
        <p className="text-sm text-dark-100">{title}</p>
      </div>
    </motion.div>
  );
}
