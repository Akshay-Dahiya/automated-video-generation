"use client";

import { motion } from "framer-motion";
import {
  Video,
  Sparkles,
  TrendingUp,
  Clock,
  Upload,
  CheckCircle,
  AlertCircle,
  Play,
} from "lucide-react";
import { StatsCard } from "@/components/dashboard/StatsCard";
import { RecentVideos } from "@/components/dashboard/RecentVideos";
import { GenerationChart } from "@/components/dashboard/GenerationChart";
import { QuickActions } from "@/components/dashboard/QuickActions";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Page Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold">
            <span className="glow-text">Dashboard</span>
          </h1>
          <p className="text-dark-100 mt-1">
            Your AI video generation command center
          </p>
        </div>
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="glass-button flex items-center gap-2"
        >
          <Sparkles className="w-4 h-4" />
          Generate New Video
        </motion.button>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="Total Videos"
          value="47"
          change="+12%"
          icon={Video}
          color="cyan"
        />
        <StatsCard
          title="Published"
          value="38"
          change="+8%"
          icon={Upload}
          color="emerald"
        />
        <StatsCard
          title="Total Views"
          value="124.5K"
          change="+23%"
          icon={TrendingUp}
          color="purple"
        />
        <StatsCard
          title="Avg. Gen Time"
          value="2.4 min"
          change="-15%"
          icon={Clock}
          color="pink"
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chart - Takes 2 columns */}
        <div className="lg:col-span-2">
          <GenerationChart />
        </div>

        {/* Quick Actions */}
        <div>
          <QuickActions />
        </div>
      </div>

      {/* Recent Videos */}
      <RecentVideos />
    </div>
  );
}
