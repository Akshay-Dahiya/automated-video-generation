"use client";

import { motion } from "framer-motion";
import { Bell, Search, User, Menu } from "lucide-react";

export function TopBar() {
  return (
    <header className="h-16 border-b border-white/5 bg-dark-800/30 backdrop-blur-xl flex items-center justify-between px-6">
      {/* Mobile menu toggle */}
      <button className="lg:hidden p-2 rounded-lg hover:bg-white/5">
        <Menu className="w-5 h-5 text-dark-100" />
      </button>

      {/* Search */}
      <div className="hidden md:flex items-center flex-1 max-w-md">
        <div className="relative w-full">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-dark-200" />
          <input
            type="text"
            placeholder="Search videos, scripts..."
            className="w-full pl-10 pr-4 py-2 rounded-xl bg-white/5 border border-white/5 text-sm text-white placeholder:text-dark-200 focus:border-primary-500/30 focus:outline-none focus:ring-1 focus:ring-primary-500/20 transition-all"
          />
        </div>
      </div>

      {/* Right section */}
      <div className="flex items-center gap-3">
        {/* Notifications */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="relative p-2 rounded-xl hover:bg-white/5 transition-colors"
        >
          <Bell className="w-5 h-5 text-dark-100" />
          <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-accent-pink" />
        </motion.button>

        {/* Profile */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="flex items-center gap-2 p-2 rounded-xl hover:bg-white/5 transition-colors"
        >
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-500 to-accent-purple flex items-center justify-center">
            <User className="w-4 h-4 text-white" />
          </div>
        </motion.button>
      </div>
    </header>
  );
}
