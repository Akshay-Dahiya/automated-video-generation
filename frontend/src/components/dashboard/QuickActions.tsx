"use client";

import { motion } from "framer-motion";
import { Sparkles, FileText, Mic, Film, Upload } from "lucide-react";
import Link from "next/link";

const actions = [
  {
    label: "Generate Video",
    description: "Full AI pipeline",
    icon: Sparkles,
    href: "/generate",
    color: "from-primary-500/20 to-primary-600/5",
    iconColor: "text-primary-400",
  },
  {
    label: "Write Script",
    description: "AI scriptwriter",
    icon: FileText,
    href: "/generate?step=script",
    color: "from-cyan-500/20 to-cyan-600/5",
    iconColor: "text-cyan-400",
  },
  {
    label: "Generate Voice",
    description: "Text to speech",
    icon: Mic,
    href: "/generate?step=voice",
    color: "from-purple-500/20 to-purple-600/5",
    iconColor: "text-purple-400",
  },
  {
    label: "Render Video",
    description: "Compose clips",
    icon: Film,
    href: "/generate?step=render",
    color: "from-pink-500/20 to-pink-600/5",
    iconColor: "text-pink-400",
  },
  {
    label: "Publish",
    description: "Upload to platforms",
    icon: Upload,
    href: "/upload",
    color: "from-emerald-500/20 to-emerald-600/5",
    iconColor: "text-emerald-400",
  },
];

export function QuickActions() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="glass-card p-6"
    >
      <h2 className="text-lg font-semibold text-white mb-4">Quick Actions</h2>
      <div className="space-y-2">
        {actions.map((action, index) => (
          <Link key={action.label} href={action.href}>
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
              whileHover={{ x: 4 }}
              className={`flex items-center gap-3 p-3 rounded-xl bg-gradient-to-r ${action.color} border border-white/5 hover:border-white/10 transition-all cursor-pointer`}
            >
              <div className="p-2 rounded-lg bg-white/5">
                <action.icon className={`w-4 h-4 ${action.iconColor}`} />
              </div>
              <div>
                <p className="text-sm font-medium text-white">{action.label}</p>
                <p className="text-xs text-dark-200">{action.description}</p>
              </div>
            </motion.div>
          </Link>
        ))}
      </div>
    </motion.div>
  );
}
