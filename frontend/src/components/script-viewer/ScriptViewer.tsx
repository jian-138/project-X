"use client";

import { motion } from "framer-motion";
import { ERA_OPTIONS, type VideoScript } from "@/lib/types";

interface Props {
  script: VideoScript;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

const TRANSITION_LABELS: Record<string, string> = {
  cut: "直接切入",
  dissolve: "交叠淡入",
  fade: "渐隐渐显",
};

function assetUrl(path: string) {
  if (!path) return "";
  if (path.startsWith("http://") || path.startsWith("https://")) return path;
  return `${API_BASE}/${path.replace(/^\/+/, "")}`;
}

export function ScriptViewer({ script }: Props) {
  const eraName = ERA_OPTIONS.find((era) => era.id === script.era)?.name || script.era;

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4">
        <div className="space-y-2">
          <h2 className="font-display text-lg text-chrono-gold">
            {script.title || "视频脚本"}
          </h2>
          {script.summary && <p className="text-sm text-gray-400 leading-relaxed">{script.summary}</p>}
        </div>
        <span className="shrink-0 text-xs text-gray-500 px-3 py-1 rounded-full border border-void-700">
          {eraName}
        </span>
      </div>

      {script.story_beats && script.story_beats.length > 0 && (
        <div className="rounded-lg border border-void-800 bg-void-950/50 p-4">
          <h3 className="text-xs text-gray-500 mb-2">故事节拍</h3>
          <ol className="space-y-1 text-sm text-gray-300">
            {script.story_beats.map((beat, index) => (
              <li key={`${beat}-${index}`}>{index + 1}. {beat}</li>
            ))}
          </ol>
        </div>
      )}

      <div className="space-y-8">
        {script.scenes.map((scene, index) => (
          <motion.div
            key={scene.index}
            className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 rounded-xl border border-void-800 bg-void-900/50"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.12, duration: 0.35 }}
          >
            <div className="space-y-2">
              <div className="grid grid-cols-2 gap-2">
                <div className="space-y-1">
                  <span className="text-[10px] text-gray-600 uppercase tracking-wider">
                    原视频
                  </span>
                  <div className="aspect-video bg-void-800 rounded-lg flex items-center justify-center text-center px-3 text-xs text-gray-500">
                    关键帧占位
                  </div>
                </div>
                <div className="space-y-1">
                  <span className="text-[10px] text-gray-600 uppercase tracking-wider">
                    时代化
                  </span>
                  {scene.generated_frame ? (
                    <img
                      src={assetUrl(scene.generated_frame)}
                      alt={`场景 ${scene.index + 1} 时代化图像`}
                      className="aspect-video w-full rounded-lg object-cover bg-void-800"
                    />
                  ) : (
                    <div className="aspect-video bg-void-800 rounded-lg flex items-center justify-center text-center px-3 text-xs text-gray-500">
                      生成图占位
                    </div>
                  )}
                </div>
              </div>
              <p className="text-[10px] text-gray-600">
                时间戳：{scene.timestamp.toFixed(1)}s · 转场：
                {TRANSITION_LABELS[scene.transition] || scene.transition}
              </p>
            </div>

            <div className="space-y-3 flex flex-col justify-center">
              <div>
                <span className="text-[10px] text-gray-600 uppercase tracking-wider">台词</span>
                <p className="text-sm text-gray-300 italic mt-1 leading-relaxed">
                  “{scene.dialogue}”
                </p>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[10px] text-gray-600 uppercase tracking-wider">配音</span>
                <button
                  className="text-xs text-chrono-blue hover:text-chrono-gold transition-colors flex items-center gap-1"
                  onClick={() => {
                    if (scene.voice_url) {
                      new Audio(assetUrl(scene.voice_url)).play().catch(() => {});
                    }
                  }}
                >
                  试听
                </button>
                <span className="text-[10px] text-gray-600">音频接口占位</span>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {script.bgm_url === null && (
        <p className="text-xs text-gray-600 text-center italic">
          背景音乐匹配接口已预留，当前版本暂不生成 BGM。
        </p>
      )}
    </div>
  );
}
