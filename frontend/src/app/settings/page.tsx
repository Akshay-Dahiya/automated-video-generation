"use client";

import { motion } from "framer-motion";
import { Settings, Key, Palette, Bell, Shield, Database } from "lucide-react";

export default function SettingsPage() {
  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-bold">
          <span className="glow-text">Settings</span>
        </h1>
        <p className="text-dark-100 mt-1">Configure your video generation platform</p>
      </motion.div>

      {/* API Keys */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <div className="flex items-center gap-2 mb-4">
          <Key className="w-5 h-5 text-primary-400" />
          <h2 className="text-lg font-semibold text-white">API Keys</h2>
        </div>
        <div className="space-y-3">
          {[
            { label: "OpenAI API Key", placeholder: "sk-...", connected: true },
            { label: "ElevenLabs API Key", placeholder: "Enter key...", connected: true },
            { label: "Pexels API Key", placeholder: "Enter key...", connected: false },
            { label: "Cloudinary", placeholder: "Cloud name...", connected: true },
          ].map((key) => (
            <div key={key.label} className="flex items-center gap-3">
              <div className="flex-1">
                <label className="block text-sm text-dark-100 mb-1">{key.label}</label>
                <input
                  type="password"
                  placeholder={key.placeholder}
                  className="glass-input py-2 text-sm"
                />
              </div>
              <div className={`mt-5 w-2 h-2 rounded-full ${key.connected ? 'bg-emerald-400' : 'bg-red-400'}`} />
            </div>
          ))}
        </div>
        <button className="glass-button mt-4 text-sm px-4 py-2">Save API Keys</button>
      </motion.div>

      {/* Default Settings */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="glass-card p-6"
      >
        <div className="flex items-center gap-2 mb-4">
          <Palette className="w-5 h-5 text-purple-400" />
          <h2 className="text-lg font-semibold text-white">Default Preferences</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm text-dark-100 mb-1">Default Voice</label>
            <select className="glass-input py-2 text-sm">
              <option>Rachel (Female, Professional)</option>
              <option>Antoni (Male, Confident)</option>
              <option>Bella (Female, Friendly)</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-dark-100 mb-1">Default Tone</label>
            <select className="glass-input py-2 text-sm">
              <option>Informative</option>
              <option>Entertaining</option>
              <option>Motivational</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-dark-100 mb-1">Subtitle Style</label>
            <select className="glass-input py-2 text-sm">
              <option>Word Highlight (Karaoke)</option>
              <option>Minimal</option>
              <option>Bold Center</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-dark-100 mb-1">Default Duration</label>
            <select className="glass-input py-2 text-sm">
              <option>30 seconds</option>
              <option>45 seconds</option>
              <option>60 seconds</option>
            </select>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
