"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Sparkles,
  FileText,
  Mic,
  Image,
  Captions,
  Film,
  Upload,
  ArrowRight,
  Check,
} from "lucide-react";

const steps = [
  { id: "topic", label: "Topic", icon: Sparkles },
  { id: "script", label: "Script", icon: FileText },
  { id: "voice", label: "Voice", icon: Mic },
  { id: "media", label: "Media", icon: Image },
  { id: "subtitles", label: "Subtitles", icon: Captions },
  { id: "render", label: "Render", icon: Film },
  { id: "publish", label: "Publish", icon: Upload },
];

export default function GeneratePage() {
  const [currentStep, setCurrentStep] = useState(0);
  const [topic, setTopic] = useState("");
  const [tone, setTone] = useState("informative");
  const [duration, setDuration] = useState(60);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async () => {
    setIsGenerating(true);
    // Simulated delay
    setTimeout(() => {
      setIsGenerating(false);
      setCurrentStep(1);
    }, 2000);
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-bold">
          <span className="glow-text">Generate Video</span>
        </h1>
        <p className="text-dark-100 mt-1">
          Create viral short-form content with AI
        </p>
      </motion.div>

      {/* Progress Steps */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-4"
      >
        <div className="flex items-center justify-between">
          {steps.map((step, index) => (
            <div key={step.id} className="flex items-center">
              <div
                className={`flex items-center gap-2 px-3 py-2 rounded-lg transition-all ${
                  index === currentStep
                    ? "bg-primary-600/20 border border-primary-500/30"
                    : index < currentStep
                    ? "bg-emerald-500/10 border border-emerald-500/20"
                    : "opacity-40"
                }`}
              >
                {index < currentStep ? (
                  <Check className="w-4 h-4 text-emerald-400" />
                ) : (
                  <step.icon className={`w-4 h-4 ${
                    index === currentStep ? "text-primary-400" : "text-dark-200"
                  }`} />
                )}
                <span className="text-xs font-medium hidden md:block">
                  {step.label}
                </span>
              </div>
              {index < steps.length - 1 && (
                <div className={`w-4 lg:w-8 h-px mx-1 ${
                  index < currentStep ? "bg-emerald-500/50" : "bg-white/10"
                }`} />
              )}
            </div>
          ))}
        </div>
      </motion.div>

      {/* Step Content */}
      <AnimatePresence mode="wait">
        {currentStep === 0 && (
          <motion.div
            key="topic"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="glass-card p-8"
          >
            <h2 className="text-xl font-semibold text-white mb-6">
              What's your video about?
            </h2>

            {/* Topic Input */}
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-dark-100 mb-2">Topic</label>
                <textarea
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="e.g., 5 AI tools that will replace your job in 2024..."
                  className="glass-input h-24 resize-none"
                />
              </div>

              {/* Tone Selection */}
              <div>
                <label className="block text-sm text-dark-100 mb-2">Tone</label>
                <div className="grid grid-cols-3 md:grid-cols-6 gap-2">
                  {["informative", "entertaining", "motivational", "educational", "humorous", "dramatic"].map(
                    (t) => (
                      <button
                        key={t}
                        onClick={() => setTone(t)}
                        className={`px-3 py-2 rounded-lg text-xs font-medium capitalize transition-all ${
                          tone === t
                            ? "bg-primary-600/30 border border-primary-500/50 text-primary-300"
                            : "bg-white/5 border border-white/5 text-dark-100 hover:bg-white/10"
                        }`}
                      >
                        {t}
                      </button>
                    )
                  )}
                </div>
              </div>

              {/* Duration */}
              <div>
                <label className="block text-sm text-dark-100 mb-2">
                  Duration: {duration}s
                </label>
                <input
                  type="range"
                  min={15}
                  max={90}
                  value={duration}
                  onChange={(e) => setDuration(Number(e.target.value))}
                  className="w-full accent-primary-500"
                />
                <div className="flex justify-between text-xs text-dark-200">
                  <span>15s</span>
                  <span>90s</span>
                </div>
              </div>

              {/* Generate Button */}
              <motion.button
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
                onClick={handleGenerate}
                disabled={!topic || isGenerating}
                className="w-full glass-button flex items-center justify-center gap-2 mt-4 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isGenerating ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Generating...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    Generate Script
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </motion.button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
