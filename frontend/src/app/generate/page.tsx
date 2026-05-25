"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  Sparkles,
  FileText,
  Mic,
  Image,
  Subtitles,
  Film,
  Upload,
  ArrowRight,
  Check,
  AlertCircle,
  RefreshCw,
} from "lucide-react";
import { mockScriptGeneration } from "@/lib/mock-data";

const steps = [
  { id: "topic", label: "Topic", icon: Sparkles },
  { id: "script", label: "Script", icon: FileText },
  { id: "voice", label: "Voice", icon: Mic },
  { id: "media", label: "Media", icon: Image },
  { id: "subtitles", label: "Subtitles", icon: Subtitles },
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

  const handleGenerateScript = async () => {
    setIsGenerating(true);
    // Simulate API delay then return mock data
    await new Promise((r) => setTimeout(r, 1500));
    const script = {
      ...mockScriptGeneration,
      topic,
      title: `${topic} - What Nobody Tells You`,
      sections: [
        {
          type: "hook",
          text: `Stop scrolling! What I'm about to tell you about ${topic} will completely change your perspective.`,
          estimated_duration: 4.0,
          visual_suggestion: "Eye-catching visual with bold text overlay and zoom effect",
        },
        {
          type: "body",
          text: `Here's the thing about ${topic} that nobody talks about. The world is changing fast, and if you're not paying attention, you'll be left behind. Let me break this down. First, the technology behind this is evolving exponentially. Second, early adopters are seeing massive results already. Third, it's more accessible than ever before. The key is to start now, even if you start small.`,
          estimated_duration: duration - 12,
          visual_suggestion: "Dynamic b-roll with text callouts highlighting each numbered point",
        },
        {
          type: "cta",
          text: "Follow for more insights like this, and comment which point resonated with you the most!",
          estimated_duration: 6.0,
          visual_suggestion: "Subscribe animation with engagement prompt overlay",
        },
      ],
      hashtags: [`#${topic.split(" ")[0]}`, "#Viral", "#MustWatch", "#Trending", "#Shorts"],
      word_count: 142,
      estimated_duration: duration,
    };
    setGeneratedScript(script);
    setCurrentStep(1);
    setIsGenerating(false);
  };

  const handleFullPipeline = async () => {
    setIsGenerating(true);
    setCurrentStep(0);
    setGeneratedScript(null);

    // Simulate full pipeline with progressive steps
    for (let i = 0; i < steps.length; i++) {
      setCurrentStep(i);
      await new Promise((r) => setTimeout(r, 800));
    }

    setVideoJob({
      id: `vid-${Date.now().toString(36)}`,
      status: "completed",
      topic,
      progress: 1.0,
      duration: duration,
      video_url: "./output/demo_video.mp4",
    });
    setIsGenerating(false);
  };

  const handleReset = () => {
    setCurrentStep(0);
    setGeneratedScript(null);
    setVideoJob(null);
    setTopic("");
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-bold">
          <span className="glow-text">Generate Video</span>
        </h1>
        <p className="text-dark-100 mt-1">Create viral short-form content with AI</p>
      </motion.div>

      {/* Progress Steps */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-4">
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
                  <step.icon className={`w-4 h-4 ${index === currentStep ? "text-primary-400" : "text-dark-200"}`} />
                )}
                <span className="text-xs font-medium hidden md:block">{step.label}</span>
              </div>
              {index < steps.length - 1 && (
                <div className={`w-4 lg:w-8 h-px mx-1 ${index < currentStep ? "bg-emerald-500/50" : "bg-white/10"}`} />
              )}
            </div>
          ))}
        </div>
      </motion.div>

      {/* Topic Input (Step 0) */}
      {currentStep === 0 && !videoJob && (
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="glass-card p-8">
          <h2 className="text-xl font-semibold text-white mb-6">What's your video about?</h2>
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

            <div>
              <label className="block text-sm text-dark-100 mb-2">Tone</label>
              <div className="grid grid-cols-3 md:grid-cols-6 gap-2">
                {["informative", "entertaining", "motivational", "educational", "humorous", "dramatic"].map((t) => (
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
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm text-dark-100 mb-2">Duration: {duration}s</label>
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

            <div className="flex gap-3 mt-4">
              <motion.button
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
                onClick={handleGenerateScript}
                disabled={!topic || isGenerating}
                className="flex-1 glass-button flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isGenerating ? (
                  <><div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" /> Generating...</>
                ) : (
                  <><FileText className="w-4 h-4" /> Generate Script</>
                )}
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
                onClick={handleFullPipeline}
                disabled={!topic || isGenerating}
                className="flex-1 px-6 py-3 rounded-xl border border-accent-cyan/30 bg-accent-cyan/10 font-medium text-accent-cyan hover:bg-accent-cyan/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {isGenerating ? (
                  <><div className="w-4 h-4 border-2 border-cyan-300/30 border-t-cyan-300 rounded-full animate-spin" /> Processing...</>
                ) : (
                  <><Sparkles className="w-4 h-4" /> Full Auto <ArrowRight className="w-4 h-4" /></>
                )}
              </motion.button>
            </div>
          </div>
        </motion.div>
      )}

      {/* Generated Script Display */}
      {generatedScript && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-8">
          <div className="flex items-center gap-2 mb-4">
            <Check className="w-5 h-5 text-emerald-400" />
            <h2 className="text-xl font-semibold text-white">Generated Script</h2>
            <span className="ml-auto px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 text-xs">Ready</span>
          </div>
          <h3 className="text-lg text-primary-300 font-medium mb-4">{generatedScript.title}</h3>
          <div className="space-y-3">
            {generatedScript.sections?.map((section: any, idx: number) => (
              <div key={idx} className="p-4 rounded-xl bg-white/[0.03] border border-white/5">
                <div className="flex items-center gap-2 mb-2">
                  <span className={`px-2 py-0.5 rounded text-xs font-medium uppercase ${
                    section.type === "hook" ? "bg-yellow-500/20 text-yellow-400" :
                    section.type === "cta" ? "bg-pink-500/20 text-pink-400" :
                    "bg-primary-500/20 text-primary-400"
                  }`}>{section.type}</span>
                  <span className="text-xs text-dark-200">~{section.estimated_duration}s</span>
                </div>
                <p className="text-sm text-dark-50 leading-relaxed">{section.text}</p>
                <p className="text-xs text-dark-300 mt-2 italic">Visual: {section.visual_suggestion}</p>
              </div>
            ))}
          </div>
          <div className="flex flex-wrap gap-2 mt-4">
            {generatedScript.hashtags?.map((tag: string) => (
              <span key={tag} className="px-2 py-1 rounded-lg bg-primary-600/20 text-primary-300 text-xs">{tag}</span>
            ))}
          </div>
          <p className="text-xs text-dark-300 mt-3">
            {generatedScript.word_count} words · ~{generatedScript.estimated_duration}s
          </p>
          <button onClick={handleReset} className="mt-4 flex items-center gap-2 text-sm text-dark-100 hover:text-white transition-colors">
            <RefreshCw className="w-4 h-4" /> Generate another
          </button>
        </motion.div>
      )}

      {/* Video Job Completed */}
      {videoJob && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6">
          <div className="flex items-center gap-2 mb-3">
            <Check className="w-5 h-5 text-emerald-400" />
            <h2 className="text-lg font-semibold text-white">Video Generated Successfully</h2>
          </div>
          <div className="flex items-center gap-4 mb-3">
            <div className="flex-1 h-2 rounded-full bg-white/10 overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: "100%" }}
                transition={{ duration: 0.5 }}
                className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-accent-cyan"
              />
            </div>
            <span className="text-sm text-emerald-400 font-medium">Complete</span>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-4">
            <div className="p-3 rounded-lg bg-white/[0.03] text-center">
              <p className="text-lg font-bold text-white">{videoJob.duration}s</p>
              <p className="text-xs text-dark-200">Duration</p>
            </div>
            <div className="p-3 rounded-lg bg-white/[0.03] text-center">
              <p className="text-lg font-bold text-white">1080x1920</p>
              <p className="text-xs text-dark-200">Resolution</p>
            </div>
            <div className="p-3 rounded-lg bg-white/[0.03] text-center">
              <p className="text-lg font-bold text-white">30fps</p>
              <p className="text-xs text-dark-200">Frame Rate</p>
            </div>
            <div className="p-3 rounded-lg bg-white/[0.03] text-center">
              <p className="text-lg font-bold text-white">H.264</p>
              <p className="text-xs text-dark-200">Codec</p>
            </div>
          </div>
          <div className="flex gap-3 mt-4">
            <button className="flex-1 glass-button flex items-center justify-center gap-2 text-sm">
              <Upload className="w-4 h-4" /> Publish to Platforms
            </button>
            <button onClick={handleReset} className="px-4 py-2 rounded-xl bg-white/5 border border-white/10 text-sm text-dark-100 hover:text-white transition-colors flex items-center gap-2">
              <RefreshCw className="w-4 h-4" /> New Video
            </button>
          </div>
        </motion.div>
      )}
    </div>
  );
}
