"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Sparkles,
  Video,
  Library,
  Upload,
  BarChart3,
  Settings,
  Zap,
} from "lucide-react";

const navItems = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/generate", label: "Generate", icon: Sparkles },
  { href: "/videos", label: "Videos", icon: Video },
  { href: "/library", label: "Library", icon: Library },
  { href: "/upload", label: "Upload", icon: Upload },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <motion.aside
      initial={{ x: -100, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.3 }}
      className="hidden lg:flex w-64 flex-col border-r border-white/5 bg-dark-800/50 backdrop-blur-xl"
    >
      {/* Logo */}
      <div className="flex items-center gap-3 px-6 py-5 border-b border-white/5">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-accent-purple flex items-center justify-center">
          <Zap className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="text-lg font-bold glow-text">VideoGen</h1>
          <p className="text-xs text-dark-200">AI Shorts Creator</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link key={item.href} href={item.href}>
              <motion.div
                whileHover={{ x: 4 }}
                className={isActive ? "nav-link-active" : "nav-link"}
              >
                <item.icon className="w-5 h-5" />
                <span className="text-sm font-medium">{item.label}</span>
                {isActive && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute left-0 w-1 h-8 rounded-r-full bg-primary-500"
                  />
                )}
              </motion.div>
            </Link>
          );
        })}
      </nav>

      {/* Bottom CTA */}
      <div className="p-4 mx-3 mb-4 rounded-xl bg-gradient-to-br from-primary-600/20 to-accent-purple/20 border border-primary-500/20">
        <p className="text-sm font-medium text-white mb-1">Pro Plan</p>
        <p className="text-xs text-dark-200 mb-3">
          Unlimited video generation
        </p>
        <button className="w-full text-xs py-2 rounded-lg bg-primary-600 hover:bg-primary-500 transition-colors font-medium">
          Upgrade Now
        </button>
      </div>
    </motion.aside>
  );
}
