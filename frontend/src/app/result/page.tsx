"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { motion } from "framer-motion";
import { getResult } from "@/lib/api";
import { ScriptViewer } from "@/components/script-viewer/ScriptViewer";
import type { VideoScript } from "@/lib/types";

function ResultContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const taskId = searchParams.get("task_id");

  const [script, setScript] = useState<VideoScript | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!taskId) {
      router.push("/");
      return;
    }

    (async () => {
      try {
        const res = await getResult(taskId);
        setScript(res.script);
      } catch {
        setError("加载结果失败，请稍后重试");
      } finally {
        setLoading(false);
      }
    })();
  }, [taskId, router]);

  if (!taskId) return null;

  return (
    <div className="max-w-4xl mx-auto px-4 py-12 space-y-8">
      <div className="flex items-center justify-between gap-3">
        <button
          onClick={() => router.push("/")}
          className="text-sm text-gray-500 hover:text-chrono-gold transition-colors"
        >
          返回首页
        </button>
        <button
          onClick={() => router.push(`/studio?task_id=${taskId}`)}
          className="text-sm text-gray-500 hover:text-chrono-gold transition-colors"
        >
          回到生成室
        </button>
      </div>

      {loading && (
        <div className="text-center py-20">
          <motion.div
            className="inline-block w-8 h-8 border-2 border-chrono-gold border-t-transparent rounded-full"
            animate={{ rotate: 360 }}
            transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
          />
          <p className="text-sm text-gray-500 mt-4">加载结果...</p>
        </div>
      )}

      {error && (
        <div className="text-center py-20">
          <p className="text-red-400">{error}</p>
        </div>
      )}

      {script && <ScriptViewer script={script} />}

      {script && (
        <motion.div
          className="border border-void-700 rounded-xl p-6 bg-void-900/50 space-y-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <h3 className="font-display text-sm text-gray-400">扩展功能</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <button disabled className="p-3 rounded-lg border border-void-700 text-sm text-gray-600 text-left cursor-not-allowed opacity-50">
              匹配背景音乐（接口已预留）
            </button>
            <button disabled className="p-3 rounded-lg border border-void-700 text-sm text-gray-600 text-left cursor-not-allowed opacity-50">
              合成完整视频（接口已预留）
            </button>
          </div>
        </motion.div>
      )}
    </div>
  );
}

export default function ResultPage() {
  return (
    <Suspense fallback={<div className="max-w-4xl mx-auto px-4 py-12 text-center text-gray-500">加载结果...</div>}>
      <ResultContent />
    </Suspense>
  );
}
