"use client";

import { motion } from "framer-motion";
import type { TaskPhase } from "@/lib/types";

const PHASE_LABELS: Record<TaskPhase, string> = {
  queued: "排队等待",
  parsing: "解析视频",
  understanding: "理解内容",
  rewriting: "时代改写",
  generating: "生成场景",
  packaging: "打包脚本",
  done: "完成",
  failed: "失败",
};

const PHASE_ORDER: TaskPhase[] = [
  "queued",
  "parsing",
  "understanding",
  "rewriting",
  "generating",
  "packaging",
  "done",
];

interface Props {
  phase: TaskPhase;
  progress: number;
  message: string;
}

export function ProgressBar({ phase, progress, message }: Props) {
  const isFailed = phase === "failed";
  const currentIdx = PHASE_ORDER.indexOf(phase);

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="flex justify-between items-center mb-2">
        <motion.span
          key={phase}
          className="text-sm font-medium text-chrono-gold"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {PHASE_LABELS[phase]}
        </motion.span>
        <span className={`text-sm ${isFailed ? "text-red-400" : "text-gray-500"}`}>
          {progress}%
        </span>
      </div>

      <div className="h-2 bg-void-800 rounded-full overflow-hidden">
        <motion.div
          className={`h-full rounded-full ${isFailed ? "bg-red-500" : "bg-chrono-gold"}`}
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        />
      </div>

      <motion.p
        key={message}
        className="text-xs text-gray-500 mt-2 text-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        {message}
      </motion.p>

      <div className="flex justify-between mt-4">
        {(["parsing", "understanding", "rewriting", "generating", "packaging"] as TaskPhase[]).map(
          (item) => {
            const itemIdx = PHASE_ORDER.indexOf(item);
            const isCompleted = itemIdx < currentIdx;
            const isCurrent = itemIdx === currentIdx;

            return (
              <div key={item} className="flex flex-col items-center gap-1">
                <div
                  className={`w-2 h-2 rounded-full transition-colors
                    ${isCompleted ? "bg-chrono-gold" : isCurrent ? "bg-chrono-gold animate-pulse" : "bg-void-700"}`}
                />
                <span className="text-[10px] text-gray-600 hidden sm:block">
                  {PHASE_LABELS[item]}
                </span>
              </div>
            );
          }
        )}
      </div>
    </div>
  );
}
