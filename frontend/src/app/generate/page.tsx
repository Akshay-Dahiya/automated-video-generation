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
  AlertCircle,
} from "lucide-react";
import { scriptAPI, videoAPI } from "@/lib/api";

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
  const [generatedScript, setGeneratedScript] = useState<any>(null);
  const [videoJob, setVideoJob] = useState<any>(null);
  const [error, setError] = useState("");

  const handleGenerateScript = async () => {
    setIsGenerating(true);
    setError("");
    try {
      const result = await scriptAPI.generate({
        topic,
        tone,
        duration_seconds: duration,
      });
      setGeneratedScript(result);
      setCurrentStep(1);
    } catch (e: any) {
      setError(e.message || "Failed to generate script");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleGenerateFullVideo = async () => {
    setIsGenerating(true);
    setError("");
    try {
      const result = await videoAPI.generate({
        topic,
        tone,
        duration_seconds: duration,
      });
      setVideoJob(result);
      setCurrentStep(5); // Jump to render step
    } catch (e: any) {
      setError(e.message || "Failed to start video generation");
    } finally {
      setIsGenerating(false);
    }
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
              <div className="flex gap-3 mt-4">
                <motion.button
                  whileHover={{ scale: 1.01 }}
                  whileTap={{ scale: 0.99 }}
                  onClick={handleGenerateScript}
                  disabled={!topic || isGenerating}
                  className="flex-1 glass-button flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isGenerating ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <FileText className="w-4 h-4" />
                      Generate Script
                    </>
                  )}
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.01 }}
                  whileTap={{ scale: 0.99 }}
                  onClick={handleGenerateFullVideo}
                  disabled={!topic || isGenerating}
                  className="flex-1 px-6 py-3 rounded-xl border border-accent-cyan/30 bg-accent-cyan/10 font-medium text-accent-cyan hover:bg-accent-cyan/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  <Sparkles className="w-4 h-4" />
                  Full Auto Pipeline
                  <ArrowRight className="w-4 h-4" />
                </motion.button>
              </div>

              {error && (
                <div className="flex items-center gap-2 mt-3 p-3 rounded-lg bg-red-500/10 border border-red-500/20">
                  <AlertCircle className="w-4 h-4 text-red-400" />
                  <span className="text-sm text-red-300">{error}</span>
                </div>
              )}
            </div>
          </motion.div>
        )}

        {/* Generated Script Display */}
        {currentStep >= 1 && generatedScript && (
          <motion.div
            key="script-result"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card p-8"
          >
            <div className="flex items-center gap-2 mb-4">
              <Check className="w-5 h-5 text-emerald-400" />
              <h2 className="text-xl font-semibold text-white">Generated Script</h2>
              <span className="ml-auto px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 text-xs">
                Demo Mode
              </span>
            </div>
            <h3 className="text-lg text-primary-300 font-medium mb-4">{generatedScript.title}</h3>
            <div className="space-y-3">
              {generatedScript.sections?.map((section: any, idx: number) => (
                <div key={idx} className="p-4 rounded-xl bg-white/[0.03] border border-white/5">
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`px-2 py-0.5 rounded text-xs font-medium uppercase ${
                      section.type === 'hook' ? 'bg-yellow-500/20 text-yellow-400' :
                      section.type === 'cta' ? 'bg-pink-500/20 text-pink-400' :
                      'bg-primary-500/20 text-primary-400'
                    }`}>{section.type}</span>
                    <span className="text-xs text-dark-200">~{section.estimated_duration}s</span>
                  </div>
                  <p className="text-sm text-dark-50">{section.text}</p>
                  <p className="text-xs text-dark-300 mt-2 italic">Visual: {section.visual_suggestion}</p>
                </div>
              ))}
            </div>
            <div className="flex flex-wrap gap-2 mt-4">
              {generatedScript.hashtags?.map((tag: string) => (
                <span key={tag} className="px-2 py-1 rounded-lg bg-primary-600/20 text-primary-300 text-xs">
                  {tag}
                </span>
              ))}
            </div>
            <p className="text-xs text-dark-300 mt-3">
              {generatedScript.word_count} words · ~{generatedScript.estimated_duration}s estimated duration
            </p>
          </motion.div>
        )}

        {/* Video Job Status */}
        {videoJob && (
          <motion.div
            key="video-job"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card p-6"
          >
            <div className="flex items-center gap-2 mb-3">
              <Film className="w-5 h-5 text-accent-cyan" />
              <h2 className="text-lg font-semibold text-white">Video Generation Started</h2>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex-1 h-2 rounded-full bg-white/10 overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${(videoJob.progress || 0.1) * 100}%` }}
                  className="h-full rounded-full bg-gradient-to-r from-primary-500 to-accent-cyan"
                />
              </div>
              <span className="text-sm text-dark-100 capitalize">{videoJob.status?.replace(/_/g, ' ')}</span>
            </div>
            <p className="text-xs text-dark-300 mt-2">
              Job ID: {videoJob.id} · Topic: {videoJob.topic}
            </p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
