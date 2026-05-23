"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { ProgressBar } from "@/components/progress/ProgressBar";
import { getTaskStatus } from "@/lib/api";
import type { TaskPhase } from "@/lib/types";

export default function ProcessingPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const taskId = searchParams.get("task_id");

  const [phase, setPhase] = useState<TaskPhase>("queued");
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState("任务已提交，等待处理...");
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (!taskId) {
      router.push("/");
      return;
    }

    const poll = async () => {
      try {
        const status = await getTaskStatus(taskId);
        setPhase(status.phase);
        setProgress(status.progress);
        setMessage(status.error || status.message);

        if (status.phase === "done") {
          if (pollRef.current) clearInterval(pollRef.current);
          router.push(`/result?task_id=${taskId}`);
        } else if (status.phase === "failed" && pollRef.current) {
          clearInterval(pollRef.current);
        }
      } catch {
        setMessage("正在等待后端响应...");
      }
    };

    poll();
    pollRef.current = setInterval(poll, 1500);

    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, [taskId, router]);

  if (!taskId) return null;

  return (
    <div className="max-w-2xl mx-auto px-4 py-20 space-y-10">
      <div className="text-center space-y-2">
        <h1 className="font-display text-2xl text-chrono-gold">时空穿越中...</h1>
        <p className="text-sm text-gray-500">任务 ID：{taskId}</p>
      </div>

      <ProgressBar phase={phase} progress={progress} message={message} />

      {phase === "failed" && (
        <div className="text-center space-y-3">
          <p className="text-red-400 text-sm">{message}</p>
          <button
            onClick={() => router.push("/")}
            className="text-sm text-chrono-gold hover:underline"
          >
            返回首页重新尝试
          </button>
        </div>
      )}

      <div className="relative h-20 overflow-hidden pointer-events-none">
        {[...Array(6)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-chrono-gold/30 rounded-full"
            style={{
              left: `${10 + i * 16}%`,
              top: "50%",
              animation: `pulseGlow ${2 + i * 0.5}s ease-in-out ${i * 0.3}s infinite`,
            }}
          />
        ))}
      </div>
    </div>
  );
}
